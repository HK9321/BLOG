# MIDDLEWARE
from redis import StrictRedis

sr = StrictRedis('10.0.129.66', 6379, 1)


class MiddlewareMixin(object):
    def __init__(self, get_response=None):
        self.get_response = get_response
        super(MiddlewareMixin, self).__init__()

    def __call__(self, request):
        response = None
        if hasattr(self, 'process_request'):
            response = self.process_request(request)
        if not response:
            response = self.get_response(request)
        if hasattr(self, 'process_response'):
            response = self.process_response(request, response)
        return response


class Online_user_count:
    def __init__(self, get_response=None):
        self.get_response = get_response
        super(Online_user_count, self).__init__()

    def __call__(self, request, *args, **kwargs):
        online_ip = "online user ip: %s" % request.META['REMOTE_ADDR']
        sr.set(online_ip, True, 30)
        online_user_num = len(sr.execute_command("KEYS", "online user ip:*"))
        request.online_user_num = online_user_num
        response = self.get_response(request, *args, **kwargs)
        # result = ("<p id=\"onlineusernum\">当前在线用户: %d</p></body>" % online_user_num).encode("utf-8").join(
        #     [response.content[0:-17], response.content[-17:]])
        # response.content = result
        return response
