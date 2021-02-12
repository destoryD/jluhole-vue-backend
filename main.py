#!/usr/bin/python
# -*- coding: UTF-8 -*-
from flask import Flask,jsonify,request
import time
import pymysql
import utils
import json
app = Flask(__name__)
class mysqldb():
    def __init__(self,host,user,password,dbname):
        conn=pymysql.connect(host=host,user = user,passwd = password,db = dbname,charset='utf8')
        self.cursor = conn.cursor()
    def fetchindex(self,lastuid,pagesize):
        if lastuid == 'none':
            self.cursor.execute("SELECT * from posts ORDER BY createtime DESC LIMIT 1")
        else:
            self.cursor.execute("SELECT * from posts where uid=%s",(lastuid))
        try:
            lastid = self.cursor.fetchone()[0]
            if lastuid == 'none':
                lastid = lastid+1
            self.cursor.execute("SELECT * from posts where id<%s ORDER BY createtime DESC LIMIT %s",(lastid,pagesize))
        except Exception as e:
            print(e)
            return []
        datalists = self.cursor.fetchall()
        if len(datalists) > 0:
            return datalists
        else:
            return []
    def insertpost(self,author,title,content):
        uid = utils.generateuid()
        row_count=self.cursor.execute("select user,pwd from User where user='%s' and pwd='%s'" ,(username,password))
@app.route('/api/index',methods=['post'])
def getIndex():
    if not request.data:
        return jsonify({'code':200,'data':[]})
    vdata= json.loads(request.data)
    db = mysqldb("42.193.97.19","jluholetest","*****","jluholetest")
    postlists=[]
    for row in db.fetchindex(vdata['lastuid'],vdata['pagesize']):
        uid = row[1]
        title = row[2]
        content = row[3]
        createtime = row[4]
        lastupdatetime = row[5]
        hot = row[6]
        likes = row[7]
        replys = row[8]
        item={"uid":uid,"Title":title,"Content":content,"createtime":createtime,"LastUpdateTime":time.strftime("%Y/%m/%d %H:%M:%S", time.localtime(lastupdatetime)),"hot":hot,"replys":replys}
        postlists.append(item)
    data={"code":200,"data":postlists}
    return jsonify(data)

if __name__ == '__main__':
    app.run(host='127.0.0.1',port=5000,debug=True)