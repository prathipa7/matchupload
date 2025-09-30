from django.contrib import admin
from .models import ResumeUpload, JobListing

@admin.register(ResumeUpload)
class ResumeUploadAdmin(admin.ModelAdmin):
    list_display = ("id", "original_filename", "user")
    search_fields = ("original_filename", "extracted_text")

@admin.register(JobListing)
class JobListingAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "company", "location")
    search_fields = ("title", "company", "location")
    list_filter = ("location",)
