from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from .models import Quiz, Question
import random

def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        name = request.POST.get("name")
        email = request.POST.get("email")
        password = request.POST.get("pass")
        confirm_password = request.POST.get("cpass")

        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect("register")  # Redirect back if passwords mismatch

        user = Quiz(
            name=name,
            username=username,
            email=email,
            password=password
        )
        user.save()

        messages.success(request, "Account created successfully! Please log in.")

    return render(request, "index.html")


def login_Page(request):
    if request.method == 'POST':
        username = request.POST.get('username').strip()  # Remove spaces
        password = request.POST.get('password')

        try:
            user = Quiz.objects.get(username=username)
            if password == user.password:  # Compare plain text password
                request.session['user_id'] = user.id  # Store user ID in session
                request.session['score'] = 0  # Initialize score for quiz
                request.session['asked_questions'] = []  # Reset question tracking

                messages.success(request, f'Welcome back, {user.name}!')
                return redirect("quiz")
            else:
                messages.error(request, 'Invalid password.')
        except Quiz.DoesNotExist:
            messages.error(request, 'User not found.')

    return render(request, 'login.html')


def quiz_view(request):
    if 'user_id' not in request.session:
        messages.error(request, "You must log in first.")
        return redirect("login")

    user_id = request.session['user_id']
    questions = list(Question.objects.all())

    if not questions:
        return HttpResponse("No questions available.")

    if 'asked_questions' not in request.session:
        request.session['asked_questions'] = []
        request.session['score'] = 0

    remaining_questions = [q for q in questions if q.id not in request.session['asked_questions']]

    if not remaining_questions:
        # Update user's final score in the database when quiz is completed
        final_score = request.session.get('score', 0)
        user = Quiz.objects.get(id=user_id)
        user.score = final_score
        user.save()

        request.session.flush()  # Clear session after quiz completion
        return render(request, 'Quiz_completed.html', {'score': final_score})

    question = random.choice(remaining_questions)
    request.session['asked_questions'].append(question.id)
    request.session.modified = True

    return render(request, 'Quiz.html', {'question': question})


def check_answer(request):
    if request.method == "POST":
        question_id = request.POST.get("question_id")
        selected_option = request.POST.get("selected_option")

        try:
            question = Question.objects.get(id=question_id)
        except Question.DoesNotExist:
            return redirect("quiz")

        if 'score' not in request.session:
            request.session['score'] = 0

        if selected_option == question.correct_option:
            request.session['score'] += 1

        request.session.modified = True
        return redirect("quiz")

    return redirect("quiz")

def leaderboard(request):
    top_users = Quiz.objects.order_by('-score')

    return render(request, 'Leaderboard.html', {'top_users': top_users})
