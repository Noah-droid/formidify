from django.urls import path
from .views import CreateFormView, FormSubmissionView, FormListView

urlpatterns = [
    path('create-form/', CreateFormView.as_view(), name='create-form'),
    path('submit-form/<uuid:id>/', FormSubmissionView.as_view(), name='submit-form'),
    path('form-submissions/<uuid:id>/', FormListView.as_view(), name='form-submissions'),
]
