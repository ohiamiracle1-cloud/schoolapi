from django.contrib import admin
from .models import User, TeacherProfile, StudentProfile
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Register your models here.

class TeacherProfileInline(admin.StackedInline):
    model = TeacherProfile
    can_delete = False

class StudentProfileInline(admin.StackedInline):
    model = StudentProfile
    can_delete = False

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Role & Profile info', {'fields': ('role', 'phone_number')}),
    )
    list_display = ('username', 'email', 'role', 'is_staff')
    list_filter = ('role', 'is_staff', 'is_active')


admin.site.register(TeacherProfile)
admin.site.register(StudentProfile)