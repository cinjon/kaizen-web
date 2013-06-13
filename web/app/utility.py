import datetime
import urllib
import random
import string
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

def serialize_datetime(_datetime):
    if _datetime is None:
        return None
    return _datetime.strftime("%Y-%m-%d")

def generate_hash(word):
    return generate_password_hash(word)

def check_hash(stored, request):
    return check_password_hash(stored, request)

def decodeJS(component):
    unquoted = urllib.unquote_plus(component.encode('utf-8'))
    st = unquoted.decode('utf-8')
    return unicode_replace(st)

def xhr_response(data, code):
    response = jsonify(data)
    response.status_code = code
    return response

def xhr_user_login(u, success):
    if success:
        return xhr_response({'bindings':u.get_json_mappings(),
                             'accountName':u.name}, 202)
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

def short_text(txt, length, replace):
    if len(txt) > length:
        return txt[:(length - len(replace))]
    return txt

def unicode_replace(txt):
    #this is fucking silly
    txt.replace(u'\u2019', u"'")
    txt.replace(u'\u201c', u'"')
    txt.replace(u'\u201d', u'"')
    txt.replace(u'\u2014', u'-')
    return txt

def generate_id(size=6):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(size))

def enum(**enums):
    return type('Enum', (), enums)
