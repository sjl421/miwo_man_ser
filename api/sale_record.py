# coding = utf-8

import tornado.web
import operator
from methods.pub import *
from methods.syn_data import syn_data_mysql

class api_sale_record(tornado.web.RequestHandler):
	@tornado.gen.coroutine
	def post(self):
		conn = mdb_get_conn()
		res = {"res": "error", "error_text": "ser:sale_record.error_0"}
		act = self.get_argument("act")

		# 同步全部销售记录
		if act and act == "syn_sale_record":
			data = {"table": "sale_record", "key": "rcd_id", "item_list": json.loads(self.get_argument("rcd_list"))}
			res = syn_data_mysql(data)

		# 增量同步销售记录时，需要获取最后一条记录的操作时间，用于确定从何时开始同步记录
		if act and act == "get_rcd_time_stamp":
			# 获取当前远程数据库中最后一条记录的操作时间戳
			sql = "select oper_time_stamp from sale_record order by oper_time_stamp desc limit 1"
			result = mdb_get_one(conn, sql)
			if result:
				res = {"res": "done", "rcd_time_stamp": result["oper_time_stamp"]}

		

		conn.close()
		self.finish(res)