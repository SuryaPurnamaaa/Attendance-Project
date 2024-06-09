from django.db import models

class Student(models.Model):
    STATUS_CHOICES = [
        ('Absent', 'Absent'),
        ('Present', 'Present'),
        ('Sick', 'Sick'),
        ('Permit', 'Permit'),
    ]
    
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]

    sid = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=100)
    batch = models.IntegerField()
    major = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Absent')
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)

    def __str__(self):
        return self.name    

class Attendance(models.Model):
    STATUS_CHOICES = [
        ('Absent', 'Absent'),
        ('Present', 'Present'),
        ('Sick', 'Sick'),
        ('Permit', 'Permit'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)

    class Meta:
        unique_together = ('student', 'date')
