from django.db import models
from django.db.models.fields import EmailField

# Create your models here.
class Interviewer(models.Model):
    Email = models.EmailField(primary_key=True)
    Name = models.CharField(max_length=100)
    def __str__(self):
        return str(self.Email)

class Candidate(models.Model):
    Email = models.EmailField(primary_key=True)
    Name = models.CharField(max_length=100)
    def __str__(self):
        return str(self.Email)


class InterviewSchedule(models.Model):
    Id=models.AutoField(primary_key=True)
    Interviewer_Email = models.ForeignKey(Interviewer,on_delete=models.CASCADE)
    Candidate_Email = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    Start_Date_time = models.DateTimeField()
    End_Date_time = models.DateTimeField()
    def __str__(self):
        return str(self.Id)