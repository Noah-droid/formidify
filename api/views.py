from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Form
from rest_framework.renderers import JSONRenderer
from rest_framework.permissions import IsAuthenticated
from django.urls import reverse
from django.shortcuts import get_object_or_404

class CreateFormView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        new_form = Form.objects.create()
        form_url = request.build_absolute_uri(reverse('submit-form', kwargs={'unique_id': new_form.unique_id}))
        return Response({'form_url': form_url}, status=status.HTTP_201_CREATED)
    

class FormSubmissionView(APIView):
    renderer_classes = [JSONRenderer]

    def post(self, request, unique_id):
        form = get_object_or_404(Form, unique_id=unique_id)
        
        new_submission = request.data
        
        if form.data:
            if isinstance(form.data, list):
                form.data.append(new_submission)
            else:
                form.data = [form.data, new_submission]
        else:
            form.data = [new_submission]
        
        form.save()
        return Response({"message": "Form submitted successfully"}, status=status.HTTP_201_CREATED)

class FormListView(APIView):
    def get(self, request, unique_id):
        form = get_object_or_404(Form, unique_id=unique_id)
        
        # Check if there are any submissions
        if not form.data:
            return Response({"message": "No submissions yet for this form."}, status=status.HTTP_200_OK)
        
        # If the data is a list of submissions
        if isinstance(form.data, list):
            submissions = form.data
        else:
            # If it's a single submission, wrap it in a list
            submissions = [form.data]
        
        return Response({
            "form_id": str(form.unique_id),
            "submissions_count": len(submissions),
            "submissions": submissions
        }, status=status.HTTP_200_OK)