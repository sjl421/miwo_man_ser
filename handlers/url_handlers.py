# coding = utf-8

import tornado.web

# 编辑商品信息
class comm(tornado.web.RequestHandler):
	@tornado.gen.coroutine
	def get(self):
		self.render("comm.html")

class index(tornado.web.RequestHandler):
	@tornado.gen.coroutine
	def get(self):
		self.render("index.html")
