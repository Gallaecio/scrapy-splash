# -*- coding: utf-8 -*-
from twisted.web.resource import Resource

from scrapy_splash.utils import to_bytes


class HtmlResource(Resource):
    isLeaf = True
    content_type = 'text/html'
    html = ''
    extra_headers = {}
    status_code = 200

    def render_GET(self, request):
        request.setHeader(b'content-type', to_bytes(self.content_type))
        for name, value in self.extra_headers.items():
            request.setHeader(to_bytes(name), to_bytes(value))
        request.setResponseCode(self.status_code)
        return to_bytes(self.html)


class HelloWorld(HtmlResource):
    html = """
    <html><body><script>document.write('hello world!');</script></body></html>
    """
    extra_headers = {'X-MyHeader': 'my value', 'Set-Cookie': 'sessionid=ABCD'}


class Http400Resource(HtmlResource):
    status_code = 400
    html = "Website returns HTTP 400 error"


class ManyCookies(Resource, object):
    class SetMyCookie(HtmlResource):
        html = "hello!"
        extra_headers = {'Set-Cookie': 'login=1'}

    def __init__(self):
        super(ManyCookies, self).__init__()
        self.putChild(b'', HelloWorld())
        self.putChild(b'login', self.SetMyCookie())



