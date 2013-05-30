#!venv/bin/python
import app
app.db.create_all()
app.flask_app.run(debug=True)
