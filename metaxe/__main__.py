from metaxe import app

# https://github.com/pallets/flask/issues/1907
app.app.jinja_env.auto_reload = True

app.app.run(port=5000, debug=True)
