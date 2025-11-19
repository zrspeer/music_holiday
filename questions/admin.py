from django.contrib import admin

from .models import Answer, Question, Submission


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 0
    fields = ("question", "value_text", "short_value")
    readonly_fields = ("short_value",)

    def short_value(self, obj):
        return (obj.value_text or "")[:60]


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("prompt", "order", "slug")
    search_fields = ("prompt", "slug")
    fields = ("prompt", "description", "order", "slug")


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ("name", "created")
    search_fields = ("name",)
    inlines = [AnswerInline]


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ("submission", "question", "short_value")
    search_fields = ("value_text", "question__prompt", "submission__name")
    autocomplete_fields = ("submission", "question")

    def short_value(self, obj):
        return (obj.value_text or "")[:60]
