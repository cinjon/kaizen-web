import app

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

def create_node(vid, x, y, radius, node_type, node_type_id):
    node = Node(vid, x, y, radius, node_type, node_type_id)
    app.models.sql.add(node)
    return node
