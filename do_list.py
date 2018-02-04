# coding = utf-8
import time
import sched
import requests

from methods.pub import *

# 同步商品资料
def syn_comm():
	# 发送商品数据
	cs_url = "http://localhost/methods/comm"
	request_headers = {"Content-Type": "application/x-www-form-urlencoded"}
	p = '{"act":"syn_comm"}'
	r = requests.post(cs_url, data = p, headers = request_headers)
	res = pub_btos(r.content)
	print(res);
	print(res)

def syn_repertory():
	cs_url = "http://localhost/methods/repertory"
	request_headers = {"Content-Type": "application/x-www-form-urlencoded"}
	p = '{"act": "syn_repertory"}'
	r = requests.post(cs_url, data = p, headers = request_headers)
	res = pub_btos(r.content)
	print(res)

def syn_spe():
	cs_url = "http://localhost/methods/spe"
	request_headers = {"Content-Type": "application/x-www-form-urlencoded"}
	p = '{"act": "syn_spe"}'
	r = requests.post(cs_url, data = p, headers = request_headers)
	res = pub_btos(r.content)
	print(res)


# 获取要执行列表的间隔时间
mconn = mdb_get_conn()
sql = "select value from info where id = 1"
res = mdb_get_one(mconn, sql)
if res:
	do_time = int(res["value"])
else: do_time = False
mconn.close()

ip_list = [{"ip": "10.0.0.23", "port": 1433}, {"ip": "bilishop.cc", "port": 8001}]

# do_time = 3

while True:
	if do_time:
		check = True
		for item in ip_list:
			if not check_ip(item["ip"], item["port"]):
				check = False
				host = str(item["ip"]) + " : " + str(item["port"])
				res = json.dumps({"error_type": "server down"})
				pub_insert_log(host, "error", res)

		if check:
			syn_comm()
			time.sleep(3)
			syn_repertory()
			time.sleep(3)
			syn_spe()

	time.sleep(do_time)
