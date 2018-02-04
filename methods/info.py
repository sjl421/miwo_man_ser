# coding = utf-8

import tornado.web
from methods.mdb import *
from methods.sdb import *
from methods.pub import *
import requests

class info_method(tornado.web.RequestHandler):
	@tornado.gen.coroutine
	def post(self):
		data = pub_json_loads(self)
		act = data["act"]
		res = {}
		mconn = mdb_get_conn()
		# 获取服务器信息
		if act == "get_info":
			sql = "select * from info where id = 0"
			info = mdb_get_one(mconn, sql)
			res = {"res": "done", "info": info}

		# 更改服务器信息
		if act == "update_host":
			host = data["host"]
			sql = mdb_cm(mconn, "update info set value = %s where id = 0", (str(host)))
			res_info = mdb_do(mconn, sql)
			if res_info:
				sql = "select value from info where id = 0"
				host = mdb_get_one(mconn, sql)

				res = {"res": "done", "host": host["value"]}

		mconn.close()
		self.finish(json.dumps(res))