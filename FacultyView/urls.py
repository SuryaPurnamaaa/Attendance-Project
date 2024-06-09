from . import views
from django.urls import path

urlpatterns = [
    path("", views.faculty_view_index, name="faculty_view"),
    path("add_manually", views.add_manually, name="add_manually"),
    path('set-to-absent/', views.set_to_absent, name='set_to_absent'),
    path('stats/', views.attendance_statistics, name='attendance_statistics'),
    path('get_attendance_data/', views.get_attendance_data, name='get_attendance_data'),  # Add this line

]
