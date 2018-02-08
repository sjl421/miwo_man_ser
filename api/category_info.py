# coding = utf-8

import tornado.web
import operator
from methods.pub import *
from methods.syn_data import syn_data_mysql

class api_category_info(tornado.web.RequestHandler):
	@tornado.gen.coroutine
	def post(self):
		conn = mdb_get_conn()
		res = {"res": "error", "error_text": "error_0"}
		act = self.get_argument("act")

		# 同步商品分类信息
		if act and act == "syn_category_info":
			data = {"table": "category_info", "key": "code", "item_list": json.loads(self.get_argument("cate_list"))}
			res = syn_data_mysql(data)

		conn.close()
		self.finish(res)