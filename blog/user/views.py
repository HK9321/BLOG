from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from post.models import Post

from form.userform import RegisterForm, LoginForm
from user.models import User, Mail


def register(request):
    """用户注册"""
    if request.method == 'POST':
        register_form = RegisterForm(request.POST, request.FILES)
        if register_form.is_valid():
            username = register_form.cleaned_data["username"]
            password = register_form.cleaned_data["password_2"]
            email = register_form.cleaned_data["email"]
            icon = request.FILES['icon']
            User.objects.create(username=username, password=password, email=email, icon=icon)
            return redirect('/user/login/')
        else:
            return render(request, 'user/regster.html', {'form': register_form})
    return render(request, 'user/regster.html')


def login(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            print(username, password)
            user = User.objects.filter(username=username)[0]
            if user is not None:
                if user.verify_password(password):
                    request.session['user111'] = user.id
                    request.session['is_login'] = True
                    request.session['username'] = user.username
                    return redirect(reverse("post:index"))
            else:
                return redirect(reverse('user:login'))
        else:
            return redirect(reverse('user:register'))
    return render(request, 'user/login.html')


def logout(request):
    request.session.clear()
    return redirect(reverse('user/login'))


# 用户详情页面
def user_info(request, *args, **kwargs):
    uid = args[0]
    post_titles = Post.objects.filter(uid=uid).only('title')
    user = User.objects.filter(id=uid).first()
    if user is None:
        return HttpResponse('我们这里没有这个人')
    context = {'user': user, 'post_titles': post_titles}
    return render(request, 'user/user_info.html', context)


def index(request):
    return None


def sendMail(request):
    
    return render(request, 'user/sendmail.html')
