from django.contrib import admin
from .models import Course, Lesson


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'instructor', 'is_premium', 'created_at')
    list_filter = ('is_premium', 'created_at')
    search_fields = ('title', 'description', 'instructor__username')


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'order', 'is_popular')
    list_filter = ('course', 'is_popular')
    search_fields = ('title', 'course__title')
    