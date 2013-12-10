import app
import math
from sqlalchemy import and_

class Mapping(app.db.Model):
    id = app.db.Column(app.db.Integer, primary_key=True)
    creation_time = app.db.Column(app.db.DateTime)
    name = app.db.Column(app.db.String(120))
    name_route = app.db.Column(app.db.String(140))
    kaizen_user_id = app.db.Column(app.db.Integer, app.db.ForeignKey('kaizen_user.id'), index=True)
    binding = app.db.Column(app.db.SmallInteger)
    notes = app.db.relationship('Note', backref='mapping', lazy='dynamic')
    deleted = app.db.Column(app.db.Boolean)

    def __init__(self, name, kaizen_user_id, binding, deleted=False):
        self.name = name.title()
        self.kaizen_user_id = kaizen_user_id
        self.binding = binding
        self.creation_time = app.utility.get_time()
        self.deleted = deleted
        self.name_route = app.models.kaizen_user.dashify_name(self.name)

    def set_binding(self, binding):
        self.binding = binding
        app.models.sql.commit()

    def add_note(self, data, keyCode):
        text = app.utility.decodeJS(data['text'])
        title = app.utility.decodeJS(data['title'])
        href = app.utility.decodeJS(data['href'])
        app.models.note.create_note(text, title, href, self.id, keyCode)

    def get_all_live_notes(self):
        return [n for n in self.notes if n.deleted==False]

    def get_all_live_sites(self):
        return list(set([n.site for n in self.notes if n.deleted==False]))

    def has_notes(self):
        for n in self.notes.filter(app.models.note.Note.deleted==False):
            return True
        return False

    def time_descending_notes(self, limit=10):
        return self.notes.filter(
            app.models.note.Note.deleted==False).order_by(
            app.models.note.Note.creation_time.desc()).limit(limit)

    def last_note_time(self):
        for n in self.time_descending_notes(1):
            return n.creation_time
        return app.utility.start_date

    def serialize(self, include_notes=False, include_user=False):
        ret = {'mid'   : self.id,
               'name' : self.name}
        if include_user:
            ret['uid'] = self.kaizen_user_id
        if include_notes:
            ret['notes'] = [note.serialize() for note in self.notes]
        return ret

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

def mapping_with_userid(uid):
    return Mapping.query.filter(Mapping.kaizen_user_id==uid).all()

def mapping_with_userid_and_name(uid, name):
    filtered = [m for m in mapping_with_userid(uid) if m.name and  m.name.lower() == name.lower()]
    if len(filtered) == 1:
        return filtered[0]
    return None

def mapping_with_userid_and_name_route(uid, name_route):
    filtered = [m for m in mapping_with_userid(uid) if m.name_route and m.name_route.lower() == name_route.lower()]
    if len(filtered) == 1:
        return filtered[0]
    return None

def mapping_with_id(id):
    return Mapping.query.get(id)

def visualize(m):
    v = app.models.visualization.visualization_with_id(m.id)
    if v:
        return visualize_from_save(v)
    else:
        return visualize_from_null(m)

def visualize_from_null(m):
    width = 1050
    height = 600
    root_id = app.utility.generate_id()
    root_distance = max(width/5, height/5)
    root_x = width/2
    root_y = height/2
    root_r = max(40, min(math.sqrt(width), math.sqrt(height)))
    site_r = root_r - 10
    note_distance = root_distance / 4
    note_r   = site_r * 2 / 5

    #****#
    v = app.models.visualization.create_visualization(m.id)
    ret = v.serialize() #building along here because otherwise we'll have to loop down everything twice, once to build the nodes, the other to build the return
    root_node = app.models.node.create_node(vid=m.id, x=root_x, y=root_y, radius=root_r,
                                            node_type=app.models.node.NodeTypes.MAPPING,
                                            node_type_id=m.id)
    ret['root'] = root_node.serialize()

    sites = m.get_all_live_sites()
    if len(sites) == 0:
        return ret
    else:
        ret['links'] = []
        ret['sites'] = {}
        ret['notes'] = {}

    angle_s = 2 * math.pi / len(sites)
    for i, site in enumerate(sites):
        angle_spos = i * angle_s
        scx = root_x + math.cos(angle_spos) * (root_r + root_distance)
        scy = root_y + math.sin(angle_spos) * (root_r + root_distance)

        site_node = app.models.node.create_node(vid=m.id, x=scx, y=scy, radius=site_r,
                                                node_type=app.models.node.NodeTypes.SITE,
                                                node_type_id=site.id)
        ret['sites'][site_node.dom_id] = site_node.serialize()
        link = app.models.link.create_link(start_nid=root_node.id,
                                           end_nid=site_node.id, vid=m.id)
        ret['links'].append(link.serialize())

        notes = site.notes.all()
        if len(notes) > 0:
            angle_n = 2 * angle_s / len(notes)
            for j, note in enumerate(notes):
                angle_counter = 0
                angle_npos = angle_spos + angle_n * j - angle_s/2
                ncx = -1
                ncy = -1
                while (ncx < 0 or ncx > width or ncy < 0 or ncy > height):
                    ncx = scx + math.cos(angle_npos - angle_spos * angle_counter) * (site_r + note_distance)
                    ncy = scy + math.sin(angle_npos - angle_spos * angle_counter) * (site_r + note_distance)
                    angle_counter += 1

                note_node = app.models.node.create_node(vid=m.id, x=ncx, y=ncy, radius=note_r,
                                                        node_type=app.models.node.NodeTypes.NOTE,
                                                        node_type_id=note.id)
                link = app.models.link.create_link(start_nid=site_node.id,
                                                   end_nid=note_node.id, vid=m.id)
                ret['notes'][note_node.dom_id] = note_node.serialize()
                ret['links'].append(link.serialize())
    return ret

def visualize_from_save(v):
    return v.serialize_recursively()
