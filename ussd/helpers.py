from flask import Response
def make_con(text):
    return Response("CON " + text, mimetype='text/plain')

def make_end(text):
    return Response("END " + text, mimetype='text/plain')
