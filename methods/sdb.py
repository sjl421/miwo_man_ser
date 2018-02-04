# coding = utf-8

import pymssql
from methods.pub import *



def sdb_get_conn():
	server = "10.0.0.23"
	user = "sa"
	password = "xufei727"
	database = "hbposv8"
	return pymssql.connect(server, user, password, database, charset="UTF-8")

# def sdb_check():
# 	if check_ip(server, 1433):
# 		global sconn
# 		global scur
# 		sconn = pymssql.connect(server, user, password, database, charset="UTF-8")
# 		scur = sconn.cursor()

# 		return True
# 	else:
# 		return False


def sdb_cm(conn, sql, var):
	if conn:
		cur = conn.cursor()
		return scur.mogrify(sql, var)
	else:
		return False
	# if sdb_check():
	# 	return scur.mogrify(sql, var)
	# else:
	# 	return False

# 获取一条信息
def sdb_get_one(conn, sql):
	if conn:
		scur = conn.cursor()
		# 进行查询
		scur.execute(sql)

		result_list = scur.fetchone()
		# 导出字段
		des_list = []
		for item in scur.description:
			des_list.append(item[0])

		result = dict(zip(des_list, result_list))
		return result
	else:
		return False
	# if sdb_check():
	# 	# 进行查询
	# 	scur.execute(sql)

	# 	result_list = scur.fetchone()
	# 	# 导出字段
	# 	des_list = []
	# 	for item in scur.description:
	# 		des_list.append(item[0])

	# 	result = dict(zip(des_list, result_list))
	# 	return result
	# else:
	# 	return False

def sdb_get_all_num(conn, sql):
	if conn:
		scur = conn.cursor()
		scur.execute(sql)
		result_list = scur.fetchall()

		result = []
		des_list = []
		for item in scur.description:
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
	else:
		return False

	# if sdb_check():
	# 	scur.execute(sql)
	# 	result_list = scur.fetchall()

	# 	result = []
	# 	des_list = []
	# 	for item in scur.description:
	# 		des_list.append(item[0])

	# 	des_list.append("num")

	# 	num = 0
	# 	for item in result_list:
	# 		item_temp = list(item)
	# 		item_temp.append(num)
	# 		# item_temp.append(0)
	# 		result.append(dict(zip(des_list, item_temp)))
	# 		num += 1
	# 	return result
	# else:
	# 	return False


def sdb_get_all(conn, sql):
	if conn:
		scur = conn.cursor()
		scur.execute(sql)
		result_list = scur.fetchall()

		result = []
		des_list = []
		for item in scur.description:
			des_list.append(item[0])

		for item in result_list:
			item_temp = list(item)
			result.append(dict(zip(des_list, item_temp)))
		return result
	else:
		return False

	# if sdb_check():
	# 	scur.execute(sql)
	# 	result_list = scur.fetchall()

	# 	result = []
	# 	des_list = []
	# 	for item in scur.description:
	# 		des_list.append(item[0])

	# 	for item in result_list:
	# 		item_temp = list(item)
	# 		result.append(dict(zip(des_list, item_temp)))
	# 	return result
	# else:
	# 	return False

def sdb_do(conn, sql):
	if conn:
		scur = conn.cursor()
		scur.execute(sql)
		db.commit()
		return True
	else:
		return False

	# if sdb_check():
	# 	scur.execute(sql)
	# 	db.commit()
	# 	return True
	# else:
	# 	return False

