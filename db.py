from flask import Flask # need to install
import pymysql # need to install

import re
import string
import jieba # need to install
import codecs
import os
import math
import time
import nltk # need to install
nltk.download('punkt')
from nltk.tokenize import word_tokenize
from collections import Counter
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
    self.index = {}

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
  
  def get_All_Lecture(self, query):
    sql = "SELECT * FROM cs410.Lecture"
    self.cur.execute(sql)
    lectures = self.cur.fetchall()

    self.classify(lectures)
    search_result = self.test(query)

    final_result = []
    for result in search_result:
      for lecture in lectures:
        if lecture["Subtitle"] == result:
          final_result.append(lecture)
          
    return final_result
  
  def create_inverted_index(self, filename, page):
    src_data = codecs.open(filename, 'r+', encoding='utf-8').read()

    if src_data[:1].encode('utf-8') == codecs.BOM_UTF8:
        src_data = src_data[1:]


    sp_data = src_data.split()


    words = list(sp_data)
    dic_word_count = Counter(words)


    for word in dic_word_count.keys():
        dic_word_count[word] = [page, dic_word_count[word]]
        if word in self.index.keys():
            self.index[word].append(dic_word_count[word])
        else:
            self.index[word] = [dic_word_count[word]]
  
  def classify(self, lectures):

      print('>>>Create an inverted index')
      fenci_txt = "fenci.txt"
      N = 0

      N = len(lectures)
      files=[]
      for i in lectures:
          files.append(i['Subtitle'])
      s = []
      for file in files: 
          if not os.path.isdir(file):


              f = codecs.open(fenci_txt, 'w', encoding="UTF-8-SIG")
              #print(file)
              for line in open("static/" + file,encoding='utf-8',errors='ignore').readlines():
                  

                  remove_chars = '[·’!"\#$%&\'()＃！（）*+,-./:;<=>?\@，：?￥★、…．＞【】［］《》？“”‘’\[\\]^_`{|}~]+'
                  line = re.sub(remove_chars, "", line)

                  seg_list =  word_tokenize(line)

                  f.write(" ".join(seg_list)+"\n")  
              f.close()      

              self.create_inverted_index(fenci_txt, file)

      print('>>>Calculate tf-idf')

      i = 0
      for key in self.index.keys():
          df = len(self.index[key])
          i += 1
          for file_tf in self.index[key]:
              tf = file_tf[1]
              w = (1.0 + math.log(tf)) * math.log10(N / df)
              file_tf.append(w)

  def search(self, query):
      time_start=time.time()
      query = re.sub( '[·’!"\#$%&\'()＃！（）*+,-./:;<=>?\@，：?￥★、…．＞【】［］《》？“”‘’\[\\]^_`{|}~]+', " ", query)

      fenci =  word_tokenize(query)
      pages = {}
      for word in fenci:
          if word in self.index:
              for page in self.index[word]:
                  if page[0] in pages:
                      pages[page[0]] += page[2]
                  else:
                      pages[page[0]] = page[2]
      
      page_list = sorted(pages.items(), key = lambda item:item[1], reverse=True)
      time_end = time.time()
      len_page_list = len(page_list)
      search_result = []
      if len_page_list != 0:
        for page in page_list:
          #print(page[0])
          #print("%d:%.1f.txt, tf-idf=%f" % (i, float(page[0]/10), page[1]))
          
          search_result.append(page[0])
          # i += 1
        return search_result
          
      else:
          return None  


  def test(self, query):
    # query = input('please enter：')
    result = self.search(query)
    return result
    index = {}



# if __name__ == '__main__':
#     app.run(debug=True)
