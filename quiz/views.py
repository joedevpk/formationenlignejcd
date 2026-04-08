# quiz/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Quiz, Question, Result
from math import ceil  # pour arrondir vers le haut


@login_required
def quiz_list(request):
    """
    Affiche tous les quiz disponibles
    """
    quizzes = Quiz.objects.all().order_by('-created_at')
    return render(request, 'quiz/quiz_list.html', {'quizzes': quizzes})


@login_required
def quiz_detail(request, quiz_id):
    """
    Affiche un quiz avec toutes ses questions
    """
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = quiz.questions.all()
    # Vérifier si l'utilisateur a déjà passé ce quiz
    try:
        result = Result.objects.get(user=request.user, quiz=quiz)
    except Result.DoesNotExist:
        result = None

    return render(request, 'quiz/quiz_detail.html', {
        'quiz': quiz,
        'questions': questions,
        'result': result,
    })


@login_required
def submit_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = quiz.questions.all()

    if Result.objects.filter(user=request.user, quiz=quiz).exists():
        return redirect('quiz_detail', quiz_id=quiz.id)

    score = 0
    total = questions.count()

    for question in questions:
        selected = request.POST.get(str(question.id))
        if selected and int(selected) == question.correct_choice:
            score += 1

    # Sauvegarde le résultat
    Result.objects.create(user=request.user, quiz=quiz, score=score)

    #  Calcul de la moitié pour le template
    half_total = total / 2

    return render(request, 'quiz/quiz_result.html', {
        'quiz': quiz,
        'score': score,
        'total': total,
        'half_total': half_total,  # <-- ajoute cette ligne
    })