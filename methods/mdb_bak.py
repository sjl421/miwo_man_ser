# coding = utf-8

import pymysql
from methods.pub import *

server = "localhost"
user = "root"
password = "xufei727"
database = "biligo_rp"

mdb = False

mdb = pymysql.connect(host='localhost', port=3306, user='root', passwd='xufei727',db='biligo_rp')

mcur = False

if mdb:

	mcur = mdb.cursor()

def mdb_cm(sql, var):
	return mcur.mogrify(sql, var)

# 获取一条信息
def mdb_get_one(sql):
	if not mcur:
		return False
	else:

		# 进行查询
		mcur.execute(sql)

		result_list = mcur.fetchone()
		# 导出字段
		des_list = []

		if not pub_none(mcur.description) and not pub_none(result_list):

			for item in mcur.description:
				des_list.append(item[0])

			result = dict(zip(des_list, result_list))
			return result
		else:
			return False

def mdb_get_all_num(sql):
	if not mcur:
		return False
	else:
		mcur.execute(sql)
		result_list = mcur.fetchall()

		result = []
		des_list = []
		for item in mcur.description:
			des_list.append(item[0])

		des_list.append("num")

		num = 0
		for item in result_list:
			item_temp = list(item)
			item_temp.append(num)
			# item_temp.append(0)
			result.append(dict(zip(des_list, item_temp)))
			num += 1
		return result


def mdb_get_all_arr(sql):
	if not mcur:
		return False
	else:
		mcur.execute(sql)
		result_t = mcur.fetchall()
		result = []
		for i in result_t:
			for j in i:
				result.append(j)
		return result

def mdb_get_all(sql):
	if not mcur:
		return False
	else:
		mcur.execute(sql)
		result_list = mcur.fetchall()

		result = []
		des_list = []
		for item in mcur.description:
			des_list.append(item[0])

		for item in result_list:
			item_temp = list(item)
			result.append(dict(zip(des_list, item_temp)))
		return result

def mdb_do(sql):
	if not mcur and mdb:
		return False
	else:
		mcur.execute(sql)
		mdb.commit()
		return True

# 获取服务器
def pub_get_host():
	if not mcur and mdb:
		return False
	else:
		sql = "select value from info where id = 0"
		info = mdb_get_one(sql)
		return info["value"]


# 添加操作日志
def pub_insert_log(host, oper_type, res):
	if not mcur and mdb:
		return False
	else:
		res = json.loads(res)
		oper_date = pub_get_time_str("date")
		oper_time = pub_get_time_str("time")

		sql = mdb_cm("insert into `biligo_rp`.`log` ( `oper_time`, `res`, `ord`, `remark`, `oper_date`, `type`, `host`, `res_code`) values ( %s, '', 0, '', %s, %s, %s, %s)", (str(oper_time),  str(oper_date), str(oper_type), str(host), str(res)))

		if(mdb_do(sql)):
			return True
		else:
			return False