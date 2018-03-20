import random
from math import ceil

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

import helper as hp
from post.models import Post
from user.models import User
from post.models import Comment
from helper import check_login



@hp.page_cache(30)
def index(request):
    '''首页,帖子列表'''
    post_count = Post.objects.count()
    pages = ceil(post_count / 5)
    page = int(request.GET.get('page', 1))
    page = (page-1) if 1 <= page <= pages else 0
    start = page * 5
    end = (page+1) * 5
    post_all = Post.objects.all()[start:end]
    return render(request, 'post/index.html', {'post_all': post_all,
                                               'pages': range(pages),
                                               'currentpage': page + 1,
                                               'pre_page': page,
                                               'next_page': page + 2})


def publish(request):
    if request.method == "POST":
        u = random.choice(User.objects.all())
        uid = u.id
        title = request.POST['title']
        content = request.POST['content']
        Post.objects.create(uid=uid, title=title, content=content)
        return HttpResponseRedirect(reverse('post:index'))
    return render(request, 'post/publish.html')


@hp.read_counter
@hp.page_cache(30)
def showpost(request, n):
    articalSet = Post.objects.filter(id=n)
    if articalSet:
        artical = articalSet[0]
    else:
        artical = Post.objects.all()[0]
    read_count = hp.get_read_counter(n)
    return render(request, 'post/showpost.html', {'artical': artical, 'read_count':read_count})


def deletepost(request, n):
    artical = Post.objects.filter(id=n)[0]
    artical.delete()
    return render(request, 'post/deletepost.html')


# 展示评论
def comment(request, *args, **kwargs):
    comment_list = Comment.objects.filter(pid=args[0])
    def get_username(comment):
        name = User.objects.filter(id=comment.uid).first().username
        return name
    username_list = map(get_username, comment_list)

    # username_list = map(Comment.get_username(*args), comment_list)
    name_comment = zip(username_list, comment_list)
    context = {'name_comment': name_comment, 'post': args[0]}
    return render(request, 'post/comment.html', context)


# 发表评论
@check_login
def reply(request,*args,**kwargs):
    if request.method == 'POST':
        c = Comment()
        c.uid = request.session['user111']
        c.pid = args[0]
        id = request.GET.get('parent')
        print(id)
        c.parent = Comment.objects.filter(id=int(id)).first()
        c.comment_text = request.POST.get('commet_text')
        c.save()
        articalSet = Post.objects.filter(id=args[0])
        if articalSet:
            artical = articalSet[0]
        else:
            artical = Post.objects.all()[0]
        return render(request, 'post/showpost.html', {'artical': artical})

