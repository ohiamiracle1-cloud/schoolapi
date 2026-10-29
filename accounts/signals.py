from django.db.models.signals import post_save
from django.dispatch import receiver
from.models import User, TeacherProfile, StudentProfile

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.role == User.Role.TEACHER:
            TeacherProfile.objects.create(user=instance)
        elif instance.role == User.Role.STUDENT:
            StudentProfile.objects.create(user=instance)