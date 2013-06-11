import app

class Link(app.db.Model):
    id = app.db.Column(app.db.Integer, primary_key=True)
    start_nid = app.db.Column(app.db.Integer, app.db.ForeignKey('node.id'), index=True)
    end_nid   = app.db.Column(app.db.Integer, app.db.ForeignKey('node.id'), index=True)
    vid    = app.db.Column(app.db.Integer, app.db.ForeignKey('visualization.id'), index=True)

    def __index__(start_nid, end_nid, vid):
        self.start_nid = start_nid
        self.end_nid   = end_nid
        self.vid = vid

def create_link(start_nid, end_nid, vis_id):
    link = Link(start_nid, end_nid, vis_id)


