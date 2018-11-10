#!/bin/env python
# -*- coding: utf-8 -*-
#
# http://steavevaivai.hatenablog.com/entry/2015/05/17/144240
#
from __future__ import print_function
import sys
import os
import tornado.httpserver
import tornado.ioloop
import tornado.iostream
import tornado.web
import tornado.httpclient
import ssl

class ProxyHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self):
        return self.myRequest()

    @tornado.web.asynchronous
    def post(self):
        return self.myRequest()

    def myRequest(self):
        #self.render("test.html")
        def get_response( response):
            if response.error and not isinstance(response.error,tornado.httpclient.HTTPError):
                self.set_status(500)
                self.write('500 error:\n' + str(response.error))
                self.finish()
            else:
                self.set_status(response.code)
                for header in ('Date', 'Cache-Control', 'Server', 'Content-Type', 'Location'):
                    v = response.headers.get(header)
                    if v:
                        self.set_header(header, v)
                if response.body:
                    print(self.request.uri)
                    #self.write(response.body.replace("<body".encode("utf-8"), "<script type='text/javascript'>(function(){alert('hello');})();</script><body".encode("utf-8")))
                    self.write(response.body)

                    #self.render(response.body)
                self.finish()

        req = tornado.httpclient.HTTPRequest(
            url=self.request.uri,
            method=self.request.method, body=self.request.body,
            headers=self.request.headers,
            follow_redirects=False,
            allow_nonstandard_methods=True)
        client = tornado.httpclient.AsyncHTTPClient()
        try:
            #コールバック関数にhandle_responseを指定。ここにアクセスしたレスポンスが入る
            client.fetch(req, get_response)
        except tornado.httpclient.HTTPError as e:
            if hasattr(e, 'response') and e.response:
                get_response(e.response)
            else:
                self.set_status(500)
                self.write('500 error:\n' + str(e))
                self.finish()

def run_proxy(port):
    app = tornado.web.Application(
        [(r'.*', ProxyHandler),]
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(port)

    print("Server is up ...")
    tornado.ioloop.IOLoop.instance().start() #プロキシサーバを稼働させる

if __name__ == "__main__":
    port = 8888
    if len(sys.argv) > 1:
        port = int(sys.argv[1])

    print ("Starting cache proxy on port %d" % port)
    run_proxy(port)
    #run_ssl_proxy(8888)
