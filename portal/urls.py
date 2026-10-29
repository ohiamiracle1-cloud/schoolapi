from django.urls import path
from . import views
from . import api_views

urlpatterns = [
    path('redirect/', views.role_redirect_view, name='role_redirect'),
    path('dashboard/admin/', views.admin_dashboard, name='admin_dashboard'),
    path('dashboard/teacher/', views.teacher_dashboard, name='teacher_dashboard'),
    path('dashboard/student/', views.student_dashboard, name='student_dashboard'),
    path('grades/record/<int:subject_id>/', views.record_grade, name='record_grade'),

    path('api/login/', api_views.CustomAuthToken.as_view(), name="api_login"),
    path('api/admin/stats/', api_views.AdminStatsAPIView.as_view(), name='api_admin_stats'),
    path('api/teacher/subject', api_views.TeacherSubjectAPIView.as_view(), name='api_teacher_subject'),
    path('api/teacher/grades/<int:subject_id>/', api_views.RecordGradeAPIView.as_view(),
    name='api_teacher_grades'),
    path('api/student/grades/', api_views.StudentGradesAPIView.as_view(),
    name='api_students_grade'),
    path('api/register/', api_views.RegisterAPIView.as_view(), name='api_register'),
]