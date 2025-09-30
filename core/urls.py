from django.urls import path
from .views import ResumeUploadView, JobListView, frontend
from . import views
from .views import ResumeUploadView, JobListView

urlpatterns = [
    path("", views.login_view, name="login"),   # first page = login
    path("home/", views.home, name="home"),
    path("logout/", views.logout_view, name="logout"),

    path("api/upload_resume/", ResumeUploadView.as_view(), name="upload_resume"),
    path("api/jobs/", JobListView.as_view(), name="job_list"),
    path("", frontend, name="frontend"),
    path("about/", views.about_view, name="about"),
    path("userdata/", views.userdata_view, name="userdata"),

    # API endpoints
    path("api/upload_resume/", ResumeUploadView.as_view(), name="upload_resume"),
    path("api/jobs/", JobListView.as_view(), name="job_list"),
]
