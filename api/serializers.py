from rest_framework import serializers
from .models import Form

class FormSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Form
        fields = ['data']