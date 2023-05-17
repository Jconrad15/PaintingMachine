#Painter.py
# 200 pulses move the motor 360 degrees
# Gear on motor is 16 mm in diameter 

import random;
import gpiod;
import time;
import math;


PI = 3.14159;
circumference = PI * 16.0;

class Motor(object):
	def __init__(self, chip, stepLineNumber, dirLineNumber):
		# Initialize motor lines and set lines to low
		self.stepLineNumber = stepLineNumber;
		self.dirLineNumber = dirLineNumber;
		
		self.stepLine = chip.get_line(self.stepLineNumber);
		self.stepLine.request(consumer='me', type = gpiod.LINE_REQ_DIR_OUT, default_vals=[0]);
		self.stepLine.set_value(1);
		
		self.dirLine = chip.get_line(self.dirLineNumber);
		self.dirLine.request(consumer='me', type = gpiod.LINE_REQ_DIR_OUT, default_vals=[0]);
		self.dirLine.set_value(0);
		
	def Release(self):
		self.stepLine.release();
		self.dirLine.release();
		
	def SetForward(self):
		# Forward is clockwise
		self.dirLine.set_value(1);
		
	def SetBackward(self):
		# Backwards is counterclockwise
		self.dirLine.set_value(0);
		
	# Need to determine how far the motors move given a pulseCount
	def Move(self, distanceMM):
		revolutions = distanceMM / circumference
		# print(revolutions);
		pulseCount = int(revolutions * 200);
		# print(pulseCount);
		for i in range(0, pulseCount):
			self.stepLine.set_value(1);
			time.sleep(0.002);
			self.stepLine.set_value(0);
			time.sleep(0.002);
			
			
class Painter(object):
	def __init__(self):
		# Get the chip that that GPIO pins are on
		self.chip = gpiod.Chip("gpiochip1");
		
		# x motor lines
		# pin 8		line 91
		# pin 10	line 92
		self.XMotor = Motor(self.chip, 91, 92);
		
		# y motor lines
		# pin 35	line 86
		# pin 37	line 84
		self.YMotor = Motor(self.chip, 86, 84);

		# z motor lines
		# pin 38	line 82
		# pin 40	line 83
		self.ZMotor = Motor(self.chip, 82, 83);
		
		# position data????
		self.x = 0;
		self.y = 0;
		self.z = 0;

	def ReleaseAll(self):
		self.XMotor.Release();
		self.YMotor.Release();
		self.ZMotor.Release();
	
	# use locations 1, 2, 3 for different paint pots
	# todo: determine locations
	# Move towards function
	def DipPaint(self, location):
		if (location == 1):
			print(location);
		elif (location == 2):
			print(location);
		else:
			print(location);
	
	def PaintLineX(self):
		print("paint line X");
		self.XMotor.SetForward();
		self.XMotor.Move(25);
		self.XMotor.SetBackward();
		self.XMotor.Move(25);
		
	def PaintLineY(self):
		print("paint line Y");
		self.YMotor.SetForward();
		self.YMotor.Move(25);
		self.YMotor.SetBackward();
		self.YMotor.Move(25);
		
	def PaintDiagonal(self):
		print("paint diagonal");
		self.XMotor.SetForward();
		self.YMotor.SetForward();
		for i in range(0, 20):
			self.XMotor.Move(10);
			self.YMotor.Move(10);
			
	def PaintCircle(self):
		print("paint circle");
		r = 1;
		self.XMotor.SetForward();
		self.YMotor.SetForward();
		for i in range(0, 180):
			xmovement = r * math.cos(math.radians(i));
			ymovement = r * math.sin(math.radians(i));
			print(str(xmovement) + " " + str(ymovement));
			if (xmovement < 0):
				self.XMotor.SetBackward();
			else:
				self.XMotor.SetForward();
			
			if (ymovement < 0):
				self.YMotor.SetBackward();
			else:
				self.YMotor.SetForward();
			
			self.XMotor.Move(xmovement);
			self.YMotor.Move(ymovement);
	
	def PaintLeft(self):
		print("paint left");
		self.YMotor.SetBackward();
		self.YMotor.Move(25);
	
	def PaintRight(self):
		print("paint right");
		self.YMotor.SetForward();
		self.YMotor.Move(25);
	
	def PaintUp(self):
		print("paint up");
		self.XMotor.SetBackward();
		self.XMotor.Move(25);
	
	def PaintDown(self):
		print("paint down");
		self.XMotor.SetForward();
		self.XMotor.Move(25);
	
	def PaintJitter(self):
		print("paint jitter");
		
		for i in range(5, 10):
			r = random.randrange(0,4,1);
			if (r == 0):
				self.XMotor.SetForward();
				self.XMotor.Move(2);
			elif (r == 1):
				self.YMotor.SetForward();
				self.YMotor.Move(2);
			elif (r == 2):
				self.XMotor.SetBackward();
				self.XMotor.Move(2);
			else:
				self.YMotor.SetForward();
				self.YMotor.Move(2);
	
	def Main(self):
		
		isPainting = True;
		while (isPainting):
			# Get commands section
			commands = [];
			creatingCommands = True;
			while (creatingCommands):
				text = input("Enter Command: \n");

				if (text == "help"):
					print("'line' - paint a line");
					print("'circle' - paint a circle");
					print("'left' - paint towards the left");
					print("'right' - paint towards the right");
					print("'up' - paint upwards");
					print("'down' - paint downwards");
					print("'jitter' - randomized brush movement");
					print("'done' - finish adding commands");
					print("'exit' - delete commands and quit");

				elif (text == "line"):
					commands.append("line");
					print("Line added  \n");

				elif (text == "circle"):
					commands.append("circle");
					print("Circle added  \n");

				elif (text == "done"):
					creatingCommands = False;

				elif (text == "exit"):
					commands.clear();
					creatingCommands = False;
					isPainting = False;
					
				elif (text == "right"):
					commands.append("right");
					print("Right added \n");
					
				elif (text == "left"):
					commands.append("left");
					print("Left added \n");
					
				elif (text == "up"):
					commands.append("up");
					print("Up added \n");
					
				elif (text == "down"):
					commands.append("down");
					print("Down added \n");

				elif (text == "jitter"):
					commands.append("jitter");
					print("Jitter added \n");
					
				elif (text == "pause"):
					commands.append("pause");
					print("Pause added \n");
					
				else:
					print("Command not recognized, type 'help' for help \n");
				
			# Painting section
			print("Starting to paint: \n");
			print(commands);

			for command in commands:

				if (command == "line"):
					r = random.randrange(0,2,1);
					if (r > 0.5):
						self.PaintLineX();
					else:
						self.PaintLineY();

				elif (command == "circle"):
					self.PaintCircle();

				elif (command == "left"):
					self.PaintLeft();
					
				elif (command == "right"):
					self.PaintRight();
					
				elif (command == "up"):
					self.PaintUp();
					
				elif (command == "down"):
					self.PaintDown();
				
				elif (command == "jitter"):
					self.PaintJitter();
					
				elif (command == "pause"):
					print("Pause for 1 second");
					time.sleep(1);

				else:
					print("Error in the command, skipping");
			
			# Check if done painting
			doneCheck = input("\n Done? y/n \n");
			if (doneCheck == "n"):
				print("\n --- Continue --- \n");
			else:
				isPainting = False;
			
				
		# Need to release lines at end
		self.ReleaseAll();


p = Painter();
p.Main();
