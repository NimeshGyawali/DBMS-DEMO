



from django.http import HttpResponse
from django.shortcuts import render
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
def homepage(request):
    return render(request, 'homepage.html')
# Utility function to execute a raw SQL insert statement.
def execute_sql_insert(statement, params):
    with transaction.atomic(), connection.cursor() as cursor:
        cursor.execute(statement, params)

@csrf_exempt
def add_staff_member(request):
    if request.method == 'POST':
        user_no = request.POST.get('user_no')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        rank = request.POST.get('rank')
        office = request.POST.get('office')
        
        sql = """
        INSERT INTO studentApp_staffmember (user_no, first_name, last_name, rank, office)
        VALUES (%s, %s, %s, %s, %s)
        """
        params = [user_no, first_name, last_name, rank, office]
        execute_sql_insert(sql, params)
        
        return HttpResponse("Staff Member Added Successfully!")
    else:
        return render(request, 'add_staff_member.html')

@csrf_exempt
def add_student(request):
    if request.method == 'POST':
        user_no = request.POST.get('user_no')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        under_grad = request.POST.get('under_grad') == 'True'
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zip_code = request.POST.get('zip_code')
        enroll_date = request.POST.get('enroll_date')

        sql = """
        INSERT INTO studentApp_student (user_no, first_name, last_name, under_grad, address, city, state, zip_code, enroll_date)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        params = [user_no, first_name, last_name, under_grad, address, city, state, zip_code, enroll_date]
        execute_sql_insert(sql, params)
        
        return HttpResponse("Student Added Successfully!")
    else:
        return render(request, 'add_student.html')

@csrf_exempt
def add_course(request):
    if request.method == 'POST':
        course_id = request.POST.get('course_id')
        id = course_id
        title = request.POST.get('title')
        credit_hours = request.POST.get('credit_hours')

        sql = """
        INSERT INTO studentApp_course (course_id, id, title, credit_hours)
        VALUES (%s,%s, %s, %s)
        """
        params = [course_id ,id, title, credit_hours]
        execute_sql_insert(sql, params)
        
        return HttpResponse("Course Added Successfully!")
    else:
        return render(request, 'add_course.html')

@csrf_exempt
def add_project(request):
    if request.method == 'POST':
        project_no = request.POST.get('project_no')
        project_name = request.POST.get('project_name')
        level = request.POST.get('level')
        keywords = request.POST.get('keywords')
        description = request.POST.get('description')
        student_user_no = request.POST.get('student_user_no')

        sql = """
        INSERT INTO studentApp_project (project_no, project_name, level, keywords, description, student_id)
        VALUES (%s, %s, %s, %s, %s, (SELECT id FROM studentApp_student WHERE user_no=%s))
        """
        params = [project_no, project_name, level, keywords, description, student_user_no]
        execute_sql_insert(sql, params)
        
        return HttpResponse("Project Added Successfully!")
    else:
        return render(request, 'add_project.html')

@csrf_exempt
def add_exam(request):
    if request.method == 'POST':
        exam_no = request.POST.get('exam_no')
        time = request.POST.get('time')
        day = request.POST.get('day')
        room_no = request.POST.get('room_no')
        student_user_no = request.POST.get('student_user_no')

        sql = """
        INSERT INTO studentApp_exam (exam_no, time, day, room_no, student_id)
        VALUES (%s, %s, %s, %s, (SELECT id FROM studentApp_student WHERE user_no=%s))
        """
        params = [exam_no, time, day, room_no, student_user_no]
        execute_sql_insert(sql, params)

        return HttpResponse("Exam Added Successfully!")
    else:
        return render(request, 'add_exam.html')

@csrf_exempt
def add_enrollment(request):
    if request.method == 'POST':
        student_user_no = request.POST.get('student_user_no')
        course_id = request.POST.get('course_id')
        grade = request.POST.get('grade')

        sql = """
        INSERT INTO studentApp_enrollment (student_id, course_id, grade)
        VALUES ((SELECT id FROM studentApp_student WHERE user_no=%s), %s, %s)
        """
        params = [student_user_no, course_id, grade]
        execute_sql_insert(sql, params)

        return HttpResponse("Enrollment Added Successfully!")
    else:
        return render(request, 'add_enrollment.html')

@csrf_exempt
def add_teaching(request):
    if request.method == 'POST':
        staff_user_no = request.POST.get('staff_user_no')
        course_id = request.POST.get('course_id')

        sql = """
        INSERT INTO studentApp_teaching (instructor_id, course_id)
        VALUES ((SELECT id FROM studentApp_staffmember WHERE user_no=%s), %s)
        """
        params = [staff_user_no, course_id]
        execute_sql_insert(sql, params)

        return HttpResponse("Teaching Assignment Added Successfully!")
    else:
        return render(request, 'add_teaching.html')
from django.shortcuts import render
from django.db import connection
from django.http import HttpResponse

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

def search_results(request):
    context = {'students': [], 'courses': [], 'projects': [], 'staff': []}
    
    student_query = request.GET.get('student_query', '')
    course_query = request.GET.get('course_query', '')
    project_query = request.GET.get('project_query', '')
    staff_query = request.GET.get('staff_query', '')

    if student_query:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM studentApp_student WHERE user_no LIKE %s OR first_name LIKE %s OR last_name LIKE %s", ['%' + student_query + '%'] * 3)
            context['students'] = dictfetchall(cursor)

    if course_query:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM studentApp_course WHERE course_id LIKE %s OR title LIKE %s", ['%' + course_query + '%'] * 2)
            context['courses'] = dictfetchall(cursor)

    if project_query:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM studentApp_project WHERE project_no LIKE %s OR project_name LIKE %s", ['%' + project_query + '%'] * 2)
            context['projects'] = dictfetchall(cursor)

    if staff_query:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM studentApp_staffmember WHERE user_no LIKE %s OR first_name LIKE %s OR last_name LIKE %s", ['%' + staff_query + '%'] * 3)
            context['staff'] = dictfetchall(cursor)
    
    return render(request, 'search_results.html', context)

