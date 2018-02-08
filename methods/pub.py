# coding = utf-8
import json
import tornado
import pprint
import os
import time
import socket

pp = pprint.pprint;

# 字节转字符串
def pub_btos(b):
	return b.decode(encoding = 'utf-8')

# 字符串转字节
def pub_stob(s):
	return s.encode(encoding = 'utf-8')

# 把变量变成json
def pub_json_loads(s):
	return json.loads(str(s.request.body, encoding = "utf=8"))


# 获取时间和日期的标准格式
def pub_get_time_str(item):
	if item == "date":
		return time.strftime("%Y-%m-%d", time.localtime())

	if item == "time":
		return time.strftime("%H:%M:%S", time.localtime())

# 获取时间和日期的数字串
def pub_get_time_code():
	return time.strftime("%Y%m%d%H%M%S", time.localtime())

# 获取当前时间戳
def pub_get_time_stamp():
	return int(time.time());


# 转换布尔值为0和1
def pub_bool_value(val):
	if(val is not None and val !=""):
		if val == True:
			return "1"

		elif val == False:
			return "0"

		elif val == "1":
			return True

		elif val == "0":
			return False

	if(pub_none(val)):
		return "0"

# 判断是否为空
def pub_none(var):
	if var is None or var == "":
		return True
	else:
		return False

# 检测服务器是否正常
def check_ip(ip, port):
    sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sk.settimeout(1)
    try:
        sk.connect((ip,port))
        print('server %s %d service is OK!' % (ip,port))
        return True
    except Exception:
        print('server %s %d service is NOT OK!'  % (ip,port))
        return False
    finally:
        sk.close()
    return False

# 获取传递数据
def pub_get_arg(s, item, method):
	if method == "post":
		try:
			data = pub_json_loads(s)
		except:
			data = ""
			return False
		else:
			return data[item]
	elif method == "get":
		try:
			res = s.get_argument(item)
		except:
			res = ""
			return False
		else:
			return res



from methods.mdb import *