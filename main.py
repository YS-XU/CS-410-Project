from flask import Flask, render_template, request, redirect
import db

app = Flask(__name__)
mydb = db.Database()


@app.route('/')
def index():
  return render_template('index.html')


@app.route('/search_user', methods=['POST'])
def search_user():
  firstName = request.form.get('fname')
  lastName = request.form.get('lname')
  email = request.form.get('email')
  result = mydb.search_user(firstName, lastName, email)
  return render_template('users.html', result=result)


@app.route('/test_db/')
def test_db():
  result = mydb.test()
  return result


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=81, debug=True)
