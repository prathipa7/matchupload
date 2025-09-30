import os
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions, generics
from django.conf import settings
from .serializers import ResumeUploadSerializer, JobListingSerializer
from .models import ResumeUpload, JobListing
from .utils.resume_parser import analyze_resume
from .utils.matching import match_jobs
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")  # not checked, just taken

        if username and password:  
            request.session["username"] = username  # save in session
            return redirect("home")
        else:
            messages.error(request, "Please enter both username and password")

    return render(request, "login.html")

def logout_view(request):
    request.session.flush()  # clear session
    return redirect("login")

def home(request):
    username = request.session.get("username")  # fetch from session
    if not username:
        return redirect("login")  # force login if not set
    return render(request, "index.html", {"username": username})


def about_view(request):
    return render(request, "about.html")

def userdata_view(request):
    return render(request, "userdata.html")


class ResumeUploadView(APIView):


    """
    Upload a resume (PDF or image), extract skills,
    analyze content, and match to available jobs.
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        file_obj = request.FILES.get("file")
        location = request.POST.get("location", "")
    

        if not file_obj:
            return Response({"error": "No file uploaded"}, status=status.HTTP_400_BAD_REQUEST)

        # Save uploaded file into DB
        resume = ResumeUpload.objects.create(
            user=request.user if request.user.is_authenticated else None,
            original_filename=file_obj.name,
            file=file_obj
        )
        try:
            if file_obj.name.lower().endswith(".pdf"):
                analysis = analyze_resume(file_path=resume.file.path)
            else:
                # Image formats like JPG, PNG
                analysis = analyze_resume(file_stream=resume.file, filename=file_obj.name)
        except Exception as e:
            return Response(
                {"error": f"Resume analysis failed: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        
        
        resume.extracted_text = analysis["extracted_text"]
        resume.parsed_skills = analysis["parsed_skills"]
        resume.analysis_summary = str(analysis["analysis_summary"])
        resume.save()

        # Match jobs
        matched_jobs = match_jobs(resume.parsed_skills)

        # Use serializer to format resume data
        serialized_resume = ResumeUploadSerializer(resume).data

        return Response({
            "message": "Resume uploaded and analyzed successfully",
            "resume": serialized_resume,
            "matched_jobs": matched_jobs
        }, status=status.HTTP_201_CREATED)


class JobListView(generics.ListAPIView):
    """
    List all job postings (for testing/debugging).
    """
    queryset = JobListing.objects.all().order_by('-posted_at')
    serializer_class = JobListingSerializer



def frontend(request):
    """
    Serve the frontend index.html page.
    """
    return render(request, "index.html")
