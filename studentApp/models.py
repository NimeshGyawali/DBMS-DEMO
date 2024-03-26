from django.db import models


class StaffMember(models.Model):
    user_no = models.CharField(max_length=50, primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    rank = models.CharField(max_length=50, blank=True, null=True)  
    office = models.CharField(max_length=100, blank=True, null=True)  

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Student(models.Model):
    id = models.AutoField(primary_key=True)
    user_no = models.CharField(max_length=50)  
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    under_grad = models.BooleanField(default=True)  
    address = models.TextField(blank=True, null=True)  
    city = models.CharField(max_length=100, blank=True, null=True)  
    state = models.CharField(max_length=100, blank=True, null=True)  
    zip_code = models.CharField(max_length=20, blank=True, null=True)  
    enroll_date = models.DateField(blank=True, null=True)  

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Course(models.Model):
    
    course_id = models.CharField(max_length=50, primary_key=True)
    id = models.CharField(max_length=50, blank=True, null=True)
    title = models.CharField(max_length=200)
    credit_hours = models.PositiveIntegerField(blank=True, null=True)  

    def __str__(self):
        return self.title

class Project(models.Model):
    project_no = models.CharField(max_length=50, primary_key=True)
    project_name = models.CharField(max_length=200)
    level = models.CharField(max_length=50)
    keywords = models.TextField()
    description = models.TextField()
    student = models.ForeignKey(Student, on_delete= models.SET_NULL , null=True, blank=False)  

    def __str__(self):
        return self.project_name

class Exam(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    exam_no = models.CharField(max_length=50)
    time = models.TimeField()
    day = models.DateField()
    room_no = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.student} - {self.exam_no}"

class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    grade = models.CharField(max_length=2, blank=True, null=True)

    def __str__(self):
        return f"{self.student} -> {self.course} : {self.grade}"

class Teaching(models.Model):
    instructor = models.ForeignKey(StaffMember, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.instructor} teaches {self.course}"
