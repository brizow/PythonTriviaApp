"""
Routes and views for the flask application.
"""

from datetime import datetime
from FlaskWebProject1 import app
from flask import Flask, url_for, request, render_template 
import redis

#let's make a top level connection string to redis
r=redis.StrictRedis(host="localhost", port=6379, db=0, charset="utf-8", decode_responses=True) #running on my local host at this default port number in the default database. 
# - 8 bit character set, decode the responses to a string for us.
#r=redis.StrictRedis() -this works for all the defaults as well.

#use a global variable for the year
year=datetime.now().year

#/ or /home
@app.route("/")
@app.route("/home")
def home():
    return render_template("Index.html", title="Home Page", year=year)
    #createLink = "<a href=" + url_for("create") + ">Create a question</a>"

#server/create
@app.route("/create", methods=["GET", "POST"]) #good practice to enable specific method calls
def create():
    #if you are posting back
    if request.method == "GET":
        #send user the form
        return render_template("CreateQuestion.html", title="Create a question", year=year)
    #if you are posting
    elif request.method == "POST":
        #read form data and save it    
        title = request.form["title"]
        answer = request.form["answer"]
        question = request.form["question"]

        #store data in the database (redis).
        #key name format = title:question, title:answer
        r.set(title + ":question", question) #colons are commonly used for key values in redis
        r.set(title + ":answer", answer)

        #return the html template
        return render_template("CreatedQuestion.html", question = question, title="Thanks!", year=year) #first question, new varible. The second question is pulling from the question variable in the elif
    else:
        #just in case
        return "<h2>Invalid Request</h2>"

#server/question/<title>
@app.route("/question/<title>", methods=["GET", "POST"])
def question(title):
    if request.method == "GET":
        #send user the form    
        #fill the question variable with data from datastore
        question = r.get(title + ":question")
        return render_template("AnswerQuestion.html", question = question, title="Answer Question", year=year)
    elif request.method == "POST":
        #user has attmepted an answer. Check if correct
        submittedAnswer = request.form["submittedAnswer"] #did fail here - we didn't have our variable name correct on the HTML side.
        #read answer from datastore
        answer = r.get(title + ":answer")
        if submittedAnswer == answer:
            return render_template("Correct.html", title="Good job!", year=year)
        else:
            return render_template("Incorrect.html", submittedAnswer = submittedAnswer, answer = answer, title="Oh noes!", year=year)    
    else: 
        return "<h2>Invalid Request</h2>"

#server/answer
@app.route("/answer")
def answer():
    return ""

    #print(allquestions)
    #return "<html><head><title>Hello, world!</title></head><body>Empty Route</body></html>"

