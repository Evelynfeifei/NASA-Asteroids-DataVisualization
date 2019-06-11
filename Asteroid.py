class Asteroid:
	def __init__(self, link, id, name, nasa_jpl_url, mph, miles):
		self.link = link
		self.id = id
		self.name = name
		self.nasa_jpl_url = nasa_jpl_url
		self.mph = mph
		self.miles = miles

	def ToList(self):
		return [self.link, self.id, self.name, self.nasa_jpl_url, self.mph, self.miles]

	def __eq__(self, other):        
		try:
			if(isinstance(other, self) and self.ToList()==other.ToList()):
				return True
		except:
			raise ValueError("Type comparison with non-Asteroid object")
			raise NotImplementedError
		return False

	def __repr__(self):
		raise NotImplementedError

	def __str__(self):
		raise NotImplementedError