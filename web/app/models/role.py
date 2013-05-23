from app import db
from flask.ext.security import RoleMixin

# Define models
roles_users = db.Table('roles_users',
        db.Column('kaizen_user_id', db.Integer(), db.ForeignKey('kaizen_user.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))
