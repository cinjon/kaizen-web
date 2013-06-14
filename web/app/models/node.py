import app
from sqlalchemy import and_
import random

NodeTypes = app.utility.enum(MAPPING=1, SITE=2, NOTE=3)

class Node(app.db.Model):
    id = app.db.Column(app.db.Integer, primary_key=True)
    x = app.db.Column(app.db.Integer)
    y = app.db.Column(app.db.Integer)
    vid = app.db.Column(app.db.Integer, app.db.ForeignKey('visualization.id'), index=True)
    radius = app.db.Column(app.db.Integer)
    node_type = app.db.Column(app.db.SmallInteger)
    dom_id = app.db.Column(app.db.VARCHAR(6))
    node_type_id = app.db.Column(app.db.Integer) #either a nid, a sid, or a mid

    def __init__(self, vid, x, y, radius, node_type, node_type_id):
        self.x = x
        self.y = y
        self.vid = vid
        self.radius = radius
        self.dom_id = app.utility.generate_id() #random id for the dom, should be s.t. (vid, dom_id) is a unique pairing ... add that later
        self.node_type = node_type
        self.node_type_id = node_type_id

    def serialize(self):
        return {'position':(self.x, self.y), 'radius':self.radius}

    def __repr__(self):
        return '(%d, %d) - %s' % (self.x, self.y, self.node_type)

def create_node(vid, x, y, radius, node_type, node_type_id):
    node = Node(vid, x, y, radius, node_type, node_type_id)
    app.models.sql.add(node)
    return node

def post_visualized_create_note_node(vid, note):
    vis = app.models.visualization.Visualization.query.get(vid)
    print vis
    if vis:
        site_node = Node.query.filter(and_(Node.node_type==NodeTypes.SITE,
                                           Node.node_type_id==note.site_id)).first()
        if not site_node:
            site_node = _post_visualized_create_site_node(vis, note.site_id)
        note_node = _post_visualized_create_note_node(vis, note.id, site_node)
        root_id = vis.nodes.filter(Node.node_type==1).first().id
        app.models.link.create_link(site_node.id, note_node.id, vid)
        app.models.link.create_link(root_id, site_node.id, vid)

def _get_radius(vis, node_type):
    return min([n.radius for n in vis.nodes if n.node_type==node_type])

def _post_visualized_create_note_node(vis, nid, site_node):
    radius = _get_radius(vis, NodeTypes.NOTE)
    #put it down at a location reasonably close to its site.
    #rely on JS to fix overlaps
    x = site_node.x + site_node.radius + radius + 55;
    y = site_node.y
    return create_node(vid=vis.id, x=x, y=y, radius=radius,
                       node_type=NodeTypes.NOTE, node_type_id=nid)

def _post_visualized_create_site_node(vis, sid):
    radius = _get_radius(vis, NodeTypes.SITE)
    #put it down at a random location reasonably close to the top.
    #rely on JS to fix overlaps
    x = radius + (radius * random.randint(1, 20) / 2)
    y = radius + radius / 2
    return create_node(vid=vis.id, x=x, y=y, radius=radius,
                       node_type=NodeTypes.SITE, node_type_id=sid)


