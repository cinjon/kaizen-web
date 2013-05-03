from app import db
from app import utility
import sql

class Site(db.Model):
    #intended use is to disambiguate sites
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.Text, unique=True, index=True)
    creation_time = db.Column(db.DateTime, index=True)
    title = db.Column(db.Text)
    notes = db.relationship('Note', backref='site', lazy='dynamic')
    #TODO: Add another table that has a user-generated nickname for sites

    def update_title(self, title):
        self.title = title

    def __init__(self, url, title):
        self.url = url
        self.title = title
        self.creation_time = utility.get_time()

    def __repr__(self):
        return '%s' % self.title

def create_site(url, title):
    site = Site(url, title)
    sql.add(site)
    return site
