# coding = utf-8

import tornado.web
import operator
from methods.pub import *
from methods.syn_data import *

class api_item_info(tornado.web.RequestHandler):
	@tornado.gen.coroutine
	def post(self):
		conn = mdb_get_conn()
		res = {"res": "error", "error_text": "error_0"}
		act = self.get_argument("act")

		# 同步商品信息
		if act == "syn_item_info":
			data = {"table": "item_info", "key": "barcode", "item_list": json.loads(self.get_argument("item_list"))}
			res = syn_data_mysql(data)

		conn.close()
		self.finish(res)
			