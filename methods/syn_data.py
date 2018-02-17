# coding = utf-8

import tornado.web
import operator
import datetime
from methods.pub import *

'''
同步数据库
实现功能：同步远程数据库和收银机数据库
传输注意：数据数组的KEY与数据库的字段名称需要相同。
传递参数：
	json = {
		table:		要同步的表
		key:		主要识别的字段
		item_list:	接受到的数据内容
	}
'''
def syn_data_mysql(data):

	conn = mdb_get_conn()
	res = {"res": "error", "error_text": "syn_data: 参数错误"}

	if "table" in data.keys() and "key" in data.keys() and "item_list" in data.keys():

		# 初始化反馈数据数据
		insert_num = 0
		update_num = 0
		insert_key = []
		update_key = []

		# 保存查询中组合全部关键字段的信息
		keys = []
		# 保存反馈记录中的关键字段，用于对比数据
		r_keys = []
		# 查询得到的记录信息
		r_list = {}

		# 遍历传递数据，整理关键字段
		if len(data["item_list"]) > 1:
			for item in data["item_list"]:
				keys.append(item[data["key"]])
			keys = tuple(keys)
		else:
			keys = "("+ data["item_list"][0][data["key"]] +")"

		# 整理要查询的字段信息
		fleld = ""
		for k in list(data["item_list"][0].keys()):
			fleld = fleld + k + ", "
		fleld = fleld + "id"

		# 进行查询
		sql = "select " + fleld + " from " + data["table"] + " where " + data["key"] + " in " + str(keys)
		result = mdb_get_all(conn, sql)
		# 对数据进行整理
		if result:
			for r in result:
				r_keys.append(r[data["key"]])
				r_list[r[data["key"]]] = r

		# 要删除的传递数据索引
		del_index = []
		# 检查传递来的数据是否存在，如果不存在，则插入新数据
		for item in data["item_list"]:

			if item[data["key"]] not in r_keys:

				# now_time_stamp = time.time()
				now_datetime = datetime.datetime.now()
				# 获取数据的key
				ks = ""
				vl = ""
				for k in list(item.keys()):
					ks = ks + str(k) + ", "
					if isinstance(item[k], str):
						vl = vl + "'" + str(item[k]) + "', " 
					else:
						vl = vl + str(item[k]) + ", "
				# ks = ks[: -2]
				# vl = vl[: -2]
				ks = ks + "insert_datetime"
				vl = vl + "'" + str(now_datetime) + "'"

				sql = "insert into " + data["table"] + " (" + ks + ") values (" + vl + ")" 
				# print(sql)
				r = mdb_do(conn, sql)

				# 将刚刚插入的记录的KEY添加到删除素银列表中
				del_index.append(data["item_list"].index(item))

				# 自增反馈数据
				insert_num += 1
				insert_key.append(item[data["key"]])

		# 在传递过来的数据中删除掉已经插入的数据
		# 因为删除掉一个元素则索引会减少1，所以需要记录删除多少个，用索引数减去相应的数量
		n = 0
		for i in del_index:
			data["item_list"].pop(i - n)
			n += 1

		# 遍历删除过插入的数据，进行对比，如果数据有变化，则更新
		for item in data["item_list"]:

			# 临时记录ID，然后删除掉数据元素，以便后面对比
			temp_id = r_list[item[data["key"]]]["id"]
			r_list[item[data["key"]]].pop("id")
			# 如果数据是datetime类型，则转为字符串
			for r in r_list[item[data["key"]]]:
				if pub_type(r_list[item[data["key"]]][r], datetime.datetime):
					r_list[item[data["key"]]][r] = str(r_list[item[data["key"]]][r])
			# 如果数据不相同，则更新数据库记录
			if not operator.eq(item, r_list[item[data["key"]]]):
				

				now_datetime = datetime.datetime.now()
				sql = "update " + data["table"] + " set "
				for i in list(item.keys()):
					if isinstance(item[i], str):
						sql = sql + i + " = '" + str(item[i]) + "', "
					else:
						sql = sql + i + " = " + str(item[i]) + ", "

				sql = sql + "update_datetime = '" + str(now_datetime) + "' where id = " + str(temp_id)

				r = mdb_do(conn, sql)
				update_num += 1
				update_key.append(item[data["key"]])

		res = {"res": "done", "insert_num": insert_num, "update_num": update_num, "insert_key": insert_key, "update_key": update_key}


	conn.close()
	return res