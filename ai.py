from cryptography.fernet import Fernet
import os

class AI:
	def __init__(self):
		f = open("model.md","rb")
		key = os.environ['FERNET']
		fernet = Fernet(key)
		lines = fernet.decrypt(f.read()).decode("utf-8").split("\r\n")
		self.bubbles = [[],[],[],[],[],[],[],[],[]]
		line = 0
		for j in range(9):
			for i in range(int(lines[line])):
				self.bubbles[j].append([float(i) for i in lines[line+1+i].split(" ")])
			line += int(lines[line])+1

	def eval(self, state):
		for i in range(9):
			flag = 0
			for j in range(len(self.bubbles[i])):
				if abs(state[i]-self.bubbles[i][j][0])<=self.bubbles[i][j][1]:
					flag = 1
			if flag == 0:
				return False
		return True
