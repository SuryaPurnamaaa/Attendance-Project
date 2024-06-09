from django.shortcuts import render
from FacultyView.models import Student
from django.http import HttpResponseRedirect
from django.urls import reverse

present = set()  # Membuat variabel present di modul StudentView.views

def add_manually_post(request):
    if request.method == "POST":
        student_sid = request.POST["student-name"]
        try:
            student = Student.objects.get(sid=student_sid)
            # Ubah status menjadi "Present"
            student.status = "Present"
            student.save()
        except Student.DoesNotExist:
            pass  # Handle the case where the student with the given sid doesn't exist
    return HttpResponseRedirect("/submitted")

def submitted(request):
    return render(request, "StudentView/Submitted.html")

def student_view_index(request):
    students = Student.objects.all()
    return render(request, "StudentView/StudentViewIndex.html", {"students": students})