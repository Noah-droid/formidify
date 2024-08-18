from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Form, FormSubmission
from rest_framework.renderers import JSONRenderer
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.core.mail import send_mail, EmailMessage

import json


class CreateFormView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        form_name = request.data.get('name', 'Untitled Form')
        new_form = Form.objects.create(name=form_name, created_by=request.user)
        form_url = request.build_absolute_uri(reverse('submit-form', kwargs={'id': new_form.id}))
        return Response({'form_id': new_form.id, 'form_url': form_url}, status=status.HTTP_201_CREATED)


class FormSubmissionView(APIView):
    permission_classes = [AllowAny]
    renderer_classes = [JSONRenderer]

    def post(self, request, id):
        form = get_object_or_404(Form, id=id)
        form_data = request.data
        new_submission = FormSubmission.objects.create(form=form, data=form_data)

        # Format the form data as a JSON string or a human-readable string
        formatted_data = json.dumps(form_data, indent=4)  # JSON format
        # Alternatively, create a string for human readability:
        readable_data = "\n".join([f"{key}: {value}" for key, value in form_data.items()])

        # Email details
        subject = "New Form Submission"
        message = (
            f"A new submission has been made for the form '{form.name}'.\n\n"
            f"Form Data:\n{formatted_data}"  # or use readable_data if you prefer
        )
        from_email = settings.DEFAULT_FROM_EMAIL
        to_emails = [settings.ADMIN_EMAIL_1]  # Primary recipients
        # cc_emails = [settings.ADMIN_EMAIL_2]  # CC recipients

        # Create and send the email
        email = EmailMessage(
            subject=subject,
            body=message,
            from_email=from_email,
            to=to_emails,
            # cc=cc_emails,
        )
        email.send(fail_silently=False)

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
