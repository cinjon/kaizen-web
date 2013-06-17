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

    def update_node_state(self, notes, sites, root, links):
        print links
        for link_dom_id in links['del']:
            self._delete_link(link_dom_id)
        for link_dom_id in links['add']:
            self._add_link(link_dom_id)
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
            if state == 'deleted':
                node.delete()
            else:
                node.update_coordinates(state)

    def _delete_link(self, link_dom_id):
        node_dom_ids = link_dom_id.split('_')
        start_node = app.models.node.node_with_dom_id_and_vid(node_dom_ids[0], self.id)
        end_node = app.models.node.node_with_dom_id_and_vid(node_dom_ids[1], self.id)
        link = app.models.link.link_with_nids(start_node.id, end_node.id)
        if link:
            link.delete()

    def _add_link(self, link_dom_id):
        node_dom_ids = link_dom_id.split('_')
        app.models.link.create_link(
            app.models.node.node_with_dom_id_and_vid(node_dom_ids[0], self.id).id,
            app.models.node.node_with_dom_id_and_vid(node_dom_ids[1], self.id).id,
            self.id)

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
