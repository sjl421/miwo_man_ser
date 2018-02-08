# coding = utf-8

import tornado.web
import operator
from methods.pub import *
from methods.syn_data import syn_data_mysql

class api_sale_record(tornado.web.RequestHandler):
	@tornado.gen.coroutine
	def post(self):
		conn = mdb_get_conn()
		res = {"res": "error", "error_text": "error_0"}
		act = self.get_argument("act")
		
		# select 	sum(sale_record.sale_qty), sale_record.item_barcode,item_info.`name` from sale_record left join item_info on 	sale_record.item_barcode = item_info.barcode where sale_record.oper_time_stamp > 1517000000 GROUP BY 	sale_record.item_barcode order by sum(sale_record.sale_qty) desc

		# 同步全部销售记录
		if act and act == "syn_sale_record":
			data = {"table": "sale_record", "key": "rcd_id", "item_list": json.loads(self.get_argument("rcd_list"))}
			res = syn_data_mysql(data)


		# 增量同步销售记录
		if act and act == "get_rcd_time_stamp":
			# 获取当前远程数据库中最后一条记录的操作时间戳
			sql = "select oper_time_stamp from sale_record order by oper_time_stamp desc limit 1"
			result = mdb_get_one(conn, sql)
			if result:
				res = {"res": "done", "rcd_time_stamp": result["oper_time_stamp"]}

		conn.close()
		self.finish(res)