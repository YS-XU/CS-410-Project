from flask import Flask
import pymysql
# from flask_cors import *
# from flask import Response,request

app = Flask(__name__)
# CORS(app, supports_credentials=True)


class Database:

  def __init__(self):
    host = "34.66.155.131"
    user = "root"
    password = "CS410project"
    db = "cs410"
    self.con = pymysql.connect(host=host,
                               user=user,
                               password=password,
                               db=db,
                               cursorclass=pymysql.cursors.DictCursor)
    self.cur = self.con.cursor()

  def getLecture(self, weeks):
    sql = "SELECT * FROM cs410.Lecture WHERE Weeks = %s"
    self.cur.execute(sql, (weeks))
    result = self.cur.fetchall()
    return result
  
  def lecture_detail(self, title):
    sql = "SELECT * FROM cs410.Lecture WHERE Title = %s"
    self.cur.execute(sql, (title))
    result = self.cur.fetchall()
    return result
#   def test(self):
#     sql = "select * from testDB.Unit"
#     self.cur.execute(sql)
#     result = self.cur.fetchall()
#     return result


# if __name__ == '__main__':
#     app.run(debug=True)
