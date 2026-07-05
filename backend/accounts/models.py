from django.db import models


class UserProfile(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=100)

    streak = models.IntegerField(default=0)

    last_review_date = models.DateField(
        null=True,
        blank=True
    )

    def __str__(self):
        return self.username

class Goal(models.Model):

    user = models.ForeignKey(
    UserProfile,
    on_delete=models.CASCADE,
    related_name="goals",
    null=True,
    blank=True
)

    title = models.CharField(max_length=200)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
class Project(models.Model):

    user = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name="projects"
    )

    title = models.CharField(max_length=200)

    description = models.TextField(
        blank=True
    )

    completed = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

class DailyReview(models.Model):

    user = models.ForeignKey(
    UserProfile,
    on_delete=models.CASCADE,
    related_name="reviews",
    null=True,
    blank=True
)
    
    day_rating = models.IntegerField()
    reflection = models.TextField()
    biggest_win = models.TextField()
    tomorrow_focus = models.TextField()
    completed = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Review #{self.id} - {self.created_at.strftime('%d %b %Y')}"
    streak = models.IntegerField(default=0)

last_review_date = models.DateField(
    null=True,
    blank=True
)
