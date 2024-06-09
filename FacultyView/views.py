import qrcode
import socket
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, HttpResponseRedirect, redirect
from .models import Student, Attendance
from django.db.models import Count
from django.db.models import Count, Case, When

def qrgenerator():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]

    link = f"http://{ip}:8000/add_manually"

    # Function to generate and display a QR code
    def generate_qr_code(link):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(link)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        img.save("FacultyView/static/FacultyView/qrcode.png")

    generate_qr_code(link)


def faculty_view_index(request):
    if request.method == "POST":
        attendance_date = request.POST.get("attendance_date")
        for student in Student.objects.all():
            status = request.POST.get(f"status_{student.sid}")
            # Simpan data ke database
            Attendance.objects.create(
                student=student,
                date=attendance_date,
                status=status
            )
        return HttpResponseRedirect('/')  # Redirect to homepage or any other page you prefer
    
    students = Student.objects.all()
    qrgenerator()  # Call the qrgenerator function to generate QR code
    return render(
        request,
        "FacultyView/FacultyViewIndex.html",
        {"students": students},
    )

def set_to_absent(request):
    if request.method == "POST":
        # Mengambil semua objek murid dan mengubah statusnya menjadi "Absent"
        students = Student.objects.all()
        for student in students:
            student.status = 'Absent'
            student.save()
    # Redirect kembali ke halaman utama setelah selesai
    return redirect('/')

def add_manually(request):
    """
    View function to display the manual attendance addition page.
    """
    students = Student.objects.all()
    return render(request, "StudentView/StudentViewIndex.html", {"students": students})

def attendance_statistics(request):
    
    # Ambil data kehadiran siswa dari database
    attendance_data = Attendance.objects.values('status').annotate(count=Count('status'))

    # Persiapkan data untuk chart dan statistik
    total_students = sum(attendance['count'] for attendance in attendance_data)
    absent_students = next((attendance['count'] for attendance in attendance_data if attendance['status'] == 'Absent'), 0)
    present_students = next((attendance['count'] for attendance in attendance_data if attendance['status'] == 'Present'), 0)
    sick_students = next((attendance['count'] for attendance in attendance_data if attendance['status'] == 'Sick'), 0)
    permit_students = next((attendance['count'] for attendance in attendance_data if attendance['status'] == 'Permit'), 0)

    # Ambil data gender distribution dari database
    male_students = Student.objects.filter(gender='Male').count()
    female_students = Student.objects.filter(gender='Female').count()

    context = {
        'total_students': total_students,
        'absent_students': absent_students,
        'present_students': present_students,
        'sick_students': sick_students,
        'permit_students': permit_students,
        'male_students': male_students,
        'female_students': female_students,
    }

    return render(request, 'FacultyView/AttendanceStatistics.html', context)

def get_attendance_data(request):
    if request.method == "GET":
        selected_date = request.GET.get('selected_date')
        # Ambil data kehadiran siswa berdasarkan tanggal yang dipilih
        attendance_data = Attendance.objects.filter(date=selected_date).values('status').annotate(count=Count('status'))
        # Persiapkan data untuk dikirim sebagai JSON
        data = {
            'total_students': len(attendance_data),
            'absent_students': next((attendance['count'] for attendance in attendance_data if attendance['status'] == 'Absent'), 0),
            'present_students': next((attendance['count'] for attendance in attendance_data if attendance['status'] == 'Present'), 0),
            'sick_students': next((attendance['count'] for attendance in attendance_data if attendance['status'] == 'Sick'), 0),
            'permit_students': next((attendance['count'] for attendance in attendance_data if attendance['status'] == 'Permit'), 0)
        }
        
        # Get student attendance data
        students_attendance_data = Attendance.objects.filter(date=selected_date).values(
            'student__name',
            'status'
        ).annotate(
            total_attendance=Count('student'),
            absent_count=Count(Case(When(status='Absent', then=1))),
            present_count=Count(Case(When(status='Present', then=1))),
            sick_count=Count(Case(When(status='Sick', then=1))),
            permit_count=Count(Case(When(status='Permit', then=1))),
        )

        data['students_attendance_data'] = list(students_attendance_data)
        
        return JsonResponse(data)
