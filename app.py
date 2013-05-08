import json
import urllib
import logging
import os.path
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define, options

from markov_by_char import CharacterMarkovGenerator

define("port", default = 8000, help = "Run on the given port ", type = int)
define("n", default = 5, help = "length of n-gram ", type = int)

class Application(tornado.web.Application):
	def __init__(self):
		handlers = [
			(r"/", MainHandler),
			(r"/markov", MarkovHandler),
			(r"/about", AboutHandler)
		]
		settings = dict(
			template_path = os.path.join(os.path.dirname(__file__), "templates"),
			static_path = os.path.join(os.path.dirname(__file__), "static")
		)
		tornado.web.Application.__init__(self, handlers, **settings)


class MainHandler(tornado.web.RequestHandler):
	def get(self):
		self.render('main.html')


class MarkovHandler(tornado.web.RequestHandler):
	def get(self):
		screen_name = self.get_argument('screen_name')
		params = {'count':200, 'screen_name':screen_name}

		# fetch tweets
		resp = urllib.urlopen(
			'http://api.twitter.com/1/statuses/user_timeline.json?' + \
			 urllib.urlencode(params))
		rawjson = resp.read()
		generator = CharacterMarkovGenerator(options.n, 140)
		data = json.loads(rawjson)
		for tweet in data:
				generator.feed(tweet['text']) # this shows the text content of the tweet
		self.write(generator.generate())

class AboutHandler(tornado.web.RequestHandler):
	def get(self):
		self.render('about.html')


if __name__ == "__main__":
	tornado.options.parse_command_line()
	http_server = tornado.httpserver.HTTPServer(Application())
	http_server.listen(options.port)
	tornado.ioloop.IOLoop.instance().start()


