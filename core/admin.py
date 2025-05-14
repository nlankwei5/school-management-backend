from django.contrib import admin
from .models import Student, Teacher, Attendance, Grade, TeacherGradeAssignment


class GradeAssignmentAdmin (admin.ModelAdmin):
    pass

admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Grade)
admin.site.register(Attendance)
admin.site.register(TeacherGradeAssignment, GradeAssignmentAdmin)

