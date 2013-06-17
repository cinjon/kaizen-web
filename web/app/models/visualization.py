import app

class Visualization(app.db.Model):
    id = app.db.Column(app.db.Integer, app.db.ForeignKey('mapping.id'), primary_key=True)
    nodes = app.db.relationship('Node', backref='visualization', lazy='dynamic')
    links = app.db.relationship('Link', backref='visualization', lazy='dynamic')
    last_save_time = app.db.Column(app.db.DateTime)

    def __init__(self, id):
        self.id = id
        self.last_save_time = app.utility.get_time()

    def serialize(self):
        return {'mapping':app.models.mapping.mapping_with_id(self.id).serialize(include_notes=False)}

    def serialize_recursively(self):
        ret = self.serialize()
        ret['links'] = [link.serialize() for link in self.links]
        ret['sites'] = {}
        ret['notes'] = {}
        for node in self.nodes:
            ser = node.serialize()
            if node.node_type == app.models.node.NodeTypes.NOTE:
                ser['note'] = app.models.note.Note.query.get(node.node_type_id).serialize()
                ret['notes'][node.dom_id] = ser
            elif node.node_type == app.models.node.NodeTypes.SITE:
                ser['site'] = app.models.site.Site.query.get(node.node_type_id).serialize()
                ret['sites'][node.dom_id] = ser
            elif node.node_type == app.models.node.NodeTypes.MAPPING:
                ser['_id'] = node.dom_id
                ret['root'] = ser
        return ret

    def update_node_state(self, notes, sites, root):
        for dom_id, state in notes.iteritems():
            self._update_node_state(dom_id, state)
        for dom_id, state in sites.iteritems():
            self._update_node_state(dom_id, state)
        for dom_id, state in root.iteritems():
            self._update_node_state(dom_id, state)
        app.models.sql.commit()

    def _update_node_state(self, dom_id, state):
        node = app.models.node.node_with_dom_id_and_vid(dom_id, self.id)
        if node:
            node.x = int(state['x'])
            node.y = int(state['y'])
            return True
        return False

    def __repr__(self):
        return '%d %s' % (self.id, self.last_save_time)

def create_visualization(id):
    vis = Visualization(id)
    app.models.sql.add(vis)
    return vis

def visualization_with_id(id):
    filtered = Visualization.query.filter_by(id=id).all()
    if len(filtered) == 1:
        return filtered[0]
    return None
