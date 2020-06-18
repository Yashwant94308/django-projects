from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import Topic, Entry
from .forms import TopicForm, EntryForm


# Create your views here.
def index(request):
    """home page for learning logs"""
    return render(request, 'learning_logs/index.html')


@login_required
def topics(request):
    """show all topics"""
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context)


@login_required
# requesting for single topic in detail
def topic(request, topic_id):
    """show all topics"""
    topic = get_object_or_404(Topic, id=topic_id)
    # Make sure the topic belongs to the current user.
    if topic.owner != request.user:
        raise Http404

    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'learning_logs/topic.html', context)


@login_required
def new_topic(request):
    # add a new topic
    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = TopicForm()
    else:
        # POST data submitted; process data.
        form = TopicForm(request.POST)
        if form.is_valid():
            new_topics = form.save(commit=False)
            new_topics.owner = request.user
            new_topics.save()
            return HttpResponseRedirect(reverse('learning_logs:topics'))
    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)


@login_required
def new_entry(request, topic_id):
    """Add a new entry for a particular topic."""
    topic = get_object_or_404(Topic, id=topic_id)
    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = EntryForm()
    else:
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entries = form.save(commit=False)
            new_entries.topic = topic
            new_entries.save()
            return HttpResponseRedirect(reverse('learning_logs:topic', args=[topic_id]))
    context = {'topic': topic, 'form': form}
    return render(request, 'learning_logs/new_entry.html', context)


@login_required
def edit_entry(request, entry_id):
    """Edit an existing entry."""
    entry = get_object_or_404(Entry, id=entry_id)
    topic = entry.topic
    if topic.owner != request.user:
        raise Http404

    if request.method != 'POST':
        # Initial request; pre-fill form with the current entry.
        form = EntryForm(instance=entry)
    else:
        # POST data submitted; process data.
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('learning_logs:topic', args=[topic.id]))
    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'learning_logs/edit_entry.html', context)


@login_required
def delete_topic(request, topic_id):
    # Delete an existing entry.
    topic = get_object_or_404(Topic, id=topic_id)

    if request.method == 'POST':
        topic.delete()
        return HttpResponseRedirect(reverse('learning_logs:topics'))
    context = {'topic': topic}
    return render(request, 'learning_logs/delete_topic.html', context)


@login_required
def delete_entry(request, entry_id):
    # Delete an existing entry.
    entry = get_object_or_404(Entry, id=entry_id)
    topic = entry.topic

    if request.method == 'POST':
        entry.delete()
        return HttpResponseRedirect(reverse('learning_logs:topic', args=[topic.id]))
    context = {'entry': entry, 'topic': topic}
    return render(request, 'learning_logs/delete_entry.html', context)
