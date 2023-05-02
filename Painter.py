#Painter.py
# 200 pulses move the motor 360 degrees
# Gear on motor is 16 mm in diameter 

import random;
import gpiod;
import time;


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
		print(revolutions);
		pulseCount = int(revolutions * 200);
		print(pulseCount);
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
		self.XMotor.Move(100);
		self.XMotor.SetBackward();
		self.XMotor.Move(100);
		
	def PaintLineY(self):
		print("paint line Y");
		self.YMotor.SetForward();
		self.YMotor.Move(100);
		self.YMotor.SetBackward();
		self.YMotor.Move(100);
		
	def PaintDiagonal(self):
		print("paint circle");
		self.XMotor.SetForward();
		self.YMotor.SetForward();
		for i in range(0, 20):
			self.XMotor.Move(10);
			self.YMotor.Move(10);
		
	def Main(self):
		done = False;
		iterations = 0;
		
		while(done == False):
			self.PaintLineX();
			#self.PaintLineY();
			iterations += 1;
			
			if (iterations > 0):
				done = True;
		
		# Need to release lines at end
		self.ReleaseAll();



p = Painter();
p.Main();
