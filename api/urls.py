from django.urls import path
from .views import FormSubmissionView

urlpatterns = [
    path('submit/', FormSubmissionView.as_view(), name='form-submission'),
]