from django.contrib import admin
from .models import Quiz, Question, Result

class QuestionInline(admin.TabularInline):
    model = Question
    extra = 4  # propose 4 questions par défaut dans l'admin

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    inlines = [QuestionInline]

@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ('user', 'quiz', 'score', 'taken_at')