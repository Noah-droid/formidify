from rest_framework import serializers
from .models import FormSubmission

class FormSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormSubmission
        fields = ['name', 'email', 'message']