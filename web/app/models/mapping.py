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

def visualize_from_null(m):
    line_weight = 5 #1-10 (noninteger fine)
    node_weight = 5 #1-10 (noninteger fine)
    width = 1050
    height = 600
    root_distance = max(width/5, height/5)
    root_position = (width/2, height/2)
    root_radius   = max(node_weight*6, min(math.sqrt(width), math.sqrt(height)))
    note_distance = root_distance / 3
    note_radius   = root_radius * 2 / 5
    vis = {'mapname':m.name, 'root':_make_node(root_position, root_radius)}

    sites = m.get_all_sites()
    if len(sites) == 0:
        return visualization
    else:
        vis['site_links'] = {} #maintain this in alphabetical ordering
        vis['note_links'] = {}

    angle_s = 2 * math.pi / len(sites)
    for i, site in enumerate(sites):
        angle_spos = i * angle_s
        scx = root_position[0] + math.cos(angle_spos) * (root_radius + root_distance)
        scy = root_position[1] + math.sin(angle_spos) * (root_radius + root_distance)
        s_id = 'site_id_' + str(i)
        vis[s_id] = _make_node((scx, scy), root_radius, url=site.url, title=site.title)
        vis['site_links']['site_id_root' + '   ' + s_id] = line_weight

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
                n_id = 'note_id_' + str(i) + '_' + str(j)
                vis[n_id] = _make_node((ncx, ncy), note_radius, text=note.text, site=i,
                                       time=app.utility.get_unixtime(note.creation_time))
                vis['note_links'][s_id + '   ' + n_id] = line_weight
    return vis

def visualize_from_save(m):
    #TODO
    return {}

def _make_node(position, radius, **kwargs):
    node = {'position':position, 'radius':radius}
    for key, value in kwargs.items():
        node[key] = value
    return node
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






