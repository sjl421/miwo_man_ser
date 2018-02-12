# coding = utf-8

import tornado.web
import time
import datetime
import requests
from datetime import timedelta
from methods.pub import *

class api_report(tornado.web.RequestHandler):
	@tornado.gen.coroutine
	def post(self):
		conn = mdb_get_conn()
		res = {"res": "error", "error_text": "ser:report.error_0"}
		data = pub_json_loads(self)

		# 获取最后一次插入记录的操作时间,用户确认是否需要同步数据
		if data["act"] and data["act"] == "get_last_syn_stamp":
			sql = "select insert_time_stamp from sale_record order by insert_time_stamp desc limit 1"
			result = mdb_get_one(conn, sql)
			if result:
				res = {"res": "done", "stamp": result["insert_time_stamp"]}

		# 获取报表
		if data["act"] and data["act"] == "get_report" and not pub_none(data["sale_date"]):

			s_stamp = float(0)
			e_stamp = float(0)
			sale_sum = {"money_sum": float(0), "item_count": float(0), "item_qty": float(0), "in_sum": float(0)}
			give_sum = {"money_sum": float(0), "item_count": float(0), "item_qty": float(0), "in_sum": float(0)}
			return_sum = {"money_sum": float(0), "item_count": float(0), "item_qty": float(0), "in_sum": float(0)}

			# 整理日期的时间戳
			now = datetime.datetime.now()
			# 今天
			if data["sale_date"] == "today":
				s_stamp = float(time.mktime(datetime.datetime.combine(datetime.date.today(), datetime.time.min).timetuple()))
				e_stamp = float(s_stamp + 86400) 

			# 昨天
			if data["sale_date"] == "yesterday":
				e_stamp = float(time.mktime(datetime.datetime.combine(datetime.date.today(), datetime.time.min).timetuple()))
				s_stamp = e_stamp - 86400

			# 本周
			if data["sale_date"] == "this_week":
				t_time = now - timedelta(days=now.weekday())
				s_stamp = float(time.mktime(t_time.timetuple()) - time.mktime(t_time.timetuple()) % 86400 + time.timezone)
				e_stamp = float(s_stamp + 604800)

			# 上周
			if data["sale_date"] == "last_week":
				t_time = now - timedelta(days=now.weekday()+7)
				s_stamp = float(time.mktime(t_time.timetuple()) - time.mktime(t_time.timetuple()) % 86400 + time.timezone)
				e_stamp = float(s_stamp + 604800)

			# 本月
			if data["sale_date"] == "this_month":
				t_time = datetime.datetime(now.year, now.month, 1) + timedelta(days=1)
				s_stamp = float(time.mktime(t_time.timetuple()) - time.mktime(t_time.timetuple()) % 86400 + time.timezone)
				t_time = datetime.datetime(now.year, now.month + 1, 1) + timedelta(days=1)
				e_stamp = float(time.mktime(t_time.timetuple()) - time.mktime(t_time.timetuple()) % 86400 + time.timezone)
			
			# 上月
			if data["sale_date"] == "last_month":
				e_time = datetime.datetime(now.year, now.month, 1) + timedelta(days=1)
				e_stamp = float(time.mktime(e_time.timetuple()) - time.mktime(e_time.timetuple()) % 86400 + time.timezone)
				s_time = datetime.datetime(e_time.year, e_time.month - 1, 1) + timedelta(days=1)
				s_stamp = float(time.mktime(s_time.timetuple()) - time.mktime(s_time.timetuple()) % 86400 + time.timezone)

			# 一周内
			if data["sale_date"] == "in_week":
				t_time = now - timedelta(days=6)
				s_stamp = float(time.mktime(t_time.timetuple()) - time.mktime(t_time.timetuple()) % 86400 + time.timezone)
				e_stamp = float(time.mktime(now.timetuple()) - time.mktime(now.timetuple()) % 86400 + time.timezone + 86400)
			# 一月内
			if data["sale_date"] == "in_month":
				t_time = now - timedelta(days=30)
				s_stamp = float(time.mktime(t_time.timetuple()) - time.mktime(t_time.timetuple()) % 86400 + time.timezone)
				e_stamp = float(time.mktime(now.timetuple()) - time.mktime(now.timetuple()) % 86400 + time.timezone + 86400)
			# 一年内
			if data["sale_date"] == "in_year":
				t_time = now - timedelta(days=365)
				s_stamp = float(time.mktime(t_time.timetuple()) - time.mktime(t_time.timetuple()) % 86400 + time.timezone)
				e_stamp = float(time.mktime(now.timetuple()) - time.mktime(now.timetuple()) % 86400 + time.timezone + 86400)

			start_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(s_stamp))
			end_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(e_stamp))

			# print(start_date)
			# print(end_date)

			sql = mdb_cm(conn, "select sum(sale_record.sale_money) - sum(sale_record.in_price) as profit, sale_record.type, sum(sale_record.sale_qty) as sale_qty, sum(sale_record.in_price) as in_price, sum(sale_record.sale_money) as sale_money, sale_record.sale_price, sale_record.item_barcode,item_info.`name`, item_info.size, item_info.unit from sale_record left join item_info on sale_record.item_barcode = item_info.barcode where sale_record.oper_time_stamp >= %s and sale_record.oper_time_stamp <= %s GROUP BY sale_record.item_barcode, sale_record.type order by sum(sale_record.sale_qty) desc, sale_money desc, type asc", (float(s_stamp), float(e_stamp)))

			result = mdb_get_all(conn, sql)
			if result:
				for r in result:
					if r["type"] == "A":
						get_sum(sale_sum, r)
					if r["type"] == "B":
						get_sum(return_sum, r)
					if r["type"] == "C":
						get_sum(give_sum, r)
				# 对反馈的概况进行整理
				# 销售额减去退货金额
				sale_sum["money_sum"] = sale_sum["money_sum"] - return_sum["money_sum"]
				sale_sum["in_sum"] = sale_sum["in_sum"] - return_sum["in_sum"] + give_sum["in_sum"]
				sale_sum["item_count"] = sale_sum["item_count"] - return_sum["item_count"]
				sale_sum["item_qty"] = sale_sum["item_qty"] - return_sum["item_qty"]

				# 整理数据
				sale_sum = trim_data(sale_sum)
				give_sum = trim_data(give_sum)
				return_sum = trim_data(return_sum)
				'''
				give_sum = keep_2(give_sum)
				return_sum = keep_2(return_sum)
				'''
		
			res = {"res": "done", "sale_sum": sale_sum, "give_sum": give_sum, "return_sum": return_sum, "start_date": start_date, "end_date": end_date, "report_list": result}

		conn.close()
		self.finish(res)

def get_sum(s, r):
	s["item_count"] += 1
	s["item_qty"] += r["sale_qty"]
	s["money_sum"] += r["sale_money"]
	s["in_sum"] += r["in_price"]

def trim_data(s):
	# 计算利润
	s["profit"] = s["money_sum"] - s["in_sum"]
	# 毛利率
	if s["money_sum"] != 0 and s["profit"] != 0:
		s["rate"] = str(pub_2f((s["profit"] / s["money_sum"]) * 100)) + " %"
	else:
		s["rate"] = "0.00 %"
	# 如果是浮点数，则保留两位小数
	for item in s:
		if pub_type(s[item], float):
			s[item] = pub_2f(s[item])

	# 数量变成整数
	s["item_qty"] = int(float(s["item_qty"]))
	s["item_count"] = int(float(s["item_count"]))

	return s

