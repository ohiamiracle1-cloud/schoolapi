from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .decorators import role_required
from accounts.models import User, TeacherProfile, StudentProfile
from academics.models import AcademicsSession, ClassRoom, Subject, Grade

# Create your views here.

@login_required
def role_redirect_view(request):
    """"Direct users to them specific dashboard based on their assigned role"""

    if request.user.role == User.Role.ADMIN or request.user.is_superuser:
        return redirect('admin_dashboard')
    elif request.user.role == User.Role.TEACHER:
        return redirect('teacher_dashboard')
    elif request.user.role == User.Role.STUDENT:
        return redirect('student_dashboard')
    else:
        return redirect('login')


@role_required(allowed_roles=['ADMIN'])
def admin_dashboard(request):
    context = {
        'total_teacher': User.objects.filter(role= User.Role.TEACHER).
        count(),
        'total_students': User.objects.filter(role= User.Role.STUDENT).
        count(),
        'total_subjects': Subject.objects.count(),
        'totla_classes': ClassRoom.objects.count(),
    }
    return render(request, 'portal/admin_dashboard.html', context)


@role_required(allowed_roles=['TEACHER'])
def teacher_dashboard(request):
    taught_subjects = Subject.objects.filter(teacher=request.user)
    assigned_classes = ClassRoom.objects.filter(class_teacher=request.user)
    context ={
        'subjest': taught_subjects,
        'classes': assigned_classes,
    }
    return render(request, 'portal/teacher_dashboard.html', context)


@role_required(allowed_roles=['TEACHER'])
def record_grade(request, subject_id):
    Subject = get_object_or_404(subject, id=subject_id, teacher=request.user)
    current_session = AcademicsSession.objects.filter(is_current = True). first()
    students = StudentProfile.object.all()

    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        ca = request.POST.get('ca', 0)
        exam = request.POST.get('exam', 0)
        student = get_object_or_404(StudentProfile, id=student_id)
        Grade.objects.update_or_or_create(
            student=student, subject=subject, session=current_session,
            defaults={'continuous_assessment': ca, 'exam_score':exam}
        )
        return redirect('teacher_dashboard')
    return render(request, 'portal/record_grade.html',{
        'subject': subject, 'students': students, 'session':current_session
    })


@role_required(allowed_roles=['STUDENT'])
def student_dashboard(request):
    profile = get_object_or_404(StudentProfile, user=request.user)
    grades = Grade.objects.filtler(student=profile).select_related
    ('subject', 'session')
    context = {
        'profile': profile,
        'grades': grades,
    }
    return render(request, 'portal/student_dashboard.html', context)