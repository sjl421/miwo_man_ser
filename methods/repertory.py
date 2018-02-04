# coding = utf-8

import tornado.web
from methods.sdb import *
from methods.pub import *
import requests

class repertory_method(tornado.web.RequestHandler):
	@tornado.gen.coroutine
	def post(self):
		data = pub_json_loads(self)

		act = data["act"]
		res = {}
		if act == "syn_repertory":
			sconn = sdb_get_conn()
			host = pub_get_host()
			# 查询库存
			sql = "select item_no as code, stock_qty as repertory from t_im_branch_stock"
			rep = sdb_get_all(sconn, sql)

			sconn.close()

			if rep:
				for item in rep:
					item["code"] = item["code"].strip()
					item["repertory"] = int(item["repertory"])

				cs_url = host + "/api/up_repertory"
				d = {"rep": json.dumps(rep)}
				r = requests.post(cs_url, data = d)

				res = pub_btos(r.content)

				# 添加操作记录
				log = pub_insert_log(host, "syn_repertory", res)

		self.finish(res)