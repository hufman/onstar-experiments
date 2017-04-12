import requests

class OnStarClient(object):
	def __init__(self, username, password, cookies=None):
		self.username = username
		self.password = password
		self.session = requests.Session()
		if cookies is not None:
			self.session.cookies = cookies
			is_auth = self.check_login()
			if not is_auth:
				self.login()
		else:
			self.login()
		self.session.headers.update({'gm.na.requesttype': 'ajax'})
		self.session.headers.update({'Host': 'my.chevrolet.com'})
		self.session.headers.update({'Accept-Language': 'en-US,en;q=0.8'})
		self.session.headers.update({'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'})
		self.session.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'})
		self.session.headers.update({'Upgrade-Insecure-Requests': '1'})
		self.get_profile()

	def login(self):
		opening = self.session.get('https://my.chevrolet.com')
		login_data = {
			'j_username': self.username,
			'j_password': self.password,
			'ocevKey': '',
			'temporaryPasswordUsedFlag': '',
			'actc': 'true'
		}
		attempt = self.session.post('https://my.chevrolet.com/j_spring_security_check', data=login_data)
		if attempt.url == 'https://my.chevrolet.com/myvehicle/':
			# successful login
			return True
		raise ValueError("Could not authenticate")

	def check_login(self):
		request = self.session.get('https://my.chevrolet.com/profile/person')
		if len(request.history) > 0:
			# we were redirected
			return False
		return True

	def get_profile(self):
		request = self.session.get('https://my.chevrolet.com/profile/person')
		if len(request.json()['serverErrorMsgs']) > 0:
			raise Exception(request.json()['serverErrorMsgs'])
		self.profile = request.json()['data']
		return self.profile

	def get_garage(self):
		request = self.session.get('https://my.chevrolet.com/services/garage/vehicles')
		if len(request.json()['serverErrorMsgs']) > 0:
			raise Exception(request.json()['serverErrorMsgs'])
		self.garage = request.json()['data']
		return self.garage

	def get_car_evstats(self, vin):
		onstarId = self.profile['onStarAcctId']
		# prepare to fetch data
		url = 'https://my.chevrolet.com/vehicleProfile/%s/%s/createAppSessionKey' % (vin, onstarId)
		request = self.session.get(url)
		if len(request.json()['serverErrorMsgs']) > 0:
			raise Exception(request.json()['serverErrorMsgs'])

		# now try loading the evstats data
		url = 'https://my.chevrolet.com/vehicleProfile/%s/%s/evstats' % (vin, onstarId)
		request = self.session.get(url)
		if len(request.json()['serverErrorMsgs']) > 0:
			raise Exception(request.json()['serverErrorMsgs'])
		return request.json()['data']
