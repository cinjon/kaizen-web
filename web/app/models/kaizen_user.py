import app
from flask import session, flash
from flask.ext.login import login_user
from flask.ext.security.utils import verify_and_update_password
from flask.ext.security import UserMixin
from app.models.role import roles_users

ROLE_USER = 0
ROLE_ADMIN = 1
ROLE_TEST = 2

class KaizenUser(app.db.Model, UserMixin):
    id = app.db.Column(app.db.Integer, primary_key=True)
    name = app.db.Column(app.db.String(120))
    name_route = app.db.Column(app.db.String(140))
    email = app.db.Column(app.db.String(120), unique=True, index=True) #Required
    password = app.db.Column(app.db.String(120)) #Required
    active = app.db.Column(app.db.Boolean())
    creation_time = app.db.Column(app.db.DateTime)
    last_login_at = app.db.Column(app.db.DateTime())
    current_login_at = app.db.Column(app.db.DateTime())
    last_login_ip = app.db.Column(app.db.String(100))
    current_login_ip = app.db.Column(app.db.String(100))
    login_count = app.db.Column(app.db.Integer)
    confirmed_at = app.db.Column(app.db.DateTime())
    roles = app.db.relationship('Role', secondary=roles_users,
                            backref=app.db.backref('users', lazy='dynamic'))
    mappings = app.db.relationship('Mapping', backref='user', lazy='dynamic')

    def __init__(self, name, email, password, roles, active):
        self.email = email
        self.name = name
        self.active = active
        self.password = password
        self.creation_time = app.utility.get_time()
        self.roles = roles
        self.name_route = self.set_name_route(name)

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

    def set_name_route(self, name):
        count = KaizenUser.query.filter(KaizenUser.name==name).count()
        name = dashify_name(name)
        if count > 0:
            name = name + '-' + str(count)
        return name

    def check_password(self, password):
        return verify_and_update_password(password, self)

    def get_current_mappings(self):
        return self.mappings.filter(app.models.mapping.Mapping.binding > -1).order_by(app.models.mapping.Mapping.binding)

    def get_json_mappings(self):
        return app.models.mapping.json_mappings(self.get_current_mappings())

    def get_all_mappings_in_name_order(self):
        #Display mappings, with bound ones first
        ret = self.get_current_mappings().all()
        [ret.append(m) for m in self.mappings.filter(app.models.mapping.Mapping.binding < 0).order_by(app.models.mapping.Mapping.name)]
        return ret

    def get_all_mappings_in_notes_order(self):
        return sorted(self.mappings, key=lambda m: len(m.get_all_notes()), reverse=True)

    def set_binding(self, binding, to_mapping):
        to_mapping = app.utility.decodeJS(to_mapping)
        found_mapping = None
        self.turn_off_mapping_with_binding(binding)
        for m in self.mappings:
            if m.name.lower() == to_mapping.lower():
                found_mapping = m
                break

        if found_mapping:
            found_mapping.set_binding(binding)
        else:
            app.models.mapping.create_mapping(self.id, to_mapping, binding)

    def turn_off_mapping_with_binding(self, binding):
        for m in self.mappings.filter(app.models.mapping.Mapping.binding == binding):
            m.set_binding(-1)

    def add_note(self, data):
        keyCode = None
        if 'keyCode' in data:
            keyCode = int(data['keyCode'])
            m = self.mappings.filter(app.models.mapping.Mapping.binding == keyCode).first()
        elif 'mapping' in data:
            keyCode = -1 #reps ~
            m = self.mappings.filter(app.models.mapping.Mapping.name == data['mapping']).first()
        else:
            m = None

        if not m:
            return
        m.add_note(data, keyCode)

    def number_of_notes(self):
        return sum([len(m.notes.all()) for m in self.mappings])

    def recent_notes(self, limit=10):
        notes = []
        for m in self.mappings:
            for n in m.notes.filter(
                not(app.models.note.Note.text == '')).order_by(
                app.models.note.Note.creation_time.desc()).limit(limit):
                notes.append(n)
        return sorted(notes, key=lambda n: n.creation_time, reverse=True)[:limit]

    def __repr__(self):
        return self.name

def user_with_id(id):
    return KaizenUser.query.get(int(id))

def user_with_name_route(name_route):
    filtered = KaizenUser.query.filter_by(name_route=name_route).all()
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
            return app.utility.xhr_user_login(u, True)
    elif xhr:
        return app.utility.xhr_user_login(u, False)
    return app.views.index.go_to_index()

def authenticate(u, password):
    return u.check_password(password)

def try_register(email, password, name, xhr=False):
    if not user_with_email(email):
        app.security_ds.create_user(email=email, password=password, name=name)
        app.security_ds.commit()
        flash(app.messages.EMAIL_VALIDATION_SENT, 'info')
    return try_login(email, password, xhr=xhr)

def all_users_sorted_by_note_total():
    users = KaizenUser.query.all()
    return sorted(users, key=lambda x: x.number_of_notes())

def dashify_name(name):
    parts = [p for p in name.strip().split(' ') if not(p=='')]
    ret = '-'.join(parts).replace('.', '-')
    return ret
