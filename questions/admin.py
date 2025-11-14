from django.contrib import admin
from .models import Topic, Entry, Question, Submission, Answer
# Register your models here.
#
admin.site.register(Topic)

@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    list_display = ("text", "date_added")
    search_fields = ("topic", "text")

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("prompt", "order", "slug")
    search_fields = ("prompt", "slug")


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ("nickname", "created")
    search_fields = ("nickname",)


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ("question", "value_text", "short_value")
    search_fields = ("value_text", "question_prompt", "submission_nickname")
    autocomplete_fields = ("submission", "question")

    def short_value(self, obj):
        return (obj.value_text or "")[:60]
