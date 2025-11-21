from django.conf import settings
from django.shortcuts import get_object_or_404, redirect, render

from .forms import AnswerForm, PasscodeForm
from .models import Answer, Question, Submission

SURVEY_PASSCODE = settings.SURVEY_PASSCODE


def index(request):
    """Home page for questions app"""
    if not request.session.get("gate_ok"):
        return redirect("questions:gate")

    first_question = Question.objects.order_by("order", "id").first()
    return render(
        request,
        "questions/index.html",
        {"first_question": first_question},
    )


def get_or_create_submission(request):
    submission_id = request.session.get("submission_id")
    if submission_id:
        try:
            return Submission.objects.get(id=submission_id)
        except Submission.DoesNotExist:
            pass

    submission = Submission.objects.create()
    request.session["submission_id"] = submission.id
    return submission


def question_list(request):
    questions = Question.objects.all()
    context = {"questions": questions}
    return render(request, "questions/question_list.html", context)


def question(request, question_id):
    if not request.session.get("gate_ok"):
        return redirect("questions:gate")

    question = get_object_or_404(Question, id=question_id)
    submission = get_or_create_submission(request)

    answer_obj, _ = Answer.objects.get_or_create(
        submission=submission, question=question, defaults={"value_text": ""}
    )

    submitted = False

    if request.method == "POST":
        form = AnswerForm(
            data=request.POST,
            question=question,
            instance=answer_obj,
        )

        if form.is_valid():
            answer = form.save()
            submitted = True

            if question.slug == "name" and not submission.name:
                submission.name = (answer.value_text or "").strip()
                submission.save(update_fields=["name"])

            next_question = (
                Question.objects.filter(order__gt=question.order)
                .order_by("order", "id")
                .first()
            )
            if next_question:
                return redirect(
                    "questions:question",
                    question_id=next_question.id,
                )
            else:
                return redirect("questions:thank_you")
    else:
        form = AnswerForm(
            question=question,
            instance=answer_obj,
        )

    context = {
        "question": question,
        "form": form,
        "submitted": submitted,
    }

    return render(request, "questions/question.html", context)


def thank_you(request):
    return render(request, "questions/thank_you.html")


def info(request):
    return render(request, "questions/info.html")


def gate(request):
    if request.session.get("gate_ok"):
        return redirect("questions:index")

    if request.method == "POST":
        form = PasscodeForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data["code"]
            if code == SURVEY_PASSCODE:
                request.session["gate_ok"] = True
                return redirect("questions:index")
            else:
                form.add_error(
                    "code", "Incorrect code. Ask Zach if you're doing it right."
                )

    else:
        form = PasscodeForm()

    return render(request, "questions/gate.html", {"form": form})
