from rest_framework import serializers
from .models import Student, Teacher, Grade, Attendance


class StudentSerializer(serializers.ModelSerializer):
    student_username = serializers.CharField(source ="student.username", read_only=True)
    student_email  = serializers.EmailField(source ="student.email", read_only=True)
    student_firstname  = serializers.CharField(source ="student.first_name", read_only=True)
    student_lastname  = serializers.CharField(source ="student.last_name", read_only=True)
    student_grade  = serializers.CharField(source ="grade.name", read_only=True)
    
    class Meta: 
        model = Student
        fields = ["student", "student_username","student_firstname","student_lastname","student_email","Student_grade"]

class TeacherSerializer(serializers.ModelSerializer):
    teacher_username = serializers.CharField(source ="teacher.username", read_only=True)
    teacher_email  = serializers.EmailField(source ="teacher.email", read_only=True)
    teacher_firstname  = serializers.CharField(source ="teacher.first_name", read_only=True)
    teacher_lastname  = serializers.CharField(source ="teacher.last_name", read_only=True)
    teacher_grade  = serializers.CharField(source ="grade.name", read_only=True)
    
    
    class Meta: 
        model = Teacher
        fields = ["teacher", "teacher_username","teacher_firstname","teacher_lastname","teacher_email", "teacher_grade"]


class GradeSerializer(serializers.ModelSerializer):
    assigned_teacher = serializers.SerializerMethodField()
    class Meta:
        model = Grade
        fields = ["grade_id", "name", "level", "academic_year", "assigned_teacher"]

    def get_assigned_teacher(self, obj):
        teacher = obj.assigned_teacher
        if teacher:
            return {
                "id": teacher.id,
                "name": teacher.teacher.name,  
                "email": teacher.teacher.email,
            }
        return None
    
class AttendanceSerializer(serializers.ModelSerializer):
    student_firstname  = serializers.CharField(source ="student.student.first_name", read_only=True)
    student_lastname  = serializers.CharField(source ="student.student.last_name", read_only=True)

    class Meta: 
        model = Attendance 
        fields= ["student_firstname","student_lastname", "status"]