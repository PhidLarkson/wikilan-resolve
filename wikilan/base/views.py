from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import *
from .models import *
from django.urls import reverse
import os

# Create your views here.
def login_view(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('/')
        else:
            return render(request, "login.html", {
                "msg": "Invalid login credentials"
            })
    else:
        return HttpResponse('<h1>Failed attempt to login</h1>')


def logout_view(request):
    logout(request)
    return redirect("/")   


def signup(request):
    if request.method == "POST":
        form = OperatorAccountForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('home')  # Replace 'home' with the URL name of your home page
    else:
        form = OperatorAccountForm()

    return render(request, 'signup.html', {"form": form})


def home(request):
    user = request.user.username
    books = TextBook.objects.all()
    context = {
        'profile': user,
        'books': books
    }
    return render(request, 'home.html', context)

def about(request):
    return render(request, 'about.html')

def show_book(request, id):
    book = get_object_or_404(TextBook, id=id)
    context = {
        'book': book
    }
    return render(request, 'show_book.html', context)

def download_book(request, id):
    book = get_object_or_404(TextBook, id=id)
    file_path = book.file.path
    with open(file_path, 'rb') as file:
        response = HttpResponse(file.read(), content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
        return response

def about(request):
    return render(request, 'about.html')

def profile(request):
    return render(request, 'base/profile.html')

def resources(request):    
    return render(request, 'base/book.html')

# CRUD
def create_profile(request):
    if request.method == 'POST':
        user = request.user
        bio = request.POST['bio']
        phone = request.POST['phone']
        address = request.POST['address']
        profile_pic = request.FILES['profile_pic']
        mail = request.POST['mail']
        profile = Profile(user=user, bio=bio, phone=phone, address=address, profile_pic=profile_pic, mail=mail)
        profile.save()
        return render(request, 'profile.html')
    return render(request, 'create_profile.html')        


def add_book(request):
    if request.method == 'POST':
        form = TextBookForm(request.POST, request.FILES)
        if form.is_valid():
            # file = request.FILES['file']
            # fs = FileSystemStorage()
            # filename = fs.save(file.name, file)
            # uploaded_file_url = fs.url(filename)    
            
            book = form.save(commit=False)  
            book.room_operator=request.user        
            book.save()
            form.save_m2m()
            return redirect('home')
        else:
            # Handle the case where the form is not valid
            return render(request, 'home.html', {'form': form})
    else:
        # Handle the case where the request method is not POST
        form = TextBookForm()
        return render(request, 'add_book.html', {'form': form})

def create_staff(request):
    if request.method == 'POST':
        user = request.user
        staff_id = request.POST['staff_id']
        department = request.POST['department']
        staff = Staff(user=user, staff_id=staff_id, department=department)
        staff.save()
        return render(request, 'base/staff.html')
    return render(request, 'base/create_staff.html')

def create_student(request):
    if request.method == 'POST':
        user = request.user
        reference = request.POST['reference']
        department = request.POST['department']
        level = request.POST['level']
        student = Student(user=user, reference=reference, department=department, level=level)
        student.save()
        return render(request, 'base/student.html')
    return render(request, 'base/create_student.html')

def update_profile(request, pk):
    profile = Profile.objects.get(pk=pk)
    if request.method == 'POST':
        profile.bio = request.POST['bio']
        profile.phone = request.POST['phone']
        profile.address = request.POST['address']
        profile.profile_pic = request.FILES['profile_pic']
        profile.mail = request.POST['mail']
        profile.save()
        return render(request, 'base/profile.html')
    return render(request, 'base/update_profile.html', {'profile': profile})

def update_book(request, pk):
    book = BookObject.objects.get(pk=pk)
    if request.method == 'POST':
        book.title = request.POST['title']
        book.author = request.POST['author']
        book.description = request.POST['description']
        book.save()
        return render(request, 'base/book.html')
    return render(request, 'base/update_book.html', {'book': book})

def update_staff(request, pk):
    staff = Staff.objects.get(pk=pk)
    if request.method == 'POST':
        staff.staff_id = request.POST['staff_id']
        staff.department = request.POST['department']
        staff.save()
        return render(request, 'base/staff.html')
    return render(request, 'base/update_staff.html', {'staff': staff})

def update_student(request, pk):
    student = Student.objects.get(pk=pk)
    if request.method == 'POST':
        student.reference = request.POST['reference']
        student.department = request.POST['department']
        student.level = request.POST['level']
        student.save()
        return render(request, 'base/student.html')
    return render(request, 'base/update_student.html', {'student': student})

def delete_profile(request, pk):
    profile = Profile.objects.get(pk=pk)
    profile.delete()
    return render(request, 'base/profile.html')

def delete_book(request, pk):
    book = BookObject.objects.get(pk=pk)
    book.delete()
    return render(request, 'base/book.html')

def delete_staff(request, pk):
    staff = Staff.objects.get(pk=pk)
    staff.delete()
    return render(request, 'base/staff.html')

def delete_student(request, pk):
    student = Student.objects.get(pk=pk)
    student.delete()
    return render(request, 'base/student.html')

def view_profile(request, pk):
    profile = Profile.objects.get(pk=pk)
    return render(request, 'base/view_profile.html', {'profile': profile})

def view_book(request, pk):
    book = BookObject.objects.get(pk=pk)
    return render(request, 'base/view_book.html', {'book': book})

def view_staff(request, pk):
    staff = Staff.objects.get(pk=pk)
    return render(request, 'base/view_staff.html', {'staff': staff})

def view_student(request, pk):
    student = Student.objects.get(pk=pk)
    return render(request, 'base/view_student.html', {'student': student})

def view_category(request, pk):
    category = Category.objects.get(pk=pk)
    return render(request, 'base/view_category.html', {'category': category})

