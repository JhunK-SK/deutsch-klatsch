from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from boards.models import Topic

@login_required(login_url='account_login')
def chat_room(request, topic):
    topic = get_object_or_404(Topic, topic=topic)
    
    context = {
        'topic': topic,
        'room_name': topic.slug,
    }
    return render(request, 'chat/chat_room.html', context)