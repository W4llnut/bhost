from numpy import linspace, meshgrid, array, arctan
from ta.trend import *
from ta.momentum import *
from ta.volatility import *
from cryptography.fernet import Fernet
import pandas as pd
import os

f = open("ai.md","rb")
w = open("ai.py","w")
key = os.environ['FERNET']
fernet = Fernet(key)
text = fernet.decrypt(f.read()).decode("utf-8")
w.write(text)
w.close()
f.close()

from ai import AI

class AlgorithmETH:
	def __init__(self, tassa, moltiplicatore):
		self.df = -1
		self.ai = AI()

		# parametri
		self.tassa = tassa
		self.moltiplicatore = moltiplicatore

		# stop calls
		self.stopWinMACD = self.tassa+0.4/self.moltiplicatore #
		self.stopLossMACD = (0.04)/self.moltiplicatore #
		self.stopWinMACDs = self.tassa+0.007/self.moltiplicatore
		self.stopLossMACDs = (0.000)/self.moltiplicatore
		self.stopWinBollinger = self.tassa+0.4/self.moltiplicatore
		self.stopLossBollinger = (0.01)/self.moltiplicatore

		# parametri periodi
		self.ADXperiodo = 14
		self.periodiB = 6
		self.periodiL = 66
		self.Periodo = 25
		self.longPeriod = 3*self.Periodo

		self.Breve = self.periodiB
		self.Lunga = self.periodiL

		self.strategia = "-"


	# ========================= funzioni dell'algoritmo ========================= #
	def check_buy(self, t):
		self.strategia,calls = self.ai.eval(self.df,t)
		if self.strategia != "-":
			self.stopWinMACD = calls1[0]
			self.stopLossMACD = calls1[1]
		return self.strategia != "-"

	def check_sell(self, t, entrata):
		if self.strategia == "MACD":
			#if self.df[f'EMA{self.Breve}'][t]<self.df[f'EMA{self.Lunga}'][t] or self.stopCallMacd(t,entrata):
			if self.stopCallMacd(t,entrata):
				self.strategia = "-"
		elif self.strategia == "bollinger":
			if self.stopCallMacd(t,entrata):
				self.strategia = "-"
		elif self.strategia == "random":
			self.strategia = "-"
		return self.strategia == "-"

	def stopCallMacd(self, t, entrata):
		#sar = self.moltiplicatore*(self.df['Close'][t]*(1-self.tassa)-entrata)/entrata>=0 and self.df['psar_di'][t]==True
		upper = self.df['Close'][t]>entrata*(1+self.stopWinMACD)#*(1+self.df['atr_pself.moltiplicatore*(self.df['Close'][t]*(1-self.tassa)-entrata)/entrata>=0 and erc'][t]))
		lower = self.df['Close'][t]<entrata*(1-self.stopLossMACD)#*(1+self.df['atr_perc'][t]))
		return upper or lower# or sar

	def stopCallBollinger(self, t, entrata):
		#sar = self.moltiplicatore*(self.df['Close'][t]*(1+self.tassa/2)-entrata*(1-self.tassa/2))/entrata<=0 and self.df['psar_di'][t]==False
		upper = self.df['Close'][t]>entrata*(1+self.stopWinMACD)#*(1+self.df['atr_pself.moltiplicatore*(self.df['Close'][t]*(1-self.tassa)-entrata)/entrata>=0 and erc'][t]))
		lower = self.df['Close'][t]<entrata*(1-self.stopLossMACD)#*(1+self.df['atr_perc'][t]))
		return upper or lower# or sar

	def analyzeDf(self):
		# EMA
		self.df[f'EMA{100}'] = ema_indicator(self.df['Close'],100,False)
		rocEMA100 = ROCIndicator(self.df['EMA100'])
		self.df['rocEMA100'] = rocEMA100.roc()
		
		self.df['distance'] = (self.df['Close']-self.df['EMA100'])/self.df['EMA100']
		macd = MACD(self.df['Close'])
		self.df['macd_diff'] = macd.macd_diff()

		# roc
		rocBreve = ROCIndicator(self.df['Close'])
		self.df['rocM'] = rocBreve.roc()
		rocBreve = ROCIndicator(self.df['Close'],5)
		self.df['roc5'] = rocBreve.roc()

		# Bollinger Bands
		bollinger = BollingerBands(self.df['Close'],100)
		self.df['bollinger_wband'] = bollinger.bollinger_wband()
		self.df['bollinger_pband'] = bollinger.bollinger_pband()