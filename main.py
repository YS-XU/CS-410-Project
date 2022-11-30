from flask import Flask, render_template, request, redirect
import db

app = Flask(__name__)
mydb = db.Database()


@app.route('/')
def index():
  lectures = mydb.getLecture("week2")
  return render_template('index.html', lectures = lectures)

@app.route('/<title>')
def lecture(title):
  lectures = mydb.lecture_detail(title)
  with open("static/" + lectures[0]["Subtitle"], "r") as f: 
    subtitle = f.read()
  return render_template('single-post.html', video = lectures[0]["Video"], subtitle = subtitle)


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=81, debug=True)
