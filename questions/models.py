from django.db import models


class Topic(models.Model):
    text = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text

class Entry(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'entries'

    def __str__(self):
        return self.text[:20] + ("..." if len(self.text) > 20 else "")


class Question(models.Model):
    prompt = models.CharField(max_length=500)
    required = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        ordering = ("order", "id")

    def __str__(self):
        return f"{self.order}, {self.prompt[:60]}"

class Submission(models.Model):
    nickname = models.CharField(max_length=100, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        who = self.nickname or "anonymous"
        return f"{who} @ {self.created:%Y-%m-%d %H:%M}"


class Answer(models.Model):
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE, related_name="answers")
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    value_text = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = [("submission", "question")]

    def __str__(self):
        return f"{self.question.slug} -> {(self.value_text or '')[:40]}"
