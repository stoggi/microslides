import pyb
import os
import sys

colors = {
	'{P}': '\033[95m',
	'{B}': '\033[94m',
	'{G}': '\033[92m',
	'{Y}': '\033[93m',
	'{R}': '\033[91m',
	'{CY}': '\033[96m',
	'{Grey}': '\033[0;37m',
	'{Black}': '\033[30m',
	'{BG_CY}': '\033[46m',
	'{BG_G}': '\033[42m',
	'{E}': '\033[0m',
	'{O}': '\033[38;5;202m',
	'{W}': '\033[38;5;255m',
	'{C}': '\033[2J\033[;H',
	'{reset}': '\033[0;0H',
	'~': '\033[1C',
	'{title}': open('title.txt').read()
}

clear_screen = '\033[2J\033[;H'

switch = pyb.Switch()
led = pyb.LED(1)

def read_slide(filename):
	with open(filename, 'r') as f:
		return f.read()

def parse_slide(slide):
	for key, escape in colors.items():
		slide = slide.replace(key, escape)
	return slide.split('{pause}')

def render_slide(filename):
	raw_slide = read_slide(filename)
	parsed_slide = parse_slide(raw_slide)
	
	for segment in parsed_slide:
		yield segment

def user_input():
	while(True):
		command = sys.stdin.read(1)
		if command in 'npq':
			return command

def calibrate():
	with open("calibration.txt", 'r') as f:
		data = f.read()
		while(True):
			print(clear_screen, end="")
			print(data, end="")
			pyb.delay(200)

def play(slide_folder, start=0):
	slide_files = slides(slide_folder)
	index = start
	total = len(slide_files)

	while True:
		print(clear_screen, end="")
		if (index >= total):
			break
		for segment in render_slide(slide_files[index]):
			print(segment, end="")
			command = user_input()
			if (command == 'p'):
				index -= 2
				break
			elif (command == 'q'):
				index = total
				break
			elif (command == 'n'):
				pass
		index += 1
	print()

def slides(foldername):
	slides = os.listdir(foldername)
	slides.sort()
	return [foldername + '/' + slide for slide in slides]

def list(filename):
	for index, name in enumerate(slides(filename)):
		print("[{}] = '{}'".format(index, name.strip()))

def help():
	print("Slideshow version 0.1 by jeremy@stott.co.nz")
	print("")
	print("calibrate()      Calibrates the display by printing a box")
	print("play(slide=1)    Plays the slideshow (from slide n)")
	print("list()           List the slides in order")
	print("help()           Print this help message")

