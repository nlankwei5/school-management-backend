from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.utils import timezone

class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifier
    for authentication instead of usernames.
    """
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        return self.create_user(email, username, password, **extra_fields)


class CustomUser (AbstractBaseUser, PermissionsMixin):
    user_id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False) 
    is_superuser = models.BooleanField(default=False) 
    date_joined = models.DateTimeField(default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return f"{self.username} ({self.email})"


class Grade(models.Model):
    Grade_id = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=30)
    Level = models.CharField(max_length=20)
    academic_year = models.CharField(max_length=9)

    def __str__(self):
        return f"{self.Name} - {self.academic_year}"
    


class Student(models.Model):
    student = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='student-profile+')
    grade = models.ForeignKey(Grade, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Student: {self.student.username}"

class Teacher(models.Model):
    teacher = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='teacher-profile+')
    department = models.CharField(max_length=20)
    contact = models.CharField(max_length=10)
    grade = models.ForeignKey(Grade, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Teacher: {self.teacher.username} ({self.department})"
    
class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=10)
    recorded_by = models.ForeignKey(Teacher, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('student', 'date')
    
    def __str__(self):
        return f"{self.student.student.username} - {self.date} - {self.status}"

class TeacherGradeAssignment(models.Model):
    teacher_to_be_assigned= models.ForeignKey(Teacher, on_delete=models.CASCADE)
    grade_to_be_assigned_to = models.ForeignKey(Grade, on_delete=models.CASCADE)
    role_type = models.CharField(max_length=20)
    subject = models.CharField(max_length=20)

    class Meta:
        unique_together = ('teacher_to_be_assigned', 'grade_to_be_assigned_to', 'subject')
        
    def __str__(self):
        return f"{self.teacher_to_be_assigned.teacher.username} - {self.grade_to_be_assigned_to.Name} - {self.subject}"


