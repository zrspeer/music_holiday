from django.shortcuts import get_object_or_404, redirect, render

from .models import Answer, Question, Submission

# Create your views here.


def index(request):
    """Home page for questions app"""
    return render(request, "questions/index.html")


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
