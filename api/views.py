from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Form, FormSubmission
from rest_framework.renderers import JSONRenderer
from rest_framework.permissions import IsAuthenticated
from django.urls import reverse
from django.shortcuts import get_object_or_404

class CreateFormView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        form_name = request.data.get('name', 'Untitled Form')
        new_form = Form.objects.create(name=form_name, created_by=request.user)
        form_url = request.build_absolute_uri(reverse('submit-form', kwargs={'id': new_form.id}))
        return Response({'form_id': new_form.id, 'form_url': form_url}, status=status.HTTP_201_CREATED)

    

class FormSubmissionView(APIView):
    renderer_classes = [JSONRenderer]

    def post(self, request, id):
        form = get_object_or_404(Form, id=id)
        new_submission = FormSubmission.objects.create(form=form, data=request.data)
        return Response({"message": "Form submitted successfully"}, status=status.HTTP_201_CREATED)


class FormListView(APIView):
    
    def get(self, request, id):
        form = get_object_or_404(Form, id=id)
        submissions = form.submissions.all()

        if not submissions:
            return Response({"message": "No submissions yet for this form."}, status=status.HTTP_200_OK)

        submissions_data = [{"id": submission.id, "data": submission.data, "submitted_at": submission.submitted_at} for submission in submissions]
        
        return Response({
            "form_id": str(form.id),
            "form_name": form.name,
            "submissions_count": submissions.count(),
            "submissions": submissions_data
        }, status=status.HTTP_200_OK)
