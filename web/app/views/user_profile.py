from app import flask_app
from app.models import kaizen_user, mapping
from flask import g, render_template, redirect, flash, url_for
from flask.ext.login import login_required


@flask_app.route('/me', endpoint='me')
@login_required
def owner_profile():
    mappings = view_mappings(g.user)
    allmaps = summarize_maps(mappings)
    allmaps['notes'] = view_notes(g.user, 5)
    return render_template('user_profile.html', user=g.user, mappings=mappings, allmaps=allmaps)

@flask_app.route('/user/<name_route>')
@login_required
def user_profile(name_route):
    if g.user and g.user.name_route == name_route:
        return redirect('/me')

    viewed = kaizen_user.user_with_name_route(name_route)
    if viewed:
        return render_template('user_profile.html', user=viewed, mappings=view_mappings(viewed), notes=view_notes(viewed, 5))
    flash('No user with name %s, should have 404ed' % name)
    return redirect(url_for('404'))

def view_mappings(u):
    return [{'name':str(m.name), 'notes':m.get_all_notes(), 'sites':m.get_all_sites()} for m in u.get_all_mappings_in_notes_order()]

def view_notes(u, n):
    return u.recent_notes(n)

def summarize_maps(mappings):
    ret = {'sumSites':0, 'sumNotes':0}
    for m in mappings:
        ret['sumSites'] += len(m['sites'])
        ret['sumNotes'] += len(m['notes'])
    return ret
