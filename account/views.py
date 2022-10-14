from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User

def login_request(request):
    if request.user.is_authenticated:
        return redirect('index')
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('index')
        else:
            return render(request,'account/login.html',{
                'error' : 'Please check your username and password',
                'class' : 'warning'
            })
    return render(request,'account/login.html')


def register_request(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        password = request.POST['password']
        repassword = request.POST['repassword']
        if password == repassword:
            if User.objects.filter(username=username).exists():
               return render(request,'account/register.html',{
                    'error' : 'Please check your username',
                    'class' : 'warning',
                    'email' : email,
                    'firstname' : firstname,
                    'lastname' : lastname,
                })
            else:
                if User.objects.filter(email=email).exists():
                    return render(request,'account/register.html',{
                        'error' : 'Please check your email',
                        'class' : 'warning',
                        'username' : username,
                        'firstname' : firstname,
                        'lastname' : lastname,
                    })
                else:
                    user = User.objects.create_user(username=username,first_name=firstname,last_name=lastname,email=email,password=password)
                    user.save()
                    return redirect('login') 
        else:
            return render(request,'account/register.html',{
                'error' : 'Please check your password and repassword',
                'class' : 'warning',
                'email' : email,
                'username' : username,
                'firstname' : firstname,
                'lastname' : lastname,
            })
    return render(request,'account/register.html')

def logout_request(request):
    logout(request)
    return redirect('index')

def view_profile(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            email = request.POST['email']
            firstname = request.POST['firstname']
            lastname = request.POST['lastname']
            password = request.POST['password']
            repassword = request.POST['repassword']
            
            if password != '':
                if password == repassword:
                    request.user.set_password(password)
                    request.user.first_name= firstname
                    request.user.last_name = lastname
                    request.user.email = email
                    request.user.save()
                    login(request,request.user)
                    return render(request,'account/my_profile.html',{
                        'error' : 'Your profile has been updated.',
                        'class' : 'success',
                        'email' : request.user.email,
                        'username' : request.user.username,
                        'firstname' : request.user.first_name,
                        'lastname' : request.user.last_name,
                    })
                else:
                    return render(request,'account/my_profile.html',{
                        'error' : 'Check your password',
                        'class' : 'warning',
                        'email' : request.user.email,
                        'username' : request.user.username,
                        'firstname' : request.user.first_name,
                        'lastname' : request.user.last_name,
                    })
            else:
                request.user.first_name= firstname
                request.user.last_name = lastname
                request.user.email = email
                request.user.save()

                return render(request,'account/my_profile.html',{
                    'error' : 'Your profile has been updated.',
                    'class' : 'success',
                    'email' : request.user.email,
                    'username' : request.user.username,
                    'firstname' : request.user.first_name,
                    'lastname' : request.user.last_name,
                })

        return render(request,'account/my_profile.html',{
            'email' : request.user.email,
            'username' : request.user.username,
            'firstname' : request.user.first_name,
            'lastname' : request.user.last_name,
        })
    else:
        return redirect('login')

