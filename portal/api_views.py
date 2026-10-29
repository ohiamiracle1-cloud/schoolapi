from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from accounts.models import User, StudentProfile
from academics.models import Subject, Grade, AcademicsSession
from .serializers import GradeSerializer, RegisterSerializer, SubjectSerializer, StudentProfileSerializer
from .permissions import IsAdminUserRole, IsTeacherUserRole, IsStudentUserRole
from rest_framework.generics import CreateAPIView


class CustomAuthToken(ObtainAuthToken):
    #Generate an auth token and returns a user detail and role
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context=
        {'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.object.get_or_create(user=user)
        return Response({'token': token.key, 'user_id': user.pk,
        'username': user.username, 'role': user.role})

class AdminStatsAPIView(APIView):
    permission_classes = [IsAdminUserRole]

    def get(self, request):
        return Response({'total_teachers': User.objects.filter(role=User.
        Role.TEACHER).count(), 'total_students': User.objects.filter
        (role=User.Role.STUDENT).count(), 'total_subjects': Subject.
        objects.count(),})

class TeacherSubjectAPIView(APIView):
    permisssion_classes = [IsTeacherUserRole]

    def get(self, request):
        subjects = Subject.objects.filter(teacher=request.user)
        serializer = SubjectSerializer(subjects, many=True)
        return Response(serializer.data)


class RecordGradeAPIView(APIView):
    permission_classes = [IsTeacherUserRole]

    def post(self, request, subject_id):
        current_session = AcademicsSession.objects.filter(is_current=True).first()
        if not current_session:
            return Response({'error': 'No active academic session found'},
            status=status.HTTP_400_BAD_REQUEST)
        data = request.data.copy
        data['subject'] = subject_id
        data['session'] = current_session.id

        student_id = data.get('student')
        existing_grade = Grade.objects.filter(student_id=student_id,
        subject_id=subject_id, session=current_session).first()

        if existing_grade:
            serilizer = GradeSerializer(existing_grade, data=data,
            partial=True)
        else:
            serializer = GradeSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.
            HTTP_201_CREATED)
        return Response(serializer.errors, status=status.
        HTTP_400_BAD_REQUEST)

class StudentGradesAPIView(APIView):
    permission_classes = [IsStudentUserRole]

    def get(self, request):
        try:
            profile =request.user.student_profile
        except StudentProfile.DoesNotExist:
            return Response({'error': 'student profile not found'},
            status=status.HTTP_404_NOT_FOUND)
        grades =Grade.objects.filter(student=profile).select_related
        ('subject', 'session')
        serializer = GradeSerializer(grades, many=True)
        return Response(serializer.data)

class RegisterAPIView(CreateAPIView):
    '''Oublic student signup; the front end still directs the users to login'''
    #authentication_classes = []
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            'message': 'User registered successfully.',
            'token': token.key,
            'user':{
                'id':user.id,
                'username':user.username,
                'role':user.role,
                'email':user.email
            }
        }, status=status.HTTP_201_CREATED)