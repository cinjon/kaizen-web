import app

class Note(app.db.Model):
    id = app.db.Column(app.db.Integer, primary_key=True)
    text = app.db.Column(app.db.Text)
    url = app.db.Column(app.db.Text)
    creation_time = app.db.Column(app.db.DateTime, index=True)
    binding = app.db.Column(app.db.SmallInteger)
    mapping_id = app.db.Column(app.db.Integer, app.db.ForeignKey('mapping.id'), index=True)
    site_id = app.db.Column(app.db.Integer, app.db.ForeignKey('site.id'), index=True)
    deleted = app.db.Column(app.db.Boolean)
    name = app.db.Column(app.db.String(120))

    def __init__(self, binding, mapping_id, text=None, title=None, url=None, deleted=False, name=None):
        self.text = text
        self.url = url
        self.binding = binding
        self.mapping_id = mapping_id
        self.site_id = self.set_site_id(url, title)
        self.creation_time = app.utility.get_time()
        self.deleted = deleted
        self.name = name

    def set_site_id(self, url, title):
        s = app.models.site.Site.query.filter(app.models.site.Site.url == url).first()
        if s:
            s.update_title(title)
            return s.id
        else:
            return app.models.site.create_site(url, title).id

    def serialize(self, include_site=True, include_map=False):
        ret = {}
        ret['name'] = self.name
        ret['nid'] = self.id
        ret['text'] = self.text
        ret['url'] = self.url
        ret['creation_time'] = app.utility.serialize_datetime(self.creation_time)
        if include_site:
            ret['sid'] = self.site_id
        if include_map:
            ret['mid'] = self.mapping_id
        return ret

    def my_mapping(self):
        return app.models.mapping.Mapping.query.get(self.mapping_id)

    def short_title(self):
        title = self.site.title
        if len(title) > 60:
            return title[:57] + '...'
        return title

    def delete(self):
        self.deleted = True

    def __unicode__(self):
        if len(self.text) > 50:
            return u"%s..." % self.text[:47]
        return u"%s" % self.text

def create_note(text, title, url, mapping_id, binding=-1):
    note = Note(text=text, title=title, url=url,
                mapping_id=mapping_id, binding=binding)
    app.models.sql.add(note)
    app.models.node.post_visualized_create_note_node(mapping_id, note)
    return note

def note_with_id(id):
    return Note.query.get(id)
