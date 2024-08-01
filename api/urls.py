from django.urls import path
from .views import CreateFormView, FormSubmissionView, FormListView

urlpatterns = [
    path('create-form/', CreateFormView.as_view(), name='create-form'),
    path('submit/<uuid:unique_id>/', FormSubmissionView.as_view(), name='submit-form'),
    path('submissions/<uuid:unique_id>/', FormListView.as_view(), name='form-submissions'),
]