import pytest
from model import PictureFile

def test_file_lab1_p1():

	file = PictureFile("tests/lab1f1.json")
	file.open()
	file.read_meta()
	file.close()

	assert file.width == file.height == 3


def test_file_lab1_p2_default():

	file = PictureFile("tests/lab1f2.json")
	file.open()
	file.read_meta()

	data = "["
	data += ",".join(
		[
			str(file.read_next_frame()).replace(" ", "")
			for i in range(file.frames) 
		])
	data += "]"

	file.close()
	
	#---------------

	file = open("tests/lab1f2.json")
	defdata = file.read()
	file.close()

	#---------------
	assert data == defdata


def test_file_lab1_p2_iterative():

	file = PictureFile("tests/lab1f2.json")
	file.open()
	file.read_meta()

	data = "["
	data += ",".join(
		[
			str([
				j for j in file.iter_next_frame()
			]).replace(" ", "")
			for _ in range(file.frames) 
		])
	data += "]"

	file.close()
	
	#---------------

	file = open("tests/lab1f2.json")
	defdata = file.read()
	file.close()

	#---------------
	assert data == defdata


def test_file_lab2():
	
	file = PictureFile("tests/lab2f1.json")
	file.open()
	file.read_meta()
	file.close()
	
	assert file.width == file.height == 3


def test_files_arr_of_ites_equal_default():

	file = PictureFile("tests/lab2f1.json")
	file.open()
	file.read_meta()

	defdata = ",".join([
		str(file.read_next_frame())
		for i in range(file.frames)
	])

	iterdata = ",".join([
		str([
			j for j in file.iter_next_frame()
		])
		for _ in range(file.frames) 
	])
	file.close()

	assert defdata == iterdata


def test_check_frames():

	file = PictureFile("tests/lab2f1.json")
	file.open()
	file.read_meta()

	x = file.read_current_frame()
	y = file.read_current_frame()
	z = file.read_next_frame()

	assert x == y
	assert x != z
	assert y != z
	