from flask import Flask, render_template,request,redirect,url_for
from flask_pymongo import PyMongo
import json

app = Flask(__name__, static_url_path='')

app.config["MONGO_URI"] = "mongodb://localhost:27017/NotesApp"
mongo = PyMongo(app)
notes_collection = mongo.db['notes']

@app.route('/')
def root():
    return app.send_static_file('index.html')

@app.route('/notes')
def get_notes():
    notes = notes_collection.find()
    return render_template('list_notes.html', notes=notes)

@app.route('/notes/<note>')
def get_note(note=None):
    if(note == None):
        return redirect("/")
    queried = notes_collection.find_one({"name":note})
    return render_template("view_note.html", note=queried)

@app.route('/create', methods=['GET', 'POST'])
def create_note():
    if(request.method == "POST"):
        post = {
            "name": request.form.get('name'),
            "text": request.form.get('text')
        }
        notes_collection.insert(post)
        return redirect("/notes")
    else:
        return render_template("create_note.html")