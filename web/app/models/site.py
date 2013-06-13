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

    def serialize(self):
        return {'sid'           : self.id,
                'url'           : self.url,
                'title'         : self.title,
                'name'          : self.name,
                'creation_time' : app.utility.serialize_datetime(self.creation_time)}

def create_site(url, title):
    site = Site(url, title)
    app.models.sql.add(site)
    return site
