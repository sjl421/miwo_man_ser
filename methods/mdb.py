# coding = utf-8

from methods.pub import *
import pymysql
# db = pymysql.connect(host='localhost', port=3306, user='root', passwd='xufei727',db='bilishop_wx_0.1.3')

mdb = {
	"host": "localhost",
	"port": 3306,
	"user": "root",
	"passwd": "xufei727",
	"db": "miwo_man_ser"
}



def mdb_get_conn():
	return pymysql.connect(**mdb)


def mdb_cm(conn, sql, var):
	cur = conn.cursor()
	return cur.mogrify(sql, var)


# 获取一条信息
def mdb_get_one(conn, sql):
	# 进行查询
	cur = conn.cursor()
	cur.execute(sql)
	result_list = cur.fetchone()
	# 导出字段
	des_list = []
	if not pub_none(cur.description) and not pub_none(result_list):
		for item in cur.description:
			des_list.append(item[0])
		if des_list and result_list:
			result = dict(zip(des_list, result_list))
			return result
		else:
			return False
	else:
		return False
# 获取带序号的数据
def mdb_get_all_num(conn, sql):
	cur = conn.cursor()
	cur.execute(sql)
	result_list = cur.fetchall()

	result = []
	des_list = []
	for item in cur.description:
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
# 获取数组数据
def mdb_get_all_arr(conn, sql):
	cur = conn.cursor()
	cur.execute(sql)
	result_t = cur.fetchall()
	result = []
	for i in result_t:
		for j in i:
			result.append(j)
	return result
# 获取全部原始数据
def mdb_get_all(conn, sql):
	cur = conn.cursor()
	cur.execute(sql)
	result_list = cur.fetchall()

	result = []
	des_list = []
	for item in cur.description:
		des_list.append(item[0])

	for item in result_list:
		item_temp = list(item)
		result.append(dict(zip(des_list, item_temp)))
	return result


# 执行一条语句
def mdb_do(conn, sql):
	cur = conn.cursor()
	try:
		cur.execute(sql)
		conn.commit()
	except:
		conn.rollback()
		return False
	else:
		return True

