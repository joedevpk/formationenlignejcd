from django.db import models
from django.conf import settings
from courses.models import Course

User = settings.AUTH_USER_MODEL

class Review(models.Model):
    # utilisateur qui laisse l'avis
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # cours concerné
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="reviews")

    # note de 1 à 5
    rating = models.IntegerField()

    # commentaire
    comment = models.TextField()

    likes = models.ManyToManyField(User, related_name='liked_reviews', blank=True)

    # date
    created_at = models.DateTimeField(auto_now_add=True)

    #  Empêche double review
    class Meta:
        unique_together = ('user', 'course')


    def __str__(self):
        return f"{self.user} - {self.course} ({self.rating})"
    