from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator

from .models import CustomUser
from .forms import CustomUserProfileForm

@login_required
def logout_view(request):
    
    if request.user.is_authenticated:
        logout(request)
        return redirect('boards:home')

    return redirect('boards:home')

@login_required
def user_account_delete(request, pk):
    
    previous_page = request.META.get('HTTP_REFERER')

    if request.method == 'POST':
        request.user.delete()
        return redirect('boards:home')
    
    context = {'previous_page': previous_page}
    return render(request, 'account/account_deletion.html', context)


@login_required(login_url='account_login')
def user_profile_view(request, username):
    """
    Display user information, such as how many posts user has written,
    How many comments has written and all posts, favorite topics.
    it would be fine to just send 'request.user', then in the template
    using queries, most of the models from foreign key can be display.
    but for convinience wise, I will disect required information.
    """
    
    if request.user.username == username:
        user_info = request.user
        user_topics = request.user.favorite.all()
        user_posts = request.user.post_set.all()
        user_comments = request.user.comment_set.all()
        user_likes = request.user.like.all()
        
        paginator = Paginator(user_posts, 5)
        page_number = request.GET.get('page')
        post_page_obj = paginator.get_page(page_number)
        
        # Since there is already default file for avatar, I specify instance attribute.
        form = CustomUserProfileForm(instance=user_info)
        
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    
    context = {
        'form': form,
        'user_info': user_info,
        'user_topics': user_topics,
        'user_posts': user_posts,
        'user_comments': user_comments,
        'user_likes': user_likes,
        'post_page_obj': post_page_obj,
    }
    return render(request, 'account/user_profile.html', context)


@login_required(login_url='account_login')
def user_edit(request, pk):
        
    user = request.user
    
    if request.method == 'POST':
        
        # I set instance=user, even though for now it's just one file.
        # in case, there is going to be further information to edit later,
        form = CustomUserProfileForm(
            request.POST,
            request.FILES,
            instance=user,
        )
        
        if form.is_valid():
            form.save()
            return redirect('user:profile', request.user.username)
    
    else:
        return redirect('user:profile', request.user.username)

