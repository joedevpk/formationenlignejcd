from django.db import models
from django.conf import settings
from cloudinary.models import CloudinaryField

User = settings.AUTH_USER_MODEL



class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()

    image = CloudinaryField('image', blank=True, null=True)

    instructor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='courses'
    )

    is_premium = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title



class Lesson(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='lessons'
    )

    title = models.CharField(max_length=255)

    video = CloudinaryField(resource_type="video", blank=True, null=True)

    content = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)

    is_popular = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.course.title} - {self.title}"

    class Meta:
        ordering = ['order']   #  IMPORTANT (ordre automatique)


#  PROGRESSION VIDÉO

class LessonProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)

    # pourcentage (0 → 100)
    progress = models.IntegerField(default=0)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user} - {self.lesson} - {self.progress}%"

    class Meta:
        unique_together = ('user', 'lesson')  #  évite doublons


