from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    PROF_CHOICES = (
        ('Developer', 'Developer'),
        ('Social Media Manager', 'Social Media Manager'),
        ('Analyst', 'Analyst'),
        ('Others', 'Others')

    )


    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=240, default='')
   
    profession = models.CharField(max_length=50, default='', choices=PROF_CHOICES)
    
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} -  {self.created_on}"
