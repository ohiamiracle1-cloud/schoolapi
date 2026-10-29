from django.db import models
from django.conf import settings

# Create your models here.

class AcademicsSession(models.Model):
    session = models.CharField(max_length=20)
    is_current = models.BooleanField(default=False)

    def __str__(self):
        return self.session
    

class ClassRoom(models.Model):
    name = models.CharField(max_length=20)
    class_teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,
     blank=True, limit_choices_to=
    {'role': 'TEACHER'}, related_name='assigned_classes')

    def __str__(self):
        return self.name


class Subject(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,
    blank=True, limit_choices_to= {'role': 'TEACHER'},
    related_name="subject_taught")

    def __str__(self):
        return f"{self.name} ({self.code})"


class Grade(models.Model):
    student = models.ForeignKey('accounts.StudentProfile', on_delete=models.CASCADE,
    related_name= 'grades')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='grade')
    session = models.ForeignKey(AcademicsSession, on_delete=models.CASCADE)
    continuous_assessment = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    exam_score= models.DecimalField(max_digits=5, decimal_places=2, default=0.00)


    class Meta:
        unique_together = ('student', 'subject', 'session')

    @property
    def total_score(self):
        return self.continuous_assessment + self.exam_score

    def __str__(self):
        return f"{self.student} - {self.Subject}: {self.total_score}"

