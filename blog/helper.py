from redis import Redis, StrictRedis
from pickle import dumps, loads
from django.shortcuts import  redirect
from django.urls import reverse

r = Redis('10.0.129.66', 6379, 1)  # 1号库存放页面缓存
re = Redis('10.0.129.66', 6379, 2) # 2号库存放帖子浏览量


# 页面缓存的装饰器
def page_cache(timeout):
    '''
    wrap1 = page_cache(timeout)
    wrap2 = wrap1(view_func)
    wrap2(request, *args, **kwargs)
    '''
    def wrap1(view_func):
        def wrap2(request, *args, **kwargs):
            key = 'page-%s' % request.get_full_path()
            pck_response = r.get(key)
            if pck_response is None:
                print('data from db')
                response = view_func(request, *args, **kwargs)
                #将 response 序列化为字节型数据后存入redis
                pck_response = dumps(response)
                r.set(key, pck_response, timeout)
            # 将字节型的pck_response数据反序列化为response后返回
            response = loads(pck_response)
            return response
        return wrap2
    return wrap1


#统计帖子浏览量的装饰器
def read_counter(view_fun):
    def wrap(request, n):
        response = view_fun(request, n)
        if response.status_code == 200:
            re.zincrby('read_counter', 'post%s'%n)
        return response
    return wrap

  
#取出帖子浏览量
def get_read_counter(n):
    members = re.zrange('read_counter',0,-1, withscores = True)
    pid_count = {'post%s'%pid:int(count) for pid, count in members}
    read_count = pid_count.get("postb'post%s'"%n, 1)
    return read_count


def check_login(view_func):
    def wrap(request, *args, **kwargs):
        if request.session.get('is_login', None):
            response = view_func(request, *args, **kwargs)
            return response
        else:
            return redirect(reverse('user:login'))
    return wrap
