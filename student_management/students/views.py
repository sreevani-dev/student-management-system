
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import student
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import re
from django.core.paginator import Paginator
from django.db.models import Count


@login_required
def student_list(request):
    search = request.GET.get('search')
    course_filter = request.GET.get('course')

    students = student.objects.all()

    if search:
        students = students.filter(name__icontains=search)

    if course_filter:
        students = students.filter(course=course_filter)

    courses = student.objects.values_list(
        'course', flat=True
    ).distinct()
    paginator = Paginator(students, 5)

    page_number = request.GET.get('page')

    students = paginator.get_page(page_number)

    total_students = paginator.count
    return render(request, 'students/student_list.html', {
        'students': students,
        'courses': courses
    })
    


@login_required
def student_register(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        age = request.POST['age']
        course = request.POST['course']

        if not name.replace(" ", "").isalpha():
            return render(request, 'students/student_register.html', {
                'error': 'Name should contain letters only'
            })

        try:
            validate_email(email)
        except ValidationError:
            return render(request, 'students/student_register.html', {
                'error': 'Please enter a valid email address'
            })

        if not age.isdigit() or int(age) < 1 or int(age) > 100:
            return render(request, 'students/student_register.html', {
                'error': 'Age must be between 1 and 100'
            })

        if not course.strip() or not re.fullmatch(
            r'[A-Za-z0-9 .+#-]+', course.strip()
        ):
            return render(request, 'students/student_register.html', {
                'error': 'Please enter a valid course name'
            })

        student.objects.create(
            name=name,
            email=email,
            age=age,
            course=course
        )
        messages.success(request,'Student registered successfully!')
        return redirect('student_list')

    return render(request, 'students/student_register.html')


@login_required
def student_update(request, id):
    students = student.objects.get(id=id)

    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        age = request.POST['age']
        course = request.POST['course']

        error = ''

        if not name.replace(" ", "").isalpha():
            error = 'Name should contain letters only'

        if not error:
            try:
                validate_email(email)
            except ValidationError:
                error = 'Please enter a valid email address'

        if not error:
            if not age.isdigit() or int(age) < 1 or int(age) > 100:
                error = 'Age must be between 1 and 100'

        if not error:
            if not course.strip() or not re.fullmatch(
                r'[A-Za-z0-9 .+#-]+', course.strip()
            ):
                error = 'Please enter a valid course name'

        if error:
            return render(request, 'students/student_update.html', {
                'students': students,
                'error': error
            })

        students.name = name
        students.email = email
        students.age = age
        students.course = course
        students.save()
        messages.success(request,'Student details upload successfully!')

        return redirect('student_list')

    return render(request, 'students/student_update.html', {
        'students': students
    })


@login_required
def student_delete(request, id):
    if request.method == 'POST':
       students = student.objects.get(id=id)
       students.delete()
       messages.success(request,'student deleted successfully')
    return redirect('student_list')


def user_register(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('login')

    return render(request, 'students/user_register.html', {
        'form': form
    })


def home(request):
    total_students = student.objects.count()
    total_courses = student.objects.values('course').distinct().count()
    course_counts=student.objects.values('course').annotate(total=Count('id'))
    recent_students=student.objects.order_by('-id'[:5])

    return render(request, 'students/home.html', {
        'total_students': total_students,
        'total_courses': total_courses,
        'recent_students':recent_students,
        'course_counts':course_counts

    })

