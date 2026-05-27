from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render,redirect
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.http import HttpResponse
import sqlite3
import datetime
import time
from google import genai
import json, random

def loadexamination(request):
    with open('questions.json') as f:
        questions = json.load(f)

    if request.method == "POST":
        random_questions = request.session.get('exam_questions', [])

        score = 0
        total = len(random_questions)*10

        for i, q in enumerate(random_questions):
            user_answer = request.POST.get(f"q{i+1}")
            correct_answer = q["answer"]

            if user_answer == correct_answer:
                score += 10

        return render(request, "result.html", {
            "score": score,
            "total": total
        })

    # GET request
    random_questions = random.sample(questions, 5)
    request.session['exam_questions'] = random_questions

    return render(request, "examination.html", {"questions": random_questions})

def home(request):
    return render(request, 'homepage.html')

def loadsignup(request):
    return render(request, 'signuppage.html')

def loadlogin(request):
    return render(request, 'loginpage.html')

def loadstarttest(request):
    return render(request, 'starttestpage.html')

@never_cache
def loaddashboard(request):
    if 'username' not in request.session:
        return redirect('login')

    return render(request, 'dashboard.html', {
        "username": request.session['username']
    })


def signup_action(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        fullname = request.POST['fullname']
        universityname = request.POST['uniname']
        mobileno = request.POST['mobileno']
        email = request.POST['email']

        con = sqlite3.connect(settings.DATABASES['default']['NAME'])
        sql = "insert into signup (username, password, fullname, universityname, mobileno, email) values(?,?,?,?,?,?)"
        values = (username, password, fullname, universityname,mobileno, email)
        con.execute(sql, values)
        con.commit()
        con.close()
        messages.success(request, "Account created successfully!")

    return render(request, 'homepage.html')

def login_action(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        con = sqlite3.connect(settings.DATABASES['default']['NAME'])
        cursor = con.cursor()

        sql = "SELECT * FROM signup WHERE username = ? AND password = ?"
        cursor.execute(sql, (username, password))
        user = cursor.fetchone()
        con.close()

        if user:
            # ✅ Create session
            request.session['username'] = username
            request.session.set_expiry(0)  # expires on browser close

            return redirect("dashboard")

        else:
            return render(request, "loginpage.html", {
                "message": "Invalid username or password"
            })

    return redirect("login")

def logout_action(request):
    request.session.flush()
    return redirect('login')

