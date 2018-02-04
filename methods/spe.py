# coding = utf-8

import tornado.web
import requests
from methods.pub import *


class spe_method(tornado.web.RequestHandler):
	@tornado.gen.coroutine
	def post(self):
		data = pub_json_loads(self)
		act = data["act"]
		res = {}
		if act == "syn_spe":
			sconn = sdb_get_conn()
			sql = "select item_no as code, old_price, spe_price, start_date, end_date from t_rm_spec_price"

			spe = sdb_get_all(sconn, sql)
			sconn.close()

			if spe:
				for item in spe:
					item["start_date"] = item["start_date"].strftime("%Y-%m-%d")
					item["end_date"] = item["end_date"].strftime("%Y-%m-%d")
					item["code"] = item["code"].strip()
					item["old_price"] = float(item["old_price"])
					item["spe_price"] = float(item["spe_price"])

				host = pub_get_host()

				# 发送商品数据
				cs_url = host + "/api/up_spe"
				p_spe = {"spe": json.dumps(spe)}
				r = requests.post(cs_url, data = p_spe)
				res = pub_btos(r.content)

				# 添加操作记录
				log = pub_insert_log(host, "syn_spe", res)

		self.finish(res)