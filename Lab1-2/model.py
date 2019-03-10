from modules import String
import os.path

class PictureFile:

	def __init__(self, path=""):

		self.width = 0
		self.height = 0
		self.frames = 0
		self.frame = 0

		self.caret = 0
		self.firstframe = 0
		self.filepath = path
		self.file = None
		self.opened = False


	def get_size(self):
		return self.width, self.height


	def set_file_path(self, path=""):

		self.close()
		self.filepath = path

		self.width = 0
		self.height = 0
		self.frames = 0
		self.frame = 0
		
		self.caret = 0
		self.firstframe = 0
		self.file = None
		self.opened = False


	def open(self):

		if os.path.isfile(self.filepath):
			self.file = open(self.filepath)
			self.opened = True


	def read_meta(self):

		if not self.opened:
			return None

		default_meta_size = 60

		#If file from 1st lab
		if self.file.read(1) != "{":
			
			self.firstframe = 2
			self.caret = self.firstframe
			
			self.width = 3
			self.height = 3
			self.frames = 12

			self.file.seek(self.firstframe, 0)
			
		#If file from 2nd lab
		else:

			is_meta_loaded = False
			while not is_meta_loaded:

				self.file.seek(0)
				submeta = String(self.file.read(default_meta_size))
				submeta.rcut(submeta.find("["))

				#Add reading meta size, while word "animation" not 
				#	contains in main string:
				if "animation" not in submeta:
					default_meta_size += 5
					continue

				self.width, self.height, self.frames = submeta.readints()

				self.firstframe = len(submeta)+1
				self.caret = self.firstframe

				self.file.seek(self.firstframe, 0)

				is_meta_loaded = True


	def __get_pixel_data(self):
		#Reading subsring from file (pixel data), cut side after closing brace,
		#	and calculate count of moving to new line and tabs (for lab1)

		max_pixel_info_size = 20

		self.file.seek(self.caret, 0)
		
		pixeldata = String(self.file.read(max_pixel_info_size))
		pixeldata.rcut(pixeldata.find("]"))
		nlinecnt = pixeldata.count("\n") + pixeldata.count("\t")

		return pixeldata, nlinecnt


	def __read_pixel(self):
		#Function to get pixel color from data
		#Also, can re-read from start (to make repeatable animation)

		pixeldata, nlinecnt = self.__get_pixel_data()

		#If pixel data is empty, get to the entrance of animation part
		if len(pixeldata) == 0:
			self.caret = self.firstframe
			pixeldata, nlinecnt = self.__get_pixel_data()
			self.frame = 1
		
		self.caret += len(pixeldata)+nlinecnt+3

		return pixeldata.readints()


	def read_next_frame(self):
		#Function to read frame - all pixels data
		
		self.frame += 1
		pix = []
		for i in range(self.width*self.height):
			pix.append(self.__read_pixel())

		return pix


	def iter_next_frame(self):
		#Function to read frame - iterable data

		for i in range(self.width*self.height):
			yield self.__read_pixel()


	def close(self):

		if not self.opened:
			return None

		self.opened = False
		return self.file.close()


