from cryptography.fernet import Fernet

class AI:
	def __init__(self):
		f = open("model.md","rb")
		key = os.environ['FERNET']
		fernet = Fernet(key)
		lines = fernet.decrypt(f.read()).decode("utf-8").split("\r\n")
		self.bubbles = [[],[],[],[]]
		line = 0
		for j in range(4):
			for i in range(int(lines[line])):
				self.bubbles[j].append([float(i) for i in lines[line+1+i].split(" ")])
			line += int(lines[line])+1

	def eval(self, state):
		for i in range(4):
			flag = 0
			for j in range(len(self.bubbles[i])):
				if abs(state[i]-self.bubbles[i][j][0])<=self.bubbles[i][j][1]:
					flag = 1
			if flag == 0:
				return False
		return True


A = AI()

print(A.eval([1550.272,1551.935,1550.272,1551.59,1551.59,0.0,1549.046,1545.988,5.619,0.764,0.166,1541.726,0,24.446,36.0,62.315]))