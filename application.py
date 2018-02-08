# coding = utf-8
# 一些基本的设置
# 注意要讲调试的设置在发布之前去掉。

import tornado.web
import os
import base64
import uuid
#-------------------------------#
from handlers.url_handlers import *
# 导入api
from api.restk import *
from api.item_info import *
from api.supplier_info import *
from api.sale_record import *
from api.category_info import *
from api.get_ip import *

url = [
	# 页面
	# (r"/", index),
	# api
	(r"/api/get_ip", api_get_ip),
	(r"/api/restk", restk),
	(r"/api/item_info", api_item_info),
	(r"/api/supplier_info", api_supplier_info),
	(r"/api/sale_record", api_sale_record),
	(r"/api/category_info", api_category_info),
	]
#--------------------------------
# 设置MODULES
# 顶部菜单
# class top_menu_module(tornado.web.UIModule):
# 	def render(self):
# 		return self.render_string("module_top_menu.html")

# # 左侧菜单
# class left_body_module(tornado.web.UIModule):
# 	def render(self):
# 		return self.render_string("module_left_body.html")

modules = {
	# "top_menu": top_menu_module,
	# "left_body": left_body_module,
}
#---------------------------------------


# 设置
settings = dict(
	template_path = os.path.join(os.path.dirname(__file__), "templates"),
	static_path = os.path.join(os.path.dirname(__file__), "statics"),
	debug = True, # 调试模式，正式发布时需要去掉
	# cookie_secret = "ldpfwUB9QVK31iEMx0XR538r0SO1zEALj+tcpdozAuQ="
	cookie_secret = base64.b64encode(uuid.uuid4().bytes + uuid.uuid4().bytes),
	# xsrf_cookies = True,
	)

application = tornado.web.Application(
	handlers = url,
	ui_modules = modules,
	**settings
	)