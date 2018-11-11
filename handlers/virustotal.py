import re
import threading
import requests
from BeautifulSoup import BeautifulSoup as soup

class VIRUSTOTAL:

	COOKIES = {}
	SERVICE = "VIRUSTOTAL"
	LOCK = threading.Semaphore(value=1)
	URL = "https://www.virustotal.com/en/domain/%s/information/"
	REGEXP = "([a-z0-9]+[.])+%s"
	TIMEOUT = 10
	RESPONSE = ""
	SUBDOMAINS = []

	def __init__(self, _class, _dm, _hd, _ag):
		self.session = requests.Session()
		self.baseclass = _class
		self.domain = _dm
		self.URL = self.URL % (self.domain)
		self.REGEXP = self.REGEXP % (self.domain)
		self.headers = self.headerer(_hd, _ag)
		self.agent = _ag

	def headerer(self, headers, _ag):
		headers['User-Agent'] = _ag
		headers['Referer'] = self.URL
		return headers

	def execute(self):
		_th = threading.Thread(target=self.request)
		_th.daemon = True
		_th.start()

	def request(self):
		self.baseclass.THREADS += 1

		try:
			req = self.session.get(self.URL, headers=self.headers, cookies=self.COOKIES, timeout=self.TIMEOUT)
			if req.status_code < 400:
				self.RESPONSE = req.text
				self.extract()
				self.append()

		except Exception, e:
			self.append()

		self.baseclass.THREADS -= 1

	def append(self, error=True):
		self.LOCK.acquire()
		self.baseclass.add( self.SUBDOMAINS, self.SERVICE )
		self.baseclass.pushtoscreen( self.SUBDOMAINS, self.SERVICE, error )
		self.LOCK.release()

	def extract(self):
		_html = soup(self.RESPONSE)
		for cite in _html.findAll("div", attrs={'class': 'enum '}):
			sub = re.search(self.REGEXP, cite.text, re.IGNORECASE)
			if sub:
				self.SUBDOMAINS.append(sub.group())