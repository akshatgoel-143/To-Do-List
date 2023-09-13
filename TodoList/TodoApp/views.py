from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import todo
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def home(requst):
    if requst.method =='POST':
        task = requst.POST.get('task')
        new_todo = todo(user=requst.user, todo_name=task)
        new_todo.save()

    all_todos = todo.objects.filter(user=requst.user)
    context ={
        'todos': all_todos
    }
    return render(requst, 'TodoApp/todo.html', context)

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if len(password) < 3:
            messages.error(request, 'Password Must be at least 3 characters')
            return redirect('register')
        
        get_all_users_by_username = User.objects.filter(username=username)
        if get_all_users_by_username:
            messages.error(request, 'Username already exists')
            return redirect('register')

        new_user = User.objects.create_user(username=username,email=email,password=password)
        new_user.save()
        messages.success(request,'User created Successfully.')
        return redirect('login')
    return render(request, 'TodoApp/register.html',{})

def loginpage(request):
    if request.method == 'POST':
        username = request.POST.get('uname')
        password = request.POST.get('pass')

        validate_user = authenticate(username=username, password=password)
        if validate_user is not None:
            login(request, validate_user)
            return redirect('home-page')
        else:
            messages.error(request, 'Invalid User')
            return redirect('login')   

    return render(request, 'TodoApp/login.html',{})

def edit(request, name):
    if request.method =='POST':
        task = request.POST.get('task')
        task2 = request.POST.get('task2')
        print("AA",task2)
        new_todo = todo.objects.get(user=request.user, id=int(task2))
        new_todo.todo_name=task
        new_todo.save()
        return redirect('home-page')
    
    edit_todo = todo.objects.get(user = request.user, todo_name=name)

    all_todos = todo.objects.filter(user=request.user)
    context ={
        'todos': all_todos, 'e_todo':edit_todo
    }
    return render(request,'TodoApp/edit.html',context)

def DeleteTask(request, name):
    get_todo = todo.objects.get(user = request.user, id=int(name))
    get_todo.delete()
    return redirect('home-page')

def Update(request, name):
    get_todo = todo.objects.get(user = request.user, id=int(name))
    get_todo.status=True
    get_todo.save()
    return redirect('home-page')

def logoutview(request):
    logout(request)
    return redirect('login')
    