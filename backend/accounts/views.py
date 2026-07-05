from datetime import datetime,timedelta
from django.utils import timezone
from .models import UserProfile, DailyReview, Goal, Project
from django.shortcuts import render, redirect
from .raven import get_raven_message
from .models import UserProfile, DailyReview, Goal


def home(request):
    return redirect("dashboard")


def login_page(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = UserProfile.objects.filter(
            username=username,
            password=password
        ).first()

        if user:
            request.session["username"] = user.username
            return redirect("dashboard")

    return render(request, "login.html")


def register_page(request):
    if request.method == "POST":
        UserProfile.objects.create(
            username=request.POST.get("username"),
            email=request.POST.get("email"),
            password=request.POST.get("password"),
        )

        return redirect("login")

    return render(request, "register.html")

def dashboard_page(request):

    username = request.session.get("username")

    if not username:
        return redirect("login")

    hour = datetime.now().hour

    if 5 <= hour < 12:
        greeting = "Good Morning"
    elif 12 <= hour < 17:
        greeting = "Good Afternoon"
    elif 17 <= hour < 22:
        greeting = "Good Evening"
    else:
        greeting = "Burning the midnight oil"

    user = UserProfile.objects.get(username=username)

    goals = Goal.objects.filter(
        user=user,
        completed=False
    ).order_by("-created_at")

    completed_goals = Goal.objects.filter(
        user=user,
        completed=True
    ).count()

    forged_goals = Goal.objects.filter(
        user=user,
        completed=True
    ).order_by("-created_at")

    reviews = DailyReview.objects.filter(
        user=user
    ).count()

    projects = Project.objects.filter(
        user=user,
        completed=False
    ).order_by("-created_at")

    completed_projects = Project.objects.filter(
        user=user,
        completed=True
    ).order_by("-created_at")

    project_count = Project.objects.filter(
        user=user
    ).count()

    today = timezone.localdate()

    review_completed = DailyReview.objects.filter(
        user=user,
        created_at__date=today
    ).exists()
    raven_title, raven_message = get_raven_message(
    user=user,
    active_goals=goals,
    completed_goals=forged_goals,
    active_projects=projects,
    review_completed=review_completed,
)

    return render(
        request,
        "dashboard.html",
        {
            "username": username,
            "greeting": greeting,
            "goals": goals,
            "completed_goals": completed_goals,
            "forged_goals": forged_goals,
            "review_count": reviews,
            "projects": projects,
            "completed_projects": completed_projects,
            "project_count": project_count,
            "review_completed": review_completed,
            "streak": user.streak,
            "raven_title": raven_title,
            "raven_message": raven_message,
           
        },
    )


def add_goal(request):

    if request.method == "POST":

        username = request.session.get("username")
        user = UserProfile.objects.get(username=username)

        Goal.objects.create(
            user=user,
            title=request.POST.get("title")
        )

        return redirect("dashboard")

    return render(request, "goal.html")
from datetime import timedelta

def add_project(request):

    username = request.session.get("username")

    if not username:
        return redirect("login")

    user = UserProfile.objects.get(username=username)

    if request.method == "POST":

        Project.objects.create(
            user=user,
            title=request.POST.get("title"),
            description=request.POST.get("description"),
        )

        return redirect("dashboard")

    return render(request, "project.html")


def update_streak(user):
    today = timezone.localdate()

    # First review ever
    if user.last_review_date is None:
        user.streak = 1

    # Consecutive day
    elif user.last_review_date == today - timedelta(days=1):
        user.streak += 1

    # Same day (don't increment again)
    elif user.last_review_date == today:
        return

    # Missed one or more days
    else:
        user.streak = 1

    user.last_review_date = today
    user.save()


def daily_review(request):

    username = request.session.get("username")

    if not username:
        return redirect("login")

    user = UserProfile.objects.get(username=username)

    today = timezone.localdate()

    # Prevent duplicate reviews on the same day
    if DailyReview.objects.filter(
        user=user,
        created_at__date=today
    ).exists():
        return redirect("dashboard")

    if request.method == "POST":

        DailyReview.objects.create(
            user=user,
            day_rating=request.POST.get("day_rating"),
            reflection=request.POST.get("reflection"),
            biggest_win=request.POST.get("biggest_win"),
            tomorrow_focus=request.POST.get("tomorrow_focus"),
        )

        update_streak(user)

        return redirect("dashboard")

    return render(request, "review.html")

def logout_page(request):
    request.session.flush()
    return redirect("login")
def complete_goal(request, goal_id):

    goal = Goal.objects.get(id=goal_id)

    goal.completed = True

    goal.save()

    return redirect("dashboard")

def complete_project(request, project_id):

    username = request.session.get("username")

    if not username:
        return redirect("login")

    user = UserProfile.objects.get(username=username)

    project = Project.objects.get(
        id=project_id,
        user=user
    )

    project.completed = True
    project.save()

    return redirect("dashboard")