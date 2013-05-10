import app
from flask.ext.login import login_required
from flask import g, request

@app.flask_app.route('/query/<params>', methods=['GET'])
@login_required
def query(params):
    print 'made it to query_maps, %s' % params
    print request
    print request.form
    return app.utility.xhr_response({'data':['falafel', 'hummus']}, 200)
