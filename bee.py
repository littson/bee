import os
import urllib
import logging
import yaml

from google.appengine.api import users
from google.appengine.ext import ndb

import jinja2
import webapp2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'])

class MainPage(webapp2.RequestHandler):

    def get(self):
        user = users.get_current_user()

        if not user:
            self.redirect(users.create_login_url(self.request.uri))
            return

        template_values = {
                'nickname': user.nickname(),
                }

        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))

class Bot(webapp2.RequestHandler):

    def get(self):
        botId = self.request.get('type')

        botConf = self.loadBotConf(botId)

        if(not botConf):
            logging.exception('can not find conf for {0}'.format(botId))
            self.response.write('A server error occurred!')
            self.response.set_status(500)
            return

        mod = __import__('bots')
        botFunc = getattr(mod, '%s' % botId)
        result = botFunc(botConf)
        logging.info('result:{0}'.format(result))
        self.response.write('ok')

    def loadBotConf(self, botId):
        f = file('accounts.yaml', 'r')
        confs = yaml.load(f)
        return confs[botId]

application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/bot', Bot),
    ], debug=True)

