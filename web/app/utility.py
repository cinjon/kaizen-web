import datetime
import urllib
from werkzeug.security import generate_password_hash, check_password_hash
from flask import jsonify, Response

start_date = datetime.datetime(year=1970,month=1,day=1)

def get_time():
    return datetime.datetime.utcnow()

#TODO: turn get_time entries into these.
def get_unixtime(_datetime=None):
    if _datetime:
        return (_datetime - start_date).total_seconds()
    return (datetime.datetime.utcnow() - start_date).total_seconds()

def generate_hash(word):
    return generate_password_hash(word)

def check_hash(stored, request):
    return check_password_hash(stored, request)

def decodeJS(component):
    unquoted = urllib.unquote_plus(component.encode('utf-8'))
    st = unquoted.decode('utf-8')
    st.replace(u'\u2014', u'-') #lolol.
    return st

def xhr_response(data, code):
    response = jsonify(data)
    response.status_code = code
    return response

def xhr_user_login(u, success):
    if success:
        return xhr_response({'bindings':u.get_json_mappings(),
                             'first':u.first, 'last':u.last}, 202)
    return xhr_response({}, 401)

def xhr_user_register(u, success):
    return xhr_user_login(u, success)

def xhr_201(success):
    if success:
        return xhr_response({}, 201)
    return xhr_response({}, 400)

def json_handler(obj):
    if hasattr(obj, 'isoformat'):
        return obj.isoformat()
    else:
        raise TypeError, 'Object of type %s with value of %s is not JSON serializable' % (type(obj), repr(obj))
