from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Course
from .utils import user_has_access
from .models import Course, Lesson, LessonProgress
from subscriptions.utils import user_has_access
from django.utils import timezone
from django.db.models import Avg, Count
from reviews.models import Review
from django.http import JsonResponse
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from courses.models import Course
from quiz.models import Quiz, Result


User = get_user_model()


# =========================
# DASHBOARD FORMATEUR
# =========================
@login_required
def instructor_dashboard(request):
    courses = Course.objects.filter(instructor=request.user)
    return render(request, 'dashboard/instructor_dashboard.html', {'courses': courses})


# =========================
# AJOUTER UN COURS
# =========================
@login_required
def add_course(request):
    if not getattr(request.user, 'is_instructor', False):
        return redirect('dashboard_redirect')

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        is_premium = request.POST.get('is_premium') == 'True'
        image = request.FILES.get('image')  # facultatif

        if title and description:
            Course.objects.create(
                title=title,
                description=description,
                is_premium=is_premium,
                image=image,
                instructor=request.user
            )
            messages.success(request, f"Le cours '{title}' a été ajouté avec succès !")
        else:
            messages.error(request, "Veuillez remplir tous les champs obligatoires.")

    return redirect('instructor_dashboard')


# =========================
# MODIFIER UN COURS
# =========================
@login_required
def edit_course(request, course_id):
    course = get_object_or_404(Course, id=course_id, instructor=request.user)

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        is_premium = request.POST.get('is_premium') == 'True'
        image = request.FILES.get('image')

        if title and description:
            course.title = title
            course.description = description
            course.is_premium = is_premium
            if image:
                course.image = image
            course.save()
            messages.success(request, f"Le cours '{title}' a été mis à jour !")
            return redirect('instructor_dashboard')
        else:
            messages.error(request, "Veuillez remplir tous les champs obligatoires.")

    return render(request, 'dashboard/edit_course.html', {'course': course})


# =========================
# SUPPRIMER UN COURS
# =========================
@login_required
def delete_course(request, course_id):
    course = get_object_or_404(Course, id=course_id, instructor=request.user)
    if request.method == 'POST':
        course.delete()
        messages.success(request, f"Le cours '{course.title}' a été supprimé !")
        return redirect('instructor_dashboard')

    return render(request, 'dashboard/delete_course.html', {'course': course})



def home(request):
    #  Top 6 cours selon la note moyenne
    courses = Course.objects.annotate(
        avg_rating=Avg('reviews__rating'),
        total_reviews=Count('reviews')
    ).order_by('-avg_rating')[:6]

    #  Quiz populaire pour la Home
    popular_quiz = Quiz.objects.order_by('-id').first()  # le plus récent ou le plus joué
    # Top score pour le badge
    top_result = Result.objects.filter(quiz=popular_quiz).order_by('-score').first() if popular_quiz else None
    top_score = f"{top_result.user.username} : {top_result.score}" if top_result else None

    return render(request, 'courses/home.html', {
        'courses': courses,
        'popular_quiz': popular_quiz,
        'top_quiz_score': top_score,
    })



#  PAGE DETAIL COURS + REVIEWS (VERSION PRO)
@login_required
def course_detail(request, id):

    #  Récupérer cours ou erreur 404
    course = get_object_or_404(Course, id=id)

    #  Vérifier accès abonnement
    from courses.utils import user_has_access
    has_access = user_has_access(request.user, course)


    #  Optimisation (évite trop de requêtes DB)
    reviews = Review.objects.filter(course=course)\
        .select_related('user')\
        .prefetch_related('likes')\
        .order_by('-created_at')

    #  Moyenne des notes
    avg_data = reviews.aggregate(avg=Avg('rating'))
    average = round(avg_data['avg'], 1) if avg_data['avg'] else 0

    #  Vérifier si utilisateur a déjà review
    user_review = reviews.filter(user=request.user).first()

    #  Top reviewers (optimisé)
    top_reviewers = User.objects.annotate(
        total_reviews=Count('review')
    ).filter(total_reviews__gt=0).order_by('-total_reviews')[:5]

    #  TRI DES AVIS
    sort = request.GET.get('sort')

    if sort == 'top':
        reviews = reviews.annotate(
            total_likes=Count('likes')
        ).order_by('-total_likes', '-created_at')

    elif sort == 'old':
        reviews = reviews.order_by('created_at')

    #  AJOUT REVIEW (POST)
    if request.method == "POST":

        #  Bloquer double review
        if user_review:
            messages.warning(request, "Vous avez déjà laissé un avis.")
            return redirect('course_detail', id=course.id)

        rating = request.POST.get('rating')
        comment = request.POST.get('comment')

        #  VALIDATION
        try:
            rating = int(rating)

            if rating < 1 or rating > 5:
                raise ValidationError("Note invalide")

            if not comment or len(comment.strip()) < 3:
                raise ValidationError("Commentaire trop court")

        except Exception:
            messages.error(request, "Erreur dans le formulaire.")
            return redirect('course_detail', id=course.id)

        #  Création review
        Review.objects.create(
            user=request.user,
            course=course,
            rating=rating,
            comment=comment.strip()
        )

        messages.success(request, "Avis ajouté avec succès !")

        return redirect('course_detail', id=course.id)

    #  CONTEXT FINAL
    context = {
        'course': course,
        'has_access': has_access,
        'reviews': reviews,
        'average': average,
        'user_review': user_review,
        'top_reviewers': top_reviewers,
        'total_reviews': reviews.count()
    }

    return render(request, 'courses/course_detail.html', context)
