from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_page, name='login'),
    path('register/', views.register_page, name='register'),
    path('dashboard/', views.dashboard_page, name='dashboard'),
    path('review/', views.daily_review, name='daily_review'),
    path('goal/', views.add_goal, name='add_goal'),
    path("project/", views.add_project, name="add_project"),
    path('goal/<int:goal_id>/complete/', views.complete_goal, name='complete_goal'),
    path('logout/', views.logout_page, name='logout'),
    path(
    "project/<int:project_id>/complete/",
    views.complete_project,
    name="complete_project"
),
]