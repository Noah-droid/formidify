from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import FormSubmissionSerializer
from rest_framework.renderers import JSONRenderer

class FormSubmissionView(APIView):
    renderer_classes = [JSONRenderer]  # This ensures JSON is always returned

    def post(self, request, format=None):
        serializer = FormSubmissionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Form submitted successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)