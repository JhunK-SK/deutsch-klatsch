from django.conf import settings
from django.views.decorators.cache import cache_page
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.core.paginator import Paginator
from django.views.decorators.csrf import ensure_csrf_cookie
from django.db.models import Q

from .models import Board, Topic, Post, Comment, IpModel, TopicRequest
from .forms import (
    PostCreationForm,
    CommentCreationForm,
    PostSearchFormInTopic,
    TopicRequestForm,
)

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)
# @cache_page(CACHE_TTL)

def index(request):
    # Display all boards(higher Categories) with linked Topics.
    # to create cards according to the number of baords.
    
    boards = Board.objects.all()
    context = {
        'boards': boards,
        'range': range(boards.count())
    }
    return render(request, 'home.html', context)


def topic_view(request, slug):
    # This topic view might be better with generic ListView.
    # Display all posts from specific topic.
    # there is also 3rd party packages for pagination.
    
    topic = Topic.objects.get(slug=slug)
    posts = topic.post_set.all()
    
    post_search = PostSearchFormInTopic()
    
    if 'search' in request.GET:
        
        search = request.GET.get('search')
        select = request.GET.get('select')

        if select == 'title_post':
            queried_posts = posts.filter(
                Q(title__icontains=search) | Q(post__icontains=search))
            
        elif select == 'writer':
            queried_posts = posts.filter(Q(writer__username__icontains=search))
        
        else:
            pass
        
        # limit the posts objects to queried post from post search section
        posts = queried_posts    
        
    paginator = Paginator(posts, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'topic': topic,
        'posts': posts,
        'page_obj': page_obj,
        'post_search': post_search,
    }
    return render(request, 'boards/topic_view.html', context)


@ensure_csrf_cookie
def topic_favorite_view(request):
    
    if not request.user.is_authenticated:
        return JsonResponse({'result': 'false'})
    
    if request.is_ajax():
        topic = get_object_or_404(Topic, slug=request.POST.get('topic_slug'))
        
        response = ''
        if topic.favorites.filter(id=request.user.id).exists():
            topic.favorites.remove(request.user)
            topic.save()
            response = {'result': 'removed'}

        else:
            topic.favorites.add(request.user)
            topic.save()
            response = {'result': 'added'}

        return JsonResponse(response, status=200)


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def post_view(request, pk):
    
    # display specific post and comment form which will be dealt in add-comment function by ajax.
    post = Post.objects.get(id=pk)
    comments = post.comments.all()
    form = CommentCreationForm()
    
    # Check if request user ip already exists in Post model.
    # get_or_create returns tuple, (object and boolean(created or not))
    ip = get_client_ip(request)
    visitor, created = IpModel.objects.get_or_create(ip=ip)
    
    if not visitor.post.filter(id=post.id).exists():
        print('there\'s no post in this ip')
        visitor.post.add(post)
        visitor.save()
        post.view_count += 1
        post.save()
            
    context = {
        'post': post,
        'form': form, 
        'comments': comments,
        'topic': post.topic,
    }
    return render(request, 'boards/post_view.html', context)


@login_required(login_url='account_login')
def create_post_view(request, slug):
    
    topic = Topic.objects.get(slug=slug)
    form = PostCreationForm()
    
    if request.method == 'POST':
        form = PostCreationForm(request.POST)
        
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.topic = Topic.objects.get(slug=slug)
            new_post.writer = request.user # getting current user from request.
            new_post.save()
            return redirect('boards:topic', slug)
    
    context = {'form': form, 'topic': topic}
    return render(request, 'boards/create_post_view.html', context)


@login_required(login_url='account_login')
def edit_post_view(request, pk):
    
    post = Post.objects.get(id=pk)
    previous_page = request.META.get('HTTP_REFERER', '/')
    
    if request.user != post.writer:
        return redirect('boards:post', pk)
    
    else:
        form = PostCreationForm(instance=post)
        
        if request.method == 'POST':
            form = PostCreationForm(request.POST, instance=post)
            
            if form.is_valid():
                form.save()
                return redirect('boards:post', pk)
        
        context = {
            'form': form,
            'post': post, 
            'topic': post.topic,
            'previous_page': previous_page,
        }
        return render(request, 'boards/edit_post_view.html', context)


@login_required(login_url='account_login')
def delete_post_view(request, pk):
    
    post = Post.objects.get(id=pk)
    slug = post.topic.slug
    previous_page = request.META.get('HTTP_REFERER')
    
    if request.user != post.writer:
        return redirect('boards:post', pk)
    
    else:
        if request.method == 'POST':
            post.delete()
            return redirect('boards:topic', slug)
        
        context = {'post': post, 'topic': post.topic, 'previous_page': previous_page}
        return render(request, 'boards/delete_post_view.html', context)


def post_likes_view(request):
    
    if not request.user.is_authenticated:
        return JsonResponse({'result': 'false'})
    
    if request.is_ajax():
        post = get_object_or_404(Post, id=request.POST.get('post_id'))
        
        response = ''
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
            post.like_count -= 1
            post.save()
            response = {'result': 'minus', 'count': post.like_count}

        else:
            post.likes.add(request.user)
            post.like_count += 1
            post.save()
            response = {'result': 'plus', 'count': post.like_count}

        return JsonResponse(response, status=200)
    

def add_comment_view(request, pk):
    # getting a request from front ajax and response.
    
    data = {}
    if request.is_ajax():
        if not request.user or not request.user.is_authenticated:
            data['success'] = 'false'
            data['url'] = 'http://127.0.0.1:8000/accounts/login/'
            return JsonResponse(data, status=404)
        
        form = CommentCreationForm(request.POST)
        
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.writer = request.user
            new_comment.post = Post.objects.get(id=pk)
            new_comment.save()
            
            # Since data from views can not be rendered dynamically in html,
            # django should send rendered data in response to ajax call.
            data['username'] = new_comment.writer.username
            data['comment'] = new_comment.comment
            data['id'] = new_comment.id
    
            return JsonResponse(data, status=200)
    
    return redirect('boards:post', pk)


def delete_comment_view(request, pk):
    
    comment = Comment.objects.get(id=pk)
    post = comment.post
    
    if request.user.is_authenticated and request.user == comment.writer:
        comment.delete()
        return redirect('boards:post', post.id)

    return redirect('boards:post', post.id)


def topic_request(request):
    
    requests = TopicRequest.objects.all()
    
    paginator = Paginator(requests, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {'request_obj': page_obj}
    return render(request, 'boards/topic_request_list.html', context)


@login_required(login_url='account_login')
def topic_request_create(request):
    
    form = TopicRequestForm()
    
    if request.method == 'POST':
        form = TopicRequestForm(request.POST)
        
        if form.is_valid():
            new_request = form.save(commit=False)
            new_request.writer = request.user
            new_request.save()
            return redirect('boards:request_list')

    
    context = {'form': form}
    return render(request, 'boards/topic_request_create.html', context)


def request_recommendation(request):
    
    if not request.user.is_authenticated:
        return JsonResponse({'result': 'false'})
    
    if request.is_ajax():
        request_id = request.POST.get('request_id')
        requested_topic = get_object_or_404(TopicRequest, id=request_id) 
               
        response = {
                'request_id': requested_topic.id,
                }
        if requested_topic.recommendations.filter(id=request.user.id).exists():
            requested_topic.recommendations.remove(request.user)
            requested_topic.like_count -= 1
            requested_topic.save()
            response['result'] = 'minus'
            
        
        else:
            requested_topic.recommendations.add(request.user)
            requested_topic.like_count += 1
            requested_topic.save()
            response['result'] = 'plus'
    
        return JsonResponse(response, status=200)



class AboutView(TemplateView):
    template_name = 'about.html'