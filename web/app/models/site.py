import app

class Site(app.db.Model):
    #intended use is to disambiguate sites
    id = app.db.Column(app.db.Integer, primary_key=True)
    url = app.db.Column(app.db.Text, unique=True, index=True)
    creation_time = app.db.Column(app.db.DateTime, index=True)
    title = app.db.Column(app.db.Text)
    notes = app.db.relationship('Note', backref='site', lazy='dynamic')
    deleted = app.db.Column(app.db.Boolean)
    name = app.db.Column(app.db.String(120))

    def __init__(self, url, title, name=None, deleted=False):
        self.url = url
        self.title = title
        self.name = name
        self.creation_time = app.utility.get_time()
        self.deleted = deleted

    def update_title(self, title):
        self.title = title

    def short_title(self):
        if len(self.title) > 40:
            return self.title[:37] + '...'
        return self.title

    def notes_in_chrono_order(self):
        return [n for n in self.get_all_live_notes().order_by(
            app.models.note.Note.creation_time.desc())]

    def serialize(self):
        return {'sid'           : self.id,
                'url'           : self.url,
                'title'         : self.title,
                'name'          : self.name,
                'creation_time' : app.utility.serialize_datetime(self.creation_time)}

    def has_notes(self):
        for n in self.notes.filter(app.models.note.Note.deleted==False):
            return True
        return False

    def num_notes(self):
        return self.get_all_live_notes().count()

    def get_all_live_notes(self):
        return self.notes.filter(app.models.note.Note.deleted==False)

    def delete(self, defer=False):
        self.deleted = True
        if not defer:
            app.models.sql.commit()

def create_site(url, title):
    site = Site(url, title)
    app.models.sql.add(site)
    return site

def site_with_id(id):
    return Site.query.get(id)
