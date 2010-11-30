import cgi
import os
import logging
import time
import datetime


from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from google.appengine.ext.webapp import template

# Can be redifined by UserSettings
PAGESIZE=31

class UserSettings():
  def __init__(self):
      self.__setOffset(0)
      self.author = None
      self.userConfigFromDB = None

  def __setOffset(self, offsetInHours):
    self.offsetHours = offsetInHours
    self.tzOffset = datetime.timedelta(hours=offsetInHours)

  def setUserSettings(self, author, offsetInHours, pageSize):
    self.__setOffset(offsetInHours)
    if author:
        if self.author != author:
            self.fetchDBUserConfig(author)

        self.userConfigFromDB.tzOffsetHours = offsetInHours
        self.userConfigFromDB.pageSize = pageSize
        self.userConfigFromDB.put()

  def getPageSize(self):
    if self.userConfigFromDB == None:
        return PAGESIZE
    else:
        return self.userConfigFromDB.pageSize

  def fetchDBUserConfig(self, author):
    q = UserConfig.all()
    q.filter('author =', author)
    results = q.fetch(2)
    assert len(results) < 2

    self.author = author

    if len(results) == 0:
        self.userConfigFromDB = UserConfig()
        self.userConfigFromDB.author = author
        #self.userConfigFromDB.tzOffsetHours = 0
        self.userConfigFromDB.put()
    else:
        self.userConfigFromDB = results[0]

    self.__setOffset(self.userConfigFromDB.tzOffsetHours)
        


userSettings = UserSettings()

class PulsHist(db.Model):
  author = db.UserProperty()
  pulse = db.StringProperty(multiline=False)
  remark = db.StringProperty(multiline=True)
  # UTC
  date = db.DateTimeProperty(auto_now_add=True)

class UserConfig(db.Model):
  author = db.UserProperty()
  tzOffsetHours = db.IntegerProperty(default=0)
  pageSize = db.IntegerProperty(default=PAGESIZE)


##########################################



class MainPage(webapp.RequestHandler):
  def get(self):
    nextPage = self.request.get('page')
    if not nextPage:
      nextPage = 0
    else:
      nextPage = int(nextPage)

    # logging.info("nextPage = %s" % nextPage)

    user = users.get_current_user()
    if user:
      global PAGESIZE
      userSettings.fetchDBUserConfig(user)
      url = users.create_logout_url(self.request.uri)
      url_linktext = 'Logout'
      PAGESIZE = userSettings.getPageSize()
    else:
      url = users.create_login_url(self.request.uri)
      url_linktext = 'Login'

    query = PulsHist.gql("""
        WHERE author = :author
        ORDER BY date DESC"""
            ,author=user)

    pulses = query.fetch(PAGESIZE, nextPage*PAGESIZE)
    for pulse in pulses:
        pulse.date = pulse.date + userSettings.tzOffset

    if len(pulses) == PAGESIZE:
        nextPage = nextPage + 1

    if len(pulses) > 0:
        lastPulse = pulses[0].pulse
    else:
        lastPulse = 60


    template_values = {
      'User': user,
      'pulses': pulses,
      'url': url,
      'url_linktext': url_linktext,
      'nextPage': nextPage,
      'lastPulse': lastPulse,
      'date': datetime.datetime.now() + userSettings.tzOffset,
      }

    if user:
        template_values['showSettingsLink'] = 1

    path = os.path.join(os.path.dirname(__file__), 'index.html')
    self.response.out.write(template.render(path, template_values))
    

class Insert(webapp.RequestHandler):
  def post(self):
    newPulseEntry = PulsHist()
    setEntry(self.request, users.get_current_user(), newPulseEntry)

    self.redirect('/')

class Change(webapp.RequestHandler):
  def get(self):
    id = db.Key(self.request.get('id'))
    author = users.get_current_user()

    pulseEntity = db.get(id)
    pulseEntity.date = pulseEntity.date + userSettings.tzOffset
    if pulseEntity.author == author:
      template_values = {
        'pulse': pulseEntity,
        }
      path = os.path.join(os.path.dirname(__file__), 'change.html')
      self.response.out.write(template.render(path, template_values))
    else:
      self.redirect('/')

class Delete(webapp.RequestHandler):
  def get(self):
    id = db.Key(self.request.get('id'))
    author = users.get_current_user()

    pulseEntity = db.get(id)
    if pulseEntity.author == author:
      pulseEntity.delete()

    self.redirect('/')


class Settings(webapp.RequestHandler):
  def get(self):
    author = users.get_current_user()
    if author == None:
        self.redirect('/')
        return

    template_values = {
      'User': author,
      'tzOffsetHour': userSettings.offsetHours,
      'pageSize': userSettings.getPageSize(),
      }
    path = os.path.join(os.path.dirname(__file__), 'settings.html')
    self.response.out.write(template.render(path, template_values))

  def post(self):
    author = users.get_current_user()

    try:
        offset = int(self.request.get('tzoffset'))

        pageSize = int(self.request.get('pageSize'))
        userSettings.setUserSettings(author, offset, pageSize)
    except ValueError:
      pass

    self.redirect('/')


class StoreChange(webapp.RequestHandler):
  def post(self):
    id = db.Key(self.request.get('id'))
    author = users.get_current_user()

    pulseEntity = db.get(id)
    setEntry(self.request, author, pulseEntity)

    self.redirect('/')


def setEntry(request, currentUser, entry):
    if currentUser:
      entry.author = currentUser
      entry.remark = request.get('remark')[:200]
    else:
      entry.remark = 'No remarks for user None'

    entry.pulse = request.get('pulse')[:3]
    ds = request.get('date')

    try:
      foo = int(entry.pulse)
      entry.date = datetime.datetime(*time.strptime(ds, "%Y-%m-%d %H:%M")[0:5])
      entry.date = entry.date - userSettings.tzOffset
      entry.put()
    except ValueError:
      pass

application = webapp.WSGIApplication(
                                     [('/', MainPage),
                                      ('/insert', Insert),
                                      ('/delete', Delete),
                                      ('/edit', StoreChange),
                                      ('/settings', Settings),
                                      ('/setUserConfig', Settings),
                                      ('/change', Change)],
                                     debug=True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()
