from django.shortcuts import render
from django.http import HttpResponse
from .forms import StudentForm
from django.db import connection
from django.views.decorators.csrf import csrf_exempt

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]
def homepage(request):
    return render(request, 'homepage.html')
@csrf_exempt
def add_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            roll_no = form.cleaned_data['roll_no']
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            phone_no = form.cleaned_data['phone_no']
            
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO studentApp_student (roll_no, name, email, phone_no) VALUES (%s, %s, %s, %s)",
                               [roll_no, name, email, phone_no])
            return HttpResponse("Student Added Successfully!")
    else:
        form = StudentForm()
    return render(request, 'add_student.html', {'form': form})

@csrf_exempt
def search_student(request):
    if 'roll_no' in request.GET:
        roll_no = request.GET['roll_no']
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM studentApp_student WHERE roll_no = %s", [roll_no])
            student = dictfetchall(cursor)
        return render(request, 'search_results.html', {'students': student})
    return render(request, 'search_student.html')
