from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Blog1
from .forms import Blog_Form,UserForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.sessions.models import Session



# Create your views here.

def login_page(request):
    page='login'
    if request.user.is_authenticated:
       return redirect('/') 
    
    if request.method=="POST":
        usern=request.POST.get('Username', '')
        passw =request.POST.get('Password', '')
        
        user=authenticate(request, username=usern, password=passw)
        if user is not None:
            login(request, user)
            return redirect('/display')
        else:
            messages.error(request,"Username or Password does NOT exist")
    return render(request, 'login_register.html', {'page':page})

def logoutUser(request):
    logout(request)
    return redirect('/')

def register(request):
    form = UserCreationForm()
    if request.method=='POST':  
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.username= user.username.lower()
            user.save()
            login(request,user)
            return redirect('/')
        else: 
            messages.error(request, 'Something went wrong please try again.')
    return render(request, 'login_register.html', {'form':form})

def home(request):
    return render(request, 'base.html')


@login_required(login_url='login')
def room(request):
    articles= Blog1.objects.all()
    page=request.GET.get('page',1)
    paginator=Paginator(articles,5)
    
    try:
        articles=paginator.page(page)
    except PageNotAnInteger:
        articles=paginator.page(1)
    except EmptyPage:
        articles=paginator.page(paginator.num_pages)
    return render(request, 'room.html', {'articles':articles})


@login_required(login_url='login')
def user_article(request):
    if request.user.is_authenticated:
        username=request.user.id
        articles=Blog1.objects.filter(user=username)
        page=request.GET.get('page',1)
        paginator=Paginator(articles,5)
        
        try:
            articles=paginator.page(page)
        except PageNotAnInteger:
            articles=paginator.page(1)
        except EmptyPage:
            articles=paginator.page(paginator.num_pages)
        return render(request, 'user_articles.html', {'articles':articles})


@login_required(login_url='login')
def create(request):
    if request.method=="POST":
        form=Blog_Form(request.POST)
        if form.is_valid():
            try:
                article=form.save(commit=False)
                article.user = request.user
                article.save()
                return redirect('/display')
            except: pass
    else: 
        form=Blog_Form()
    return render(request, 'form.html', {'form': form})

@login_required(login_url='login')
def edit(request, id):
    articles= Blog1.objects.get(id=id)
    form=Blog_Form(instance=articles)
    if request.method=="POST":
        if request.user.is_superuser or request.user == articles.user:
            form=Blog_Form(request.POST,instance=articles)
            if form.is_valid():
                form.save()
                return redirect("/display")
        elif request.user!=articles.user:
            return HttpResponse("You cannot edit this article")
    return render(request, 'form.html',{'form':form})

@login_required(login_url='login')
def delete(request, id):
    articles=Blog1.objects.get(id=id)
    if request.method=="POST":
        if request.user.is_superuser or request.user == articles.user:
            articles.delete()
            return redirect('/display')
        elif request.user!=articles.user:
            return HttpResponse("You cannot delete this article")
    return render(request, 'delete.html', {'articles':articles})

# @login_required(login_url='login')
# def users(request,id):
#     session = request.session.get('_auth_user_id')
#     user = User.objects.get(id=session)
#     # articles = user.objects.get(id=id)
#     # context = {'user':user}
#     return render(request,'usershow.html',{'user':user})
@login_required(login_url='login')
def users(request):
    session = request.session.get('_auth_user_id')
    user = User.objects.get(id=session)
    return render(request, 'usershow.html', {'user': user})

@login_required(login_url='login')
def usera(request,id):
    user = User.objects.get(id=id)
    return render(request, 'useranother.html', {'user': user})

@login_required(login_url='login')
def userp(request):
    session = request.session.get('_auth_user_id')
    user = User.objects.get(id=session)
    form = UserForm(instance=user)
    if request.method == "POST":
        form = UserForm(request.POST,instance=user)
        if form.is_valid():
                # userprofile=form.save(commit=False)
                # userprofile.user = session
                # userprofile.save()
                form.save()
                return redirect('/users/')
    else: 
        form=UserForm()
    return render(request,'userpage.html',{'form':form})

    
       

