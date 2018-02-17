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
		if data["act"] and data["act"] == "get_report" and not pub_none(data["report_item"]):

			s_stamp = float(0)
			e_stamp = float(0)
			sale_sum = {"money_sum": float(0), "item_count": float(0), "item_qty": float(0), "in_sum": float(0)}
			give_sum = {"money_sum": float(0), "item_count": float(0), "item_qty": float(0), "in_sum": float(0)}
			return_sum = {"money_sum": float(0), "item_count": float(0), "item_qty": float(0), "in_sum": float(0)}

			# 整理日期的时间戳
			now_day = datetime.datetime.now()
			# 今天
			if data["report_item"]["sale_date"] == "today":
				s_datetime = datetime.datetime.combine(now_day, datetime.time.min)
				e_datetime = datetime.datetime.combine(now_day, datetime.time.max)

			# 昨天
			if data["report_item"]["sale_date"] == "yesterday":
				s_datetime = datetime.datetime.combine((datetime.date.today() - datetime.timedelta(days = 1)), datetime.time.min)
				e_datetime = datetime.datetime.combine((datetime.date.today() - datetime.timedelta(days = 1)), datetime.time.max)

			# 本周
			if data["report_item"]["sale_date"] == "this_week":
				
				s_datetime = datetime.datetime.combine((now_day - datetime.timedelta(days = now_day.weekday())), datetime.time.min)
				e_datetime = datetime.datetime.combine((now_day + datetime.timedelta(days = (6 - now_day.weekday()))), datetime.time.max)

			# 上周
			if data["report_item"]["sale_date"] == "last_week":

				# t_time = now - timedelta(days=now.weekday()+7)
				# s_stamp = float(time.mktime(t_time.timetuple()) - time.mktime(t_time.timetuple()) % 86400 + time.timezone)
				# e_stamp = float(s_stamp + 604800)
				s_datetime = datetime.datetime.combine((now_day - datetime.timedelta(days = now_day.weekday() + 7)), datetime.time.min)
				e_datetime = datetime.datetime.combine((now_day - datetime.timedelta(days = now_day.weekday() + 1)), datetime.time.max)


			# 本月
			if data["report_item"]["sale_date"] == "this_month":
				now_year = now_day.year
				now_month = now_day.month

				s_datetime = datetime.datetime.combine(datetime.date(now_year, now_month, 1), datetime.time.min)

				if now_month == 12:
					e_datetime = datetime.datetime.combine(datetime.date(now_year + 1, 1, 1) - datetime.timedelta(days = 1), datetime.time.min)
				else:
					e_datetime = datetime.datetime.combine(datetime.date(now_year, now_month + 1, 1) - datetime.timedelta(days = 1), datetime.time.max)

			
			# 上月
			if data["report_item"]["sale_date"] == "last_month":
				now_year = now_day.year
				now_month = now_day.month

				if now_month == 1:
					s_datetime = datetime.datetime.combine(datetime.date(now_year - 1, 12, 1), datetime.time.min)

				else:
					s_datetime = datetime.datetime.combine(datetime.date(now_year, now_month - 1, 1), datetime.time.min)

				e_datetime =  datetime.datetime.combine((datetime.date(now_year, now_month, 1) - datetime.timedelta(days = 1)), datetime.time.max)

			# 一周内
			if data["report_item"]["sale_date"] == "in_week":
				s_datetime = datetime.datetime.combine((datetime.date.today() - datetime.timedelta(days = 6)), datetime.time.min)
				e_datetime = datetime.datetime.combine(datetime.date.today(), datetime.time.max)
			# 一月内
			if data["report_item"]["sale_date"] == "in_month":
				s_datetime = datetime.datetime.combine((datetime.date.today() - datetime.timedelta(days = 30)), datetime.time.min)
				e_datetime = datetime.datetime.combine(datetime.date.today(), datetime.time.max)
			# 一年内
			if data["report_item"]["sale_date"] == "in_year":
				s_datetime = datetime.datetime.combine((datetime.date.today() - datetime.timedelta(days = 365)), datetime.time.min)
				e_datetime = datetime.datetime.combine(datetime.date.today(), datetime.time.max)


			# start_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(s_stamp))
			# end_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(e_stamp))
			print(s_datetime)
			print(e_datetime)
			start_date = str(s_datetime)[: 19]
			end_date = str(e_datetime)[: 19]

			

			# 整理关键字
			if not pub_none(data["report_item"]["key_word"]):
				key_word = "%" + data["report_item"]["key_word"].replace(" ", "%") + "%"
			else:
				key_word = "%"

			sql = mdb_cm(conn, "select (sum(sale_record.sale_money) - sum(sale_record.in_price)) / sum(sale_record.sale_money) as rate, sum(sale_record.sale_money) - sum(sale_record.in_price) as profit, sale_record.type, sum(sale_record.sale_qty) as sale_qty, sum(sale_record.in_price) as in_price, sum(sale_record.sale_money) as sale_money, sale_record.sale_price, sale_record.item_barcode,item_info.`name`, item_info.size, item_info.unit from sale_record left join item_info on sale_record.item_barcode = item_info.barcode where sale_record.oper_datetime >= %s and sale_record.oper_datetime <= %s and item_info.name like %s GROUP BY sale_record.type, sale_record.item_barcode  order by sum(sale_record.sale_qty) desc, sale_money desc, type asc", (str(s_datetime), str(e_datetime), str(key_word)))

			# print(sql)

			result = mdb_get_all(conn, sql)
			if result:
				for r in result:
					# r["rate"] = r["rate"] * 100
					if pub_type(r["rate"], float):
						r["rate"] = pub_2f(r["rate"] * 100) + "%";

					if r["type"] == "A":
						# r["type"] = "售"
						get_sum(sale_sum, r)
					if r["type"] == "B":
						# r["type"] = "退"
						get_sum(return_sum, r)
					if r["type"] == "C":
						# r["type"] = "赠"
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

