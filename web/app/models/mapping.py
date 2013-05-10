from app import db
from app import utility
import sql
import user
import note
import site
from sqlalchemy import and_
import operator

class Mapping(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    creation_time = db.Column(db.DateTime)
    name = db.Column(db.String(120))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), index=True)
    binding = db.Column(db.SmallInteger)
    notes = db.relationship('Note', backref='mapping', lazy='dynamic')

    def set_binding(self, binding):
        self.binding = binding
        sql.commit()

    def add_note(self, data, keyCode):
        text = utility.decodeJS(data['text'])
        title = utility.decodeJS(data['title'])
        href = utility.decodeJS(data['href'])
        if 'ugn' in data: #TODO: userGeneratedNote
            pass
        note.create_note(text, title, href, self.id, keyCode)

    def get_all_notes(self):
        return [n for n in self.notes]

    def get_all_sites(self):
        sites = set([n.site for n in self.notes])
        return list(sites)

    def __init__(self, name, user_id, binding):
        self.name = name
        self.user_id = user_id
        self.binding = binding
        self.creation_time = utility.get_time()

    def __repr__(self):
        return self.name

def create_mapping(user_id, name, binding=-1):
    mapping = Mapping(name=name, binding=binding, user_id=user_id)
    sql.add(mapping)
    return mapping

def json_mappings(maps):
    ret = {}
    for m in maps:
        if m.binding < 0:
            continue
        ret[m.binding] = m.name
    return ret

def mapping_with_userid_and_name(uid, name):
    filtered = Mapping.query.filter(and_(Mapping.name==name, Mapping.user_id==uid)).all()
    if len(filtered) == 1:
        return filtered[0]
    return None

def visualize(m):
    if len(m.notes.all()) == 0:
        return None

    urls = {}
    for n in m.notes:
        s = n.site
        if s.url not in urls:
            urls[s.url] = {'title':s.title,
                           'start_time':utility.get_unixtime(n.creation_time)}
        urls[s.url].setdefault('notes', []).append(
            {'time':utility.get_unixtime(n.creation_time), 'text':n.text})

    time_sorted_urls = sorted(urls.iteritems(), key=lambda (k,v): v['start_time'])
    latest_time = time_sorted_urls[-1][1]['start_time']

    ret = []
    for url in time_sorted_urls:
        ret.append({'url':url[0], 'title':url[1]['title'], 'notes':url[1]['notes'],
                    'radii':(latest_time - url[1]['start_time']) + 60})
    return ret

def test_visualize(mapname):
    #time should be real time as well. That needs to be displayed.
    return {"sites":[{"notes":[{"text":"qclub and shit lot of costs, etc", "time":100},
                              {"text":"a note on avocadoes", "time":120}],
                     "title":"This is a node",
                     "url":"http://url.com"},
                     {"notes":[{"text":"other note", "time":70},
                               {"text":"second note", "time":150}],
                      "title":"a second node",
                      "url":"2.url.com"}],
            "mapname":mapname}






