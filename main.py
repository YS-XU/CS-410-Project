from flask import Flask, render_template, request, redirect
import db

app = Flask(__name__)
mydb = db.Database()


@app.route('/')
def index():
  return render_template('index.html')

@app.route('/lecture')
def lecture():
  lectures = mydb.getLecture()
  
  return render_template('single-post.html', video = lectures[0]["Video"])


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=81, debug=True)
