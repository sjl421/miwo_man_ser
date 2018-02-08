# coding = utf-8

import tornado.web

class api_get_ip(tornado.web.RequestHandler):
	@tornado.gen.coroutine
	def get(self):
		# ip = self.headers.get("X-Real-Ip", self.headers.get("X-Forwarded-For", remote_ip))
		ip = self.request.remote_ip
		self.finish(ip)