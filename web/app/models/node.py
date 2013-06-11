import app

NodeType = app.utility.enum(NOTE=1, SITE=2, ROOT=3)

class Node(app.db.Model):
    id = app.db.Column(app.db.Integer, primary_key=True)
    x = app.db.Column(app.db.Integer)
    y = app.db.Column(app.db.Integer)
    ty = app.db.Column(app.db.SmallInteger)
    vid = app.db.Column(app.db.Integer, app.db.ForeignKey('visualization.id'), index=True)

    def __init__(self, vid, ty, x, y):
        self.x = x
        self.y = y
        self.vid = vid
        self.ty = ty

def create_node(vid, ty, x, y):
    node = Node(vid, ty, x, y)
    app.models.sql.add(node)
    return node
