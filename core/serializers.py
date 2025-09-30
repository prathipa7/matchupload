from rest_framework import serializers
from .models import ResumeUpload, JobListing


class ResumeUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResumeUpload
        fields = [
            "id",
            "user",
            "original_filename",
            "file",
            "extracted_text",
            "parsed_skills",
            "analysis_summary",
            "uploaded_at",
        ]


class JobListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobListing
        fields = "__all__"
