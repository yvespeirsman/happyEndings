__author__ = 'yves'

from bottle import run, route, template, request, post, static_file, debug
import os

@route('/')
def start():
    t = template('indexline.html')
    return t

@route('/static/:path#.+#', name='static')
def static(path):
    return static_file(path, root='static')

debug(True)
run(host="0.0.0.0", port = os.environ.get('PORT',5000))