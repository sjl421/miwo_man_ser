# coding = utf-8

import tornado.web

from methods.pub import *

class restk(tornado.web.RequestHandler):
	@tornado.gen.coroutine
	def post(self):
		
		res = {"res": "error_0"}
		data = pub_get_arg(self)
		if data:
			act = data["act"]
			res = {"res": "error"}
			# 引入数据库连接
			conn = mdb_get_conn()
			if act == "get_restk_node":
				print("restk_node")
				sql = mdb_cm(conn, "select * from restk where state = %s order by insert_time_stamp desc limit 8", (int(1)))
				result = mdb_get_all_num(conn, sql)
			

			'''
			添加数据
			实现功能：
				商品管理的首页中的预期进货组件中，增加项目
			传入参数：
				数据格式：json
				item: {
					name: ""	预期进货的商品名称
				}
			'''
			if act == "add_node_item":
				print(data)
				# 检查数据是否有效
				item = data["item"]
				pp(item)
				if pub_none(item) or pub_none(item["name"]):
					res = {"res": "error", "error_text": "名称错误"}
				elif not pub_none(item) and not pub_none(item["name"]):
					print("asdfasdfsa");
					# 时间戳
					time_stamp = pub_get_time_stamp()
					sql = mdb_cm(conn, "insert into `miwo_man_ser`.`restk_node` ( `size`, `insert_time_stamp`, `state`, `name`) values ( %s, %s, '1', %s)", (str(""), int(time_stamp), str(item["name"])))
					result = mdb_do(conn, sql)
					print(result)
					if result:
						res = {"res": "done"}
				
			if act == "get_restk_list":
				sql = mdb_cm(conn, "select id, name from restk_node where state = %s order by insert_time_stamp desc limit 8 ", (str(1)))
				result = mdb_get_all(conn, sql)
				restk_list = []

				'''
				for item in result:
					restk_list.append(item["name"])
				'''
				restk_list = result

				if result:
					res = {"res": "done", "restk_list": restk_list}
				else:
					res = {"res": "error", "error_text": "服务器错误"}

			if act == "restk_list_op":
				if pub_none(data["item_id"]) or pub_none(data["act_type"]):
					res = {"res": "error", "error_text": "没有删除项目"}
				else:
					# op_value = 1
					print(data)
					if data["act_type"] == "done":
						op_value = 2
					elif data["act_type"] == "cxl":
						op_value = 0
					sql = mdb_cm(conn, "update `restk_node` set `state`=%s where `id`= %s", (int(op_value), int(data["item_id"])))
					print(sql)
					result = mdb_do(conn, sql)

					if result:
						res = {"res": "done"}
					else:
						res = {"res": "error", "error_text": "失败"}

		conn.close()
		print(res)
		self.finish(res)