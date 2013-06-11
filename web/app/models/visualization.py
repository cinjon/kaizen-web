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
        pass

def create_visualization(id):
    vis = Visualization(id)
    app.models.sql.add(vis)

def visualization_with_id(id):
    filtered = Visualization.query.filter_by(id=id).all()
    if len(filtered) == 1:
        return filtered[0]
    return None
