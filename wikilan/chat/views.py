from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate, login
from .forms import *
from .models import *

# Create your views here.
def lobby(request):
    threads = MessageThread.objects.all().reverse
    print(threads)
    return render(request, 'lobby.html', {"threads": threads})

# creates a new session
def start(request):
    if request.method == 'POST':
        form = SessionForm(request.POST)
        if form.is_valid():
            session = form.save(commit=False)
            session.admin = request.user
            session.save()
            return redirect('lobby')
    else:
        form = SessionForm()
    return render(request, 'start_session.html', {"form": form})

# 
def session(request, id):
    session = Session.objects.get(id=id)
    messages = Message.objects.filter(session=session)[0:80]
    
    context={
        'session_id': id,
        'session': session.name,
        'messages': messages,
    }
    return render(request, 'session.html', context)
        

def chat(request):
    sessions = Session.objects.all()
    context = {
        'sessions': sessions
    }
    return render(request, 'chat.html', context)


# Open a thread
def thread(request, id):
    thread = MessageThread.objects.get(id=id)
    if request.method == 'POST':
        form = ThreadReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.user = request.user
            reply.key = thread.id
            thread.id = id
            thread.save()
            reply.save()

            return redirect('/chat/thread/'+str(id))
    else:
        form = ThreadReplyForm()

    # thread = MessageThread.objects.filter(id=id)
    replies=ThreadReply.objects.filter(key=id)
    context={
        'form':form,
        'thread': thread,
        'replies':replies
    }
    return render(request, 'thread_replies.html', context)


# Add a new thread
def add_thread(request):
    if request.method == 'POST':
        form = ThreadForm(request.POST)
        if form.is_valid():
            thread = form.save(commit=False)
            thread.user = request.user
            thread.save()
            return redirect('/chat')
    else:
        form = ThreadForm()
    return render(request, 'add_thread.html', {"form": form})

def delete_thread(request, pk):
    thread = MessageThread.objects.get(id=pk)
    thread.delete()
    return redirect('/lobby')

def search(request):
    query = request.GET.get('q')
    if query is not None and query.strip():  # Check if query is not None and is not an empty string
        sessions = Session.objects.filter(name__icontains=query)
    else:
        sessions = []

    context = {
        'query': query,
        'sessions': sessions
    }
    return render(request, 'search.html', context)
