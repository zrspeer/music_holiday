from django.shortcuts import get_object_or_404, redirect, render

from .forms import EntryForm, TopicForm
from .models import Answer, Question, Submission, Topic

# Create your views here.


def index(request):
    """Home page for questions app"""
    return render(request, "questions/index.html")


def topics(request):
    """Show all topics."""
    topics = Topic.objects.order_by("date_added")
    context = {"topics": topics}
    return render(request, "questions/topics.html", context)


def topic(request, topic_id):
    """Show single topic and all its entries"""
    topic = Topic.objects.get(id=topic_id)
    entries = topic.entry_set.order_by("-date_added")
    context = {"topic": topic, "entries": entries}
    return render(request, "questions/topic.html", context)


def question(request, question_id):
    """Show a question"""
    question = get_object_or_404(Question, id=question_id)

    if request.method == "POST":
        next_question = (
            Question.objects.filter(order__gt=question.order)
            .order_by("order", "id")
            .first()
        )

        if next_question:
            return redirect("questions:question", question_id=next_question.id)
        else:
            return redirect("questions:thank_you")

    context = {
        "question": question,
        "answer": "",
        "submitted": False,
    }
    return render(request, "questions/question.html", context)


def question_list(request):
    questions = Question.objects.all()
    context = {"questions": questions}
    return render(request, "questions/question_list.html", context)


def thank_you(request):
    return render(request, "questions/thank_you.html")


def new_topic(request):
    """Add a new topic"""
    if request.method != "POST":
        # No data submitted; create a blank form.
        form = TopicForm()
    else:
        # POST data submitted; process data.
        form = TopicForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect("questions:topics")
    # Display blank or invalid form.
    context = {"form": form}
    return render(request, "questions/new_topic.html", context)


def new_entry(request, topic_id):
    """Add a new entry for a particular topic"""
    topic = Topic.objects.get(id=topic_id)

    if request.method != "POST":
        form = EntryForm()
    else:
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return redirect("questions:topic", topic_id=topic_id)
    # Display a blank or invalid form.
    context = {"topic": topic, "form": form}
    return render(request, "questions/new_entry.html", context)
