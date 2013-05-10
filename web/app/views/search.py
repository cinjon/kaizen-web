import app
from flask.ext.login import login_required
from flask import g, request

@flask_app.route('/query_maps', methods=['GET'])
@login_required
def query_maps():
    print 'made it to query_maps'
    print request
    print request.form
    return app.utility.xhr_response({'falafel'}, 200)
