import pymongo
from flask import Flask, render_template, request, redirect
from flask_moment import Moment
from datetime import datetime
from bson.objectid import ObjectId

app = Flask('notemanager')
moment=Moment(app)

connectionstring = open("connectionstring.txt", "r")
cluster = pymongo.MongoClient(connectionstring.read().strip())
connectionstring.close()
database = cluster.notemanager
collection = database.notes

@app.route('/',methods=["GET","POST"])
def index():
    if request.method=="GET":
        notes=list(collection.find({}))
        # print(notes)
        return render_template('index.html', notes = notes)
    else:
        record = {}
        record["note"]=request.form["note"]
        record["time"]=datetime.utcnow()

        collection.insert_one(record)
        return redirect('/')
    
@app.route('/deletenote')
def delete():
    # print("deleting note")
    noteid=request.args["noteid"]
    # print(noteid)
    # print(request.args)
    collection.delete_one({"_id":ObjectId(noteid)})
    return redirect('/')

app.run (debug = True)
