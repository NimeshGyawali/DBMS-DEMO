from django.db import models

class Student(models.Model):
    roll_no = models.IntegerField(unique=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    phone_no = models.CharField(max_length=15)
    
    def __str__(self):
        return self.name



