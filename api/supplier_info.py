# coding = utf-8

import tornado.web
import operator
from methods.pub import *
from methods.syn_data import *

class api_supplier_info(tornado.web.RequestHandler):
	@tornado.gen.coroutine
	def post(self):
		conn = mdb_get_conn()
		res = {"res": "error", "error_text": "error_0"}
		act = self.get_argument("act")

		if act and act == "syn_supplier_info":
			data = {"table": "sup_info", "key": "code", "item_list": json.loads(self.get_argument("sup_list"))}
			res = syn_data_mysql(data)
			
		conn.close()
		self.finish(res)
