import app
from app import db, utility, messages
import mapping
import sql
from mapping import Mapping
from flask import session, flash
from flask.ext.login import login_user
from sqlalchemy import and_
from flask.ext.security import UserMixin
from role import roles_users

ROLE_USER = 0
ROLE_ADMIN = 1
ROLE_TEST = 2

STATUS_AWAITING_CONFIRMATION = 'awaiting_confirm'
STATUS_ACTIVE = 'active'


class KaizenUser(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first = db.Column(db.String(64)) #Required
    last = db.Column(db.String(64)) #Required
    name = db.Column(db.String(120)) #Should be unique by design, but not set to be here.
    email = db.Column(db.String(120), unique=True, index=True) #Required
    password = db.Column(db.String(100)) #Required
    active = db.Column(db.Boolean())
    creation_time = db.Column(db.DateTime)
    last_login_at = db.Column(db.DateTime())
    current_login_at = db.Column(db.DateTime())
    last_login_ip = db.Column(db.String(100))
    current_login_ip = db.Column(db.String(100))
    login_count = db.Column(db.Integer)
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))
    mappings = db.relationship('Mapping', backref='user', lazy='dynamic')

    def __init__(self, first, last, email, password, roles, active):
        self.first = first
        self.last = last
        self.email = email
        self.active = active
        self.password = self.set_password(password)
        self.creation_time = utility.get_time()
        self.name = self.set_name(first, last)
        self.roles = roles

    def is_authenticated(self):
        #Can the user be logged in in general?
        return True

    def is_active(self):
        #Is this an active account or perhaps banned?
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def set_name(self, first, last):
        name = first + '_' + last
        count = len(KaizenUser.query.filter(and_(KaizenUser.first==first, KaizenUser.last==last)).all())
        if count > 0:
            return name + '' + str(count)
        else:
            return name

    def set_password(self, password):
        return utility.generate_hash(password)

    def check_password(self, password):
        return utility.check_hash(self.password, password)

    def get_current_mappings(self):
        return self.mappings.filter(Mapping.binding > -1).order_by(Mapping.binding)

    def get_json_mappings(self):
        return mapping.json_mappings(self.get_current_mappings())

    def get_all_mappings_in_name_order(self):
        #Display mappings, with bound ones first
        ret = self.get_current_mappings().all()
        [ret.append(m) for m in self.mappings.filter(Mapping.binding < 0).order_by(Mapping.name)]
        return ret

    def set_binding(self, binding, to_mapping):
        to_mapping = utility.decodeJS(to_mapping)
        found_mapping = None
        self.turn_off_mapping_with_binding(binding)
        for m in self.mappings:
            if m.name.lower() == to_mapping.lower():
                found_mapping = m
                break

        if found_mapping:
            found_mapping.set_binding(binding)
        else:
            mapping.create_mapping(self.id, to_mapping, binding)

    def turn_off_mapping_with_binding(self, binding):
        for m in self.mappings.filter(Mapping.binding == binding):
            m.set_binding(-1)

    def add_note(self, data):
        keyCode = None
        if 'keyCode' in data:
            keyCode = int(data['keyCode'])
            m = self.mappings.filter(Mapping.binding == keyCode).first()
        elif 'mapping' in data:
            keyCode = -1 #reps ~
            m = self.mappings.filter(Mapping.name == data['mapping']).first()
        else:
            m = None

        if not m:
            return
        m.add_note(data, keyCode)

    def number_of_notes(self):
        return sum([len(m.notes.all()) for m in self.mappings])

    def __repr__(self):
        return '%s %s' % (self.first, self.last)

def create_user(first, last, email, password, role=ROLE_USER):
    user = KaizenUser(first=first, last=last, email=email, password=password, role=role)
    sql.add(user)
    return user

def user_with_id(id):
    return KaizenUser.query.get(int(id))

def user_with_name(name):
    filtered = KaizenUser.query.filter_by(name=name).all()
    if len(filtered) == 1:
        return filtered[0]
    return None

def user_with_email(email):
    filtered = KaizenUser.query.filter_by(email=email).all()
    if len(filtered) == 1:
        return filtered[0]
    return None

def try_login(email, password, remember_me=True, xhr=False):
    u = user_with_email(email)
    if u and authenticate(u, password):
        session.pop('remember_me', None)
        login_user(u, remember=remember_me)
        if xhr:
            return utility.xhr_user_login(u, True)
    elif xhr:
        return utility.xhr_user_login(u, False)
    return app.views.index.go_to_index()

def authenticate(u, password):
    return u.check_password(password)

def try_register(email, password, first, last, xhr=False):
    if not user_with_email(email):
        app.security_ds.create_user(email=email, password=password, first=first, last=last)
        app.security_ds.commit()
        flash(messages.EMAIL_VALIDATION_SENT, 'info')
    return try_login(email, password, xhr=xhr)

def all_users_sorted_by_note_total():
    users = KaizenUser.query.all()
    return sorted(users, key=lambda x: x.number_of_notes())

