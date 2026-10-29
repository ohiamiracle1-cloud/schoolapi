from rest_framework import serializers
from accounts.models import User, StudentProfile, TeacherProfile
from academics.models import AcademicsSession, ClassRoom, Subject, Grade

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role','phone_number']

class StudentProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class_name = serializers.StringRelatedField(source='current_class.name', read_only=True)

    class Meta:
        model = StudentProfile
        fields = ['id', 'user', 'class_name', 'admission_number','date_of_birth', 'class_name']

class SubjectSerializer(serializers.ModelSerializer):
    teacher_name = serializers.CharField(source='teacher.username', read_only=True)

    class Meta:
        model = Subject
        fields = ['id', 'name', 'code', 'teacher_name', 'teacher']

class GradeSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.user.get_full_name', read_only=True)
    subject_name = serializers.CharField(source='subject.name', read_only=True)
    
    class Meta:
        model = Grade
        fields = ['id', 'student_name', 'subject_name', 'session', 'continous_assessment', 'exam_score', 'total_score']

    def get_total_score(self, obj):
        return obj.total_score()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    admission_number = serializers.CharField(
        write_only=True, required=False, allow_blank=True
    )
    employee_id = serializers.CharField(
        write_only=True, required=False, allow_blank=True
    )

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'password', 'first_name',
            'last_name', 'role', 'phone_number', 'admission_number',
            'employee_id'
        ]