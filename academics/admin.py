from django.contrib import admin
from .models import AcademicsSession, ClassRoom, Subject, Grade

# Register your models here.

admin.site.register(AcademicsSession)
admin.site.register(ClassRoom)
admin.site.register(Subject)

@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ('student', 'subject', 'session',
    'continuous_assessment', 'exam_score', 'total_score')
    list_filter = ('session', 'subject')
