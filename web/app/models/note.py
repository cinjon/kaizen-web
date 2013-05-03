from app import db
from app import utility
import sql
import mapping
import site

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text)
    url = db.Column(db.Text)
    creation_time = db.Column(db.DateTime, index=True)
    binding = db.Column(db.SmallInteger)
    mapping_id = db.Column(db.Integer, db.ForeignKey('mapping.id'), index=True)
    site_id = db.Column(db.Integer, db.ForeignKey('site.id'), index=True)

    def set_site_id(self, url, title):
        s = site.Site.query.filter(site.Site.url == url).first()
        if s:
            s.update_title(title)
            return s.id
        else:
            return site.create_site(url, title).id

    def __init__(self, binding, mapping_id, text=None, title=None, url=None):
        self.text = text
        self.url = url
        self.binding = binding
        self.mapping_id = mapping_id
        self.site_id = self.set_site_id(url, title)
        self.creation_time = utility.get_time()

    def __repr__(self):
        if len(self.text) > 50:
            return self.text[:47] + '...'
        return self.text

def create_note(text, title, url, mapping_id, binding=-1):
    note = Note(text=text, title=title, url=url,
                mapping_id=mapping_id, binding=binding)
    sql.add(note)
