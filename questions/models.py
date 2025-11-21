from django.db import models


class Question(models.Model):
    # Choice between text and radio buttons
    INPUT_TYPE_CHOICES = [("text", "Text"), ("radio", "Radio")]

    prompt = models.CharField(max_length=500)
    required = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    input_type = models.CharField(
        max_length=10,
        choices=INPUT_TYPE_CHOICES,
        default="text",
    )

    choices = models.TextField(
        blank=True,
    )

    def get_choices_list(self):
        # Returns list of choice strings for radio questions
        if not self.choices:
            return []

        raw_choices = self.choices.split(",")
        cleaned = []

        for choice in raw_choices:
            item = choice.strip()
            if item:
                cleaned.append(item)

        return cleaned

    class Meta:
        ordering = ("order", "id")

    def __str__(self):
        return f"{self.order}, {self.prompt[:60]}"


class Submission(models.Model):
    name = models.CharField(max_length=200, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        who = self.name or "anonymous"
        return f"{who} @ {self.created:%Y-%m-%d %H:%M}"


class Answer(models.Model):
    submission = models.ForeignKey(
        Submission, on_delete=models.CASCADE, related_name="answers"
    )
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    value_text = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = [("submission", "question")]

    def __str__(self):
        return f"{self.question.slug} -> {(self.value_text or '')[:40]}"
