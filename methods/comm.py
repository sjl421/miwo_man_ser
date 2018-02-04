# coding = utf-8

import tornado.web
import requests
from methods.pub import *


class comm_method(tornado.web.RequestHandler):
	@tornado.gen.coroutine
	def post(self):
		data = pub_json_loads(self)
		act = data["act"]
		res = {}
		if act == "syn_comm":
			sql = "select price as p_price, item_no as code, item_name as name, unit_no as unit, item_size as sp, sale_price as price from t_bd_item_info"
			sconn = sdb_get_conn()
			comm = sdb_get_all(sconn, sql)
			sconn.close()
			if comm:
				for item in comm:
					item["code"] = item["code"].strip()
					item["unit"] = str(item["unit"]).strip()
					item["price"] = float(item["price"])
					item["p_price"] = float(item["p_price"])

				host = pub_get_host()

				# 发送商品数据
				cs_url = host + "/api/up_comm"
				p_comm = {"comm": json.dumps(comm)}
				r = requests.post(cs_url, data = p_comm)
				res = pub_btos(r.content)

				# 添加操作记录
				log = pub_insert_log(host, "syn_comm", res)

		self.finish(res)