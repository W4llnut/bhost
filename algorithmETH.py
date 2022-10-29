from numpy import linspace, meshgrid, array, arctan
from ta.trend import *
from ta.momentum import *
from ta.volatility import *
from cryptography.fernet import Fernet
import pandas as pd
import os

f = open("ai.md","rb")
w = open("ai.py","wb")
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
		Smacd = self.df[f'EMA{self.Breve}'].iloc[t]<self.df[f'EMA{self.Lunga}'].iloc[t]
		SrocMACD =  self.df['rocM'].iloc[t]<0.2
		SsarM = self.df['psar_di'].iloc[t]==True
		state,calls = self.ai.eval(self.df,t)
		if state:
			self.stopWinMACD = calls[0]
			self.stopLossMACD = calls[1]
			self.strategia = "MACD"
		elif Smacd and SrocMACD and False:
			if SsarM:
				self.short = True
				self.strategia = "MACDshort"
		return self.strategia != "-"

	def check_sell(self, t, entrata):
		if self.strategia == "MACD":
			if self.ai.stopCall(self.df,t,entrata*(1+self.tassa)) or self.stopCallMacd(t,entrata):
				self.strategia = "-"
		elif self.strategia == "MACDshort":
			if self.df[f'EMA{self.Breve}'].iloc[t]>self.df[f'EMA{self.Lunga}'].iloc[t] or self.stopCallMacdshort(t,entrata):
				self.strategia = "-"
		return self.strategia == "-"

	def stopCallMacd(self, t, entrata):
		#sar = self.moltiplicatore*(self.df['Close'].iloc[t]*(1-self.tassa)-entrata)/entrata>=0 and self.df['psar_di'].iloc[t]==True
		upper = self.df['Close'].iloc[t]>entrata*(1+self.stopWinMACD)
		lower = self.df['Close'].iloc[t]<entrata*(1-self.stopLossMACD)
		return upper or lower or sar

	def stopCallMacdshort(self, t, entrata):
		sar = self.moltiplicatore*(self.df['Close'].iloc[t]*(1+self.tassa/2)-entrata*(1-self.tassa/2))/entrata<=0 and self.df['psar_di'].iloc[t]==False
		lower = self.df['Close'].iloc[t]<entrata*(1-self.stopWinMACDs)
		upper = self.df['Close'].iloc[t]>entrata*(1+self.stopLossMACDs)
		return upper or lower or sar

	def analyzeDf(self):
		# EMA
		self.df[f'EMA{100}'] = ema_indicator(self.df['Close'],100,False)
		macd = MACD(self.df['Close'])
		self.df['macd_diff'] = macd.macd_diff()

		# roc
		rocBreve = ROCIndicator(self.df['Close'],5)
		self.df['roc5'] = rocBreve.roc()