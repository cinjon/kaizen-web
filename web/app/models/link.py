import app
from sqlalchemy import and_

class Link(app.db.Model):
    id = app.db.Column(app.db.Integer, primary_key=True)
    start_nid = app.db.Column(app.db.Integer, app.db.ForeignKey('node.id'), index=True)
    end_nid   = app.db.Column(app.db.Integer, app.db.ForeignKey('node.id'), index=True)
    vid    = app.db.Column(app.db.Integer, app.db.ForeignKey('visualization.id'), index=True)

    def __init__(self, start_nid, end_nid, vid):
        self.start_nid = start_nid
        self.end_nid   = end_nid
        self.vid = vid

    def serialize(self):
        start_node = app.models.node.Node.query.get(self.start_nid)
        end_node   = app.models.node.Node.query.get(self.end_nid)
        return (start_node.dom_id, start_node.x, start_node.y,
                end_node.dom_id, end_node.x, end_node.y)

    def delete(self):
        app.models.sql.delete(self)

def create_link(start_nid, end_nid, vid):
    link = Link(start_nid, end_nid, vid)
    app.models.sql.add(link)
    return link

def link_with_nids(start_nid, end_nid):
    return Link.query.filter(and_(Link.start_nid==start_nid, Link.end_nid==end_nid)).first()
