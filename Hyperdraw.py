import pygame, time
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

from math import *


# GUI Stuff
from tkinter import *
# ^ Standard library GUI module

# Some unfortunate workarounds for tkinter not being able
# to interact with the main program variables. (These variables
# are used as a sort of messenger)
global tkReturnVar
global screen

# Allows the tk window to be accessed from anywhere
global window
global screen

def gWrap(function, returnFunction=True):
	def inner(*args, **kwargs):
		def work():
			out = function(*args, **kwargs)
			if returnFunction:
				global tkReturnVar
				tkReturnVar = out
		return work
	return inner

def gGiveInputs(*args, **kwargs):
	def work():
		out = function(*args, **kwargs)
		global tkReturnVar
		tkReturnVar = out
	return work

# Sets up application window
def gOpen():
	global window
	global screen
	window = Tk()
	screen = Frame(window)
	screen.pack()

def gClose():
	global window
	window.destroy()

# Tkinter function to give the user a range of options (buttons)
def gMenu(*choices):
	# Gives the menu function its own section of the window
	frame = Frame(screen)
	frame.pack()
	# Creates versions of a function that sets the 'messenger' variable to a specific number,
	# for use in the menu buttons (and so the internal function cannot take any perameters,
	# since this is not allowed in buttons)
	def numberReturn(number):
		def wrapper():
			# Sets messenger variable to specified number
			global tkReturnVar
			tkReturnVar = number

			# Removes the menu section of the application window
			# (since a choice has been made so it is no longer needed)
			frame.destroy()
		return wrapper

	def menuWork(choices):
		# Initializes variables
		buttons = []
		num = 1

		# For each option, creates a button that will set the 'messenger' variable to its option number
		for choice in choices:
			buttons.append(Button(frame, text=str(num) + ".  " + choice, command=numberReturn(num)))
			num += 1
			buttons[num - 2].pack()

		# Waits for an option to be selected, then returns the option number selected
		screen.wait_window(frame)
		return tkReturnVar
	return menuWork(choices)

# A tkinter version of the basic input function.
# Used by all of the more advanced input functions.
def gInput(prompt=""):
	# Function to set the 'messenger' variable to the text entered
	def returnTime(*args):
		global tkReturnVar
		tkReturnVar = textEntry.get()
		frame.destroy()

	# Gives the function its own section of the window
	frame = Frame(screen)
	frame.pack()

	# Displays the prompt on the window
	promptLabel = Label(frame, text=prompt)
	promptLabel.pack()

	# Creates a text entry box and displays it on the screen
	textEntry = Entry(frame)
	textEntry.pack()
	# Binds the ENTER key so that it will return the text entered
	textEntry.bind('<Return>', returnTime)

	# Adds an on-screen button to return the entered text,
	# Acts as an alternative to pressing ENTER
	enter = Button(frame, text="ENTER", command=returnTime)
	enter.pack()

	# Waits until ENTER is pressed / clicked, then returns
	# the text that the user entered
	screen.wait_window(frame)
	return tkReturnVar

# A tkinter version of 'print' with only basic arguments
def gPrint(text="\n"):
	frame = Frame(screen)
	frame.pack()

	# Creates a label containing the desired text and displays it
	Label(frame, text=text).pack()

# A basic procedure to wait for the user to continue
def gContinue(text="CONTINUE"):
	# Creats a button labeled 'CONTINUE', which clears the entire screen when clicked
	continueButton = Button(screen, text=text, command=clear)
	continueButton.pack()

	# Waits for the continue button to be clicked before continuing
	window.wait_window(screen)

# A procedure to clear the tkinter screen
def clear():
	# Removes all objects on the screen
	global screen
	screen.destroy()

	# Creates a blank area for new objects to be put into
	screen = Frame(window)
	screen.pack()

# Decorator to error manage functions
def errorManage(manageType="Ignore",
				returnOrNo="No",
				errorMessage="Sorry, there was an error",
				hardError="No"):
	# ^ Outer function just serves to enable perameters to be entered

	# Takes a subroutine to be error mangaged
	def errorManageReturn(function):
		# Attempts to execute a subroutine, takes apropriate action if it raises an error
		def errorManageProcedure(*args, **kwargs):
			try:
				# Attempts to execute the subroutine
				returnVar = function(*args, **kwargs)

				# Returns the output of the subroutine if it is a function
				if returnOrNo.upper() == "YES":
					return returnVar
			except:
				# Displays the specified error message if the subroutine raises an error
				gPrint(errorMessage)

				# If the subroutine is intended to run repeatedly until it is succesful, trys again
				if manageType.upper() == "REPEAT":
					returnVar = errorManageProcedure(*args, **kwargs)
					if returnOrNo == "YES":
						return returnVar

				# If the subroutine is likely to raise the same errors again, e.g.
				# if it takes no new input, the program will continue as normal
				elif manageType.upper() == "IGNORE":
					if hardError.upper() == "NO":
						pass
					else:
						# If the error is a hard error (e.g. a required piece of data is missing)
						# the program will close after the user acknowledges the error message
						tkContinue()
						exit()
		return errorManageProcedure
	return errorManageReturn

# An error managed function to get an integer input from the user
def mkInt(prompt=""):
	try:
		return int(notNone(prompt))
	except:
		# If the user does not enter an integer, it tries again until a valid input is given
		gPrint("Not a valid integer")
		return mkInt(prompt)

# An error managed function to get a number input from the user
# (works on the same principle as mkInt)
def mkFloat(prompt=""):
	try:
		return float(notNone(prompt))
	except:
		gPrint("Not a valid number")
		return mkFloat(prompt)

# An error managed function to get an input from the user that is not nothing
# (works on the same principle as mkInt)
def notNone(prompt=""):
	returnVar = gInput(prompt)
	if not returnVar == None:
		return returnVar
	else:
		gPrint("You Must Enter An Input")
		return notNone(prompt)

def gInputSatisfies(prompt="", condition=lambda x:x>0):
	num = mkFloat(prompt)
	if condition(num):
		return num
	else:
		gPrint("The condition was not met")
		return gInputSatisfies(prompt, condition)

def gButton(text, function, size=None):
	frame = Frame(screen)
	frame.pack()

	if size != None:
		button = Button(frame, text=text, command=function)
	else:
		button = Button(frame, text=text, command=function, height=size[0], width=size[1])
	button.pack()

# W.I.P
def gButtonMatrix(textMatrix, functionMatrix, size=None):
	frame = Frame(screen)
	frame.pack()

	maxLength = 0
	for row in textMatrix:
		if len(row) > maxLength:
			maxLength = len(row)
	for row in textMatrix:
		row += ["<Blank>"]*(maxLength-len(row))
	print(textMatrix)

	if size == None:
		for row in range(len(textMatrix)):
			for column in range(len(row)):
				if textMatrix[row][column] != "<Blank>":
					button = Button(frame, text=textMatrix[row][column], command=functionMatrix[row][column])
				button.grid(row=row, column=column, sticky=W)
	else:
		for row in range(len(textMatrix)):
			for column in range(len(row)):
				if textMatrix[row][column] != "<Blank>":
					button = Button(frame, text=textMatrix[row][column], command=functionMatrix[row][column], height=size[0], width=size[1])
				button.grid(row=row, column=column, sticky=W)

positionList = {"x":0,"y":0,"z":0,"a":0}
# [magnitude of rotation, origin, end of axis 1, end of axis 2 <end of axies relative to origin>]
#rotation = [0,[0,0,0],[1,0,0],[0,1,0]]
# sets size of screen in graph units
bounds = [[-10,10],[-15,15],[-10,10]]
# maximum number of resolution improvement itterations
maxIncrements = 6

# W.I.P
# keeping enableGhosts as False is strongly recomended
maxGhostIncrements = 1
totalGhostNumber = 3
ghostSpacing = 1
ghostAxis = "a"
enableGhosts = False

pointsPerStep = 10
# sets amount to shift bounds by in the shift function
shiftSize = 1

axies = ["x","z"]

equations = list()

refresh = False

def isBetween(check, bound1, bound2):
	if bound1 > bound2:
		biggest = bound1
		smallest = bound2
	else:
		biggest = bound2
		smallest = bound1
	if check >= smallest and check <= biggest:
		return True
	else:
		return False

def hyperTranslate(magnitude, *indexes):
	global bounds
	for index in indexes:
		bounds[index-1][0] += magnitude
		bounds[index-1][1] += magnitude

def hyperShift(magnitude, *indexes):
	global positionList
	for index in indexes:
		positionList[index-1] += shiftSize*magnitude

def hyperRotate(magnitude):
	rotation[0] += magnitude

def drawAxies():
	glBegin(GL_LINES)
	glColor3fv((1,0,0))
	glVertex3fv((0,0,0))
	glVertex3fv((2,0,0))
	glColor3fv((0,0,1))
	glVertex3fv((0,0,0))
	glVertex3fv((0,2,0))
	glColor3fv((0,1,0))
	glVertex3fv((0,0,0))
	glVertex3fv((0,0,2))
	glEnd()

def mapChar(char):
	number = ord(char)
	if number in range(120,123):
		return number - 120
	elif number in range(97,120):
		return number - 94
	elif number in range(65,91):
		return number - 39

class plot:
	def __init__(self,equationString,colour):
		self.equationString = equationString
		self.variables = list()
		for char in equationString:
			if ord(char) > 65: self.variables.append(char)
			if not char in [*positionList]:
				positionList[char] = 0
		self.lastPositions = None
		self.lastBounds = None
		self.lastAxies = None
		self.colour = colour

	def improve(self):
		grid = [*self.surface]
		incrementX = (bounds[0][1]-bounds[0][0])/(len(grid)-1)
		incrementY = (bounds[2][1]-bounds[2][0])/((len(grid)-1)*2)
		for indexO in range(len(grid)):
			for index in range((len(grid[indexO])*2)-1):
				if index % 2 == 0:
					newPoint = grid[indexO][index//2]
				else:
					newPoint = eval(f"self.equation({axies[0]}={bounds[0][0]+(incrementX*indexO)}, {axies[1]}={bounds[2][0]+(incrementY*index)})")
				try:
					if newPoint >= bounds[1][0] and newPoint <= bounds[1][1]:
						yield newPoint
					else:
						yield None
				except:
					yield None
			yield "end column"
			if indexO != len(grid) - 1:
				for index in range((len(grid[indexO])*2)-1):
					newPoint = eval(f"self.equation({axies[0]}={bounds[0][0]+(incrementX*(indexO+0.5))}, {axies[1]}={bounds[2][0]+(incrementY*index)})")
					try:
						if newPoint >= bounds[1][0] and newPoint <= bounds[1][1]:
							yield newPoint
						else:
							yield None
					except:
						yield None
				yield "end column"
		yield "end grid"

	def buildSurface(self):
		for _ in range(pointsPerStep):
			msg = next(self.improver)
			if msg == "end column":
				self.lastPoint = None
				if self.surfaceColumnNumber % 2 == 0:
					self.surface[self.surfaceColumnNumber] = self.currentLine
				else:
					self.surface.insert(self.surfaceColumnNumber, self.currentLine)
				self.currentLine = []
				self.surfaceColumnNumber += 1
				return
			elif msg == "end grid":
				self.oldSurface = [column.copy() for column in self.surface.copy()]
				self.lastPoint = None
				raise StopIteration
			self.currentLine.append(msg)

	def drawPlot(self):
		glBegin(GL_LINES)
		glColor3fv(self.colour)
		glEnd()
		incrementX = (bounds[0][1]-bounds[0][0])/(len(self.oldSurface)-1)
		for indexC in range(len(self.oldSurface)):
			self.lastPoint = None
			incrementY = (bounds[2][1]-bounds[2][0])/(len(self.oldSurface[indexC])-1)
			for index in range(len(self.oldSurface[indexC])):
				fullPoint = (bounds[0][0]+(incrementX*indexC),self.oldSurface[indexC][index],bounds[2][0]+(incrementY*index))
				glBegin(GL_LINES)
				try:
					glVertex3fv(self.lastPoint)
					glVertex3fv(fullPoint)
					if indexC != 0:
						try:
							glVertex3fv((bounds[0][0]+(incrementX*(indexC-1)),self.oldSurface[indexC-1][index],bounds[2][0]+(incrementY*index)))
							glVertex3fv(fullPoint)
						except:
							pass
					glEnd()
				except:
					glEnd()
				if self.oldSurface[indexC][index] != None:
					self.lastPoint = fullPoint
				else:
					self.lastPoint = None

	def makeGhosts(self):
		for direction in [-1,1]:
			for ghostIndex in range(1, totalGhostNumber+1):
				grid = self.ghosts[ghostIndex]
				if len(grid) != 0:
					incrementX = (bounds[0][1]-bounds[0][0])/(len(grid)-1)
					incrementY = (bounds[2][1]-bounds[2][0])/((len(grid)-1)*2)
					equation = eval("lambda "+",".join([var + f"={positionList[var]}" if var != ghostAxis else ghostAxis+f"={(ghostSpacing*ghostIndex*direction) + positionList[var]}" for var in self.variables])+":"+self.equationString)
					for indexO in range(len(grid)):
						for index in range((len(grid[indexO])*2)-1):
							if index % 2 == 0:
								newPoint = grid[indexO][index//2]
							else:
								newPoint = eval(f"equation({axies[0]}={bounds[0][0]+(incrementX*indexO)}, {axies[1]}={bounds[2][0]+(incrementY*index)})")
							try:
								if newPoint >= bounds[1][0] and newPoint <= bounds[1][1]:
									yield newPoint
								else:
									yield None
							except:
								yield None
						yield "end column"
						if indexO != len(grid) - 1:
							for index in range((len(grid[indexO])*2)-1):
								newPoint = eval(f"equation({axies[0]}={bounds[0][0]+(incrementX*(indexO+0.5))}, {axies[1]}={bounds[2][0]+(incrementY*index)})")
								try:
									if newPoint >= bounds[1][0] and newPoint <= bounds[1][1]:
										yield newPoint
									else:
										yield None
								except:
									yield None
							yield "end column"
					yield "end grid"
		else:
			incrementX = bounds[0][1]-bounds[0][0]
			incrementY = bounds[2][1]-bounds[2][0]
			for direction in [-1,1]:
				for indexC in range(2):
					for index in range(2):
						point = eval(f"self.equation({axies[0]}={bounds[indexC][index]}, {axies[1]}={bounds[2][0]}, {ghostAxis}={(ghostSpacing*ghostIndex*direction) + positionList[ghostAxis]})")
						try:
							if point > bounds[1][0] and point < bounds[1][1]:
								yield point
							else:
								yield None
						except:
							yield None
					yield "end column"
				yield "end grid"
		yield "end ghost"

	def buildGhost(self):
		for _ in range(pointsPerStep):
			msg = next(self.ghostImprover)
			if msg == "end column":
				self.lastPoint = None
				if self.ghostColumnNumber % 2 == 0:
					try:
						self.ghosts[self.ghostNumber][self.ghostColumnNumber] = self.currentGhostLine
					except:
						self.ghosts[self.ghostNumber].append(self.currentGhostLine)
				else:
					self.ghosts[self.ghostNumber].insert(self.ghostColumnNumber, self.currentGhostLine)
				self.currentGhostLine = []
				self.ghostColumnNumber += 1
				return
			elif msg == "end grid":
				self.oldGhosts[self.ghostNumber] = [column.copy() for column in self.ghosts[self.ghostNumber].copy()]
				self.lastPoint = None
				self.ghostNumber += 1
				raise StopIteration
			elif msg == "end ghosts":
				self.ghostNumber = 0
				raise StopIteration
			self.currentGhostLine.append(msg)
	
	def ghost(self):
		glBegin(GL_LINES)
		glColor3fv(self.colour)
		glEnd()
		incrementX = (bounds[0][1]-bounds[0][0])/(len(self.oldSurface)-1)
		for indexC in range(len(self.oldSurface)):
			self.lastPoint = None
			incrementY = (bounds[2][1]-bounds[2][0])/(len(self.oldSurface[indexC])-1)
			for index in range(len(self.oldSurface[indexC])):
				fullPoint = (bounds[0][0]+(incrementX*indexC),self.oldSurface[indexC][index],bounds[2][0]+(incrementY*index))
				glBegin(GL_LINES)
				try:
					glVertex3fv(self.lastPoint)
					glVertex3fv(fullPoint)
					if indexC != 0:
						try:
							glVertex3fv((bounds[0][0]+(incrementX*(indexC-1)),self.oldSurface[indexC-1][index],bounds[2][0]+(incrementY*index)))
							glVertex3fv(fullPoint)
						except:
							pass
					glEnd()
				except:
					glEnd()
				if self.oldSurface[indexC][index] != None:
					self.lastPoint = fullPoint
				else:
					self.lastPoint = None

	def __call__(self):
		global refresh
		if bounds != self.lastBounds or axies != self.lastAxies or positionList != self.lastPositions:
			self.increments = 0
			self.ghostIncrements = 0
			self.equation = eval("lambda "+",".join([var + f"={positionList[var]}" for var in self.variables])+":"+self.equationString)
			point1 = eval(f"self.equation({axies[0]}={bounds[0][0]},{axies[1]}={bounds[2][0]})")
			point2 = eval(f"self.equation({axies[0]}={bounds[0][0]},{axies[1]}={bounds[2][1]})")
			point3 = eval(f"self.equation({axies[0]}={bounds[0][1]},{axies[1]}={bounds[2][0]})")
			point4 = eval(f"self.equation({axies[0]}={bounds[0][1]},{axies[1]}={bounds[2][1]})")
			self.surface = [[point1, point2], [point3, point4]]
			self.oldSurface = [column.copy() for column in self.surface.copy()]
			self.lastPositions = positionList.copy()
			self.lastBounds = [bound.copy() for bound in bounds.copy()]
			self.lastAxies = axies.copy()
			self.lastPoint = None
			self.currentLine=[]
			self.surfaceColumnNumber = 0
			self.ghosts = [[]]*totalGhostNumber*2
			self.oldGhosts = [[]]*totalGhostNumber*2
			self.lastGhostPoint = None
			self.currentGhostLine=[]
			self.ghostColumnNumber = 0
			self.ghostNumber = 0
			self.improver = self.improve()
			self.ghostImprover = self.makeGhosts()
			self.increments += 1
		if self.increments <= maxIncrements:
			try:
				self.buildSurface()
			except StopIteration:
				self.lastPoint = None
				self.currentLine=[]
				self.surfaceColumnNumber = 0
				self.improver = self.improve()
				self.increments += 1
				refresh = True
		if self.ghostIncrements <= maxGhostIncrements and enableGhosts and not ghostAxis in axies:
			try:
				self.buildGhost()
			except StopIteration:
				self.lastGostPoint = None
				self.currentGhostLine=[]
				self.ghostColumnNumber = 0
				self.ghostImprover = self.makeGhosts()
				self.ghostIncrements += 1
				refresh = True

def addEquation(string, directCall=True):
	if directCall:
		equations.append(list())
	splitString = string.split("#")
	if len(splitString) > 1:
		addEquation("#".join(splitString[:-1])+"+"+splitString[-1], False)
		addEquation("#".join(splitString[:-1])+"-"+splitString[-1], False)
	else:
		equations[-1].append(plot(string, (len(equations),0.5,0.5)))

addEquation("x**2+sin(z)")

pygame.init()
display = (1000,1000)
pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
gluPerspective(40,display[0]/display[1], 0.1, 200)
glTranslatef(0,0,-30)
glRotatef(15,1,0,0)
glRotatef(30,0,1,0)
glLineWidth(1)



# Main loop
glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
for equationGroup in equations:
	for equation in equationGroup:
		equation()
		equation.drawPlot()
drawAxies()
pygame.display.flip()
pygame.time.wait(50)

while True:
	refresh = False
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			quit()
		# Controls are tempory and will be improved
		if event.type == pygame.KEYDOWN:
			refresh = True
			if event.key == K_LEFT:
				glRotatef(5,0,1,0)
			elif event.key == K_RIGHT:
				glRotatef(-5,0,1,0)
			elif event.key == K_UP:
				glRotatef(5,0,0,1)
			elif event.key == K_DOWN:
				glRotatef(-5,0,0,1)
			elif event.key == K_w:
				hyperTranslate(1,2)
			elif event.key == K_s:
				hyperTranslate(-1,2)
			elif event.key == K_a:
				hyperTranslate(1,1)
			elif event.key == K_d:
				hyperTranslate(-1,1)
			elif event.key == K_q:
				hyperTranslate(1,3)
			elif event.key == K_e:
				hyperTranslate(-1,3)
			elif event.key == K_j:
				hyperShift(1,4)
			elif event.key == K_l:
				hyperShift(-1,4)
			elif event.key == K_n:
				axies = ["x","z"]
			elif event.key == K_m:
				axies = ["x","a"]
			elif event.key == K_x:
				gOpen()
				gPrint("== SETTINGS ==")
				gPrint("GUI coming soon ish")
				gContinue()
				gClose()
	for equationGroup in equations:
		for equation in equationGroup:
			equation()
	if refresh:
		glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
		for equationGroup in equations:
			for equation in equationGroup:
				equation.drawPlot()
				# if enableGhosts and not ghostAxis in axies:
				# 	equation.ghost()
		drawAxies()
		pygame.display.flip()
		pygame.time.wait(50)
