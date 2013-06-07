import app
import math
from sqlalchemy import and_

start_visualization_from_blank = True

class Mapping(app.db.Model):
    id = app.db.Column(app.db.Integer, primary_key=True)
    creation_time = app.db.Column(app.db.DateTime)
    name = app.db.Column(app.db.String(120))
    kaizen_user_id = app.db.Column(app.db.Integer, app.db.ForeignKey('kaizen_user.id'), index=True)
    binding = app.db.Column(app.db.SmallInteger)
    notes = app.db.relationship('Note', backref='mapping', lazy='dynamic')

    def set_binding(self, binding):
        self.binding = binding
        app.models.sql.commit()

    def add_note(self, data, keyCode):
        text = app.utility.decodeJS(data['text'])
        title = app.utility.decodeJS(data['title'])
        href = app.utility.decodeJS(data['href'])
        if 'ugn' in data: #TODO: userGeneratedNote
            pass
        app.models.note.create_note(text, title, href, self.id, keyCode)

    def get_all_notes(self):
        return [n for n in self.notes]

    def get_all_sites(self):
        sites = set([n.site for n in self.notes])
        return list(sites)

    def serialize(self, include_notes=False, include_user=False):
        ret = {'id'   : self.id,
               'name' : self.name}
        if include_user:
            ret['uid'] = self.kaizen_user_id
        if include_notes:
            ret['notes'] = [note.serialize() for note in self.notes]
        return ret

    def __init__(self, name, kaizen_user_id, binding):
        self.name = name
        self.kaizen_user_id = kaizen_user_id
        self.binding = binding
        self.creation_time = app.utility.get_time()

    def __repr__(self):
        return self.name

def create_mapping(kaizen_user_id, name, binding=-1):
    mapping = Mapping(name=name, binding=binding, kaizen_user_id=kaizen_user_id)
    app.models.sql.add(mapping)
    return mapping

def json_mappings(maps):
    ret = {}
    for m in maps:
        if m.binding < 0:
            continue
        ret[m.binding] = m.name
    return ret

def mapping_with_userid_and_name(uid, name):
    filtered = Mapping.query.filter(and_(Mapping.name==name, Mapping.kaizen_user_id==uid)).all()
    if len(filtered) == 1:
        return filtered[0]
    return None

def visualize(m):
    if start_visualization_from_blank:
        return visualize_from_null(m)
    else:
        return visualize_from_save(m)

def visualize_alex(m):
    if len(m.notes.all()) == 0:
        return None

    urls = {}
    for n in m.notes:
        s = n.site
        if s.url not in urls:
            urls[s.url] = {'title':s.title,
                           'start_time':app.utility.get_unixtime(n.creation_time)}
        urls[s.url].setdefault('notes', []).append(
            {'time':app.utility.get_unixtime(n.creation_time), 'text':n.text})

    time_sorted_urls = sorted(urls.iteritems(), key=lambda (k,v): v['start_time'])
    latest_time = time_sorted_urls[1][1]['start_time']

    ret = []
    for url in time_sorted_urls:
        ret.append({'url':url[0], 'title':url[1]['title'], 'notes':url[1]['notes'],
                    'radii':(latest_time - url[1]['start_time']) + 60})
    return ret

def visualize_from_null(m):
    line_weight = 5 #1-10 (noninteger fine)
    node_weight = 5 #1-10 (noninteger fine)
    width = 1050
    height = 600
    root_id = app.utility.generate_id()
    root_distance = max(width/5, height/5)
    root_position = (width/2, height/2)
    root_radius   = max(node_weight*6, min(math.sqrt(width), math.sqrt(height)))
    note_distance = root_distance / 3
    note_radius   = root_radius * 2 / 5
    vis = {'mapping':m.serialize(include_notes=False), 'root':_make_node(root_position, root_radius, _id=root_id)}

    sites = m.get_all_sites()
    if len(sites) == 0:
        return vis
    else:
        vis['links'] = []
        vis['sites'] = {}
        vis['notes'] = {}

    angle_s = 2 * math.pi / len(sites)
    for i, site in enumerate(sites):
        angle_spos = i * angle_s
        scx = root_position[0] + math.cos(angle_spos) * (root_radius + root_distance)
        scy = root_position[1] + math.sin(angle_spos) * (root_radius + root_distance)
        sid = app.utility.generate_id()
        vis['sites'][sid] = _make_node((scx, scy), root_radius, site=site.serialize())
        vis['links'].append((root_id, root_position[0], root_position[1],
                             sid, scx, scy, line_weight))

        notes = site.notes.all()
        if len(notes) > 0:
            angle_n = 2 * angle_s / len(notes)
            for j, note in enumerate(notes):
                angle_counter = 0
                angle_npos = angle_spos + angle_n * j - angle_s/2
                ncx = -1
                ncy = -1
                while (ncx < 0 or ncx > width or ncy < 0 or ncy > height):
                    ncx = scx + math.cos(angle_npos - angle_spos * angle_counter) * (root_radius + note_distance)
                    ncy = scy + math.sin(angle_npos - angle_spos * angle_counter) * (root_radius + note_distance)
                    angle_counter += 1
                nid = app.utility.generate_id()
                vis['notes'][nid] = _make_node((ncx, ncy), note_radius, note=note.serialize())
                vis['links'].append((sid, scx, scy,
                                     nid, ncx, ncy, line_weight))
    return vis

def visualize_from_save(m):
    #TODO
    return {}

def _make_node(position, radius, **kwargs):
    node = {'position':position, 'radius':radius}
    for key, value in kwargs.items():
        node[key] = value
    return node




