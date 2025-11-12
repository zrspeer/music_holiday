from django.shortcuts import render

from .models import Topic

# Create your views here.

def index(request):
    """Home page for questions app"""
    return render(request, 'questions/index.html')

def topics(request):
    """Show all topics."""
    topics = Topic.objects.order_by('date_added')
    context = {'topics': topics}
    return render(request, 'questions/topics.html', context)

def topic(request, topic_id):
    """Show single topic and all its entries"""
    topic = Topic.objects.get(id=topic_id)
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'questions/topic.html', context)
