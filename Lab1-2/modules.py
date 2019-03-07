class String:

	def __init__(self, strs):
		self.string = strs

	def __add__(self, strs):
		return self.string+str(strs)

	def __radd__(self, strs):
		return str(strs)+self.string

	def __contains__(self, strs):
		return str(strs) in self.string

	def __eq__(self, strs):
		return self.string == str(strs)

	def __ne__(self, strs):
		return self.string != str(strs)

	def __str__(self):
		return self.string

	def __len__(self):
		return len(self.string)

	def readints(self):
		#Function to read integers from created string

		s = []
		
		#Variable to check, is we started to read integer
		start = False 

		ord0, ord9 = ord("0"), ord("9") #precalculated

		for i in self.string:

			if ord0 <= ord(i) <= ord9:
			
				if not start:
					s.append(i)
					start = True
			
				else:
					s[len(s)-1] += i

			else:
				start = False

		return [int(i) for i in s]

	def rcut(self, tosize):
		#Function to cut string to new size from right (remove all right part after fixed size)
		self.string = self.string[:tosize]


	def find(self, strs, beg=0, end=-1):

		if end == -1:
			end = len(self.string)

		return self.string.find(strs, beg, end)

	def count(self, strs):
		return self.string.count(strs)
		
