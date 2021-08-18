
class DDH2Exception(Exception):
	def __init__(self, response):
		self.status_code = response.status_code
		self.text = response.text
		
	def __repr__(self):
		return 'DDH2Exception [{}]: {}'.format(self.status_code, self.text)
	
	def __str__(self):
		return self.text