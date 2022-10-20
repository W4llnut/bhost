from numpy import linspace, meshgrid, array, arctan
from ta.trend import *
from ta.momentum import *
from ta.volatility import *
from ai import AI
import pandas as pd

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

		if self.ai.eval([self.df['bollinger_wband'].iloc[t],self.df['rocM'].iloc[t],self.df['rocBreve'].iloc[t],self.df['adx'].iloc[t],self.df['aroon_indicator'].iloc[t],self.df['rsi'].iloc[t],self.df['rocLungo'].iloc[t],self.df['macd_diff'].iloc[t],self.df['awesome_osc'].iloc[t],self.df['stoch_rsi'].iloc[t],self.df['bollinger_pband'].iloc[t],self.df['roc5'].iloc[t]]):
			self.strategia = "MACD"
		elif Smacd and SrocMACD and False:
			if SsarM:
				self.short = True
				self.strategia = "MACDshort"
		return self.strategia != "-"

	def check_sell(self, t, entrata):
		if self.strategia == "MACD":
			if self.df[f'EMA{self.Breve}'].iloc[t]<self.df[f'EMA{self.Lunga}'].iloc[t] or self.stopCallMacd(t,entrata):
				self.strategia = "-"
		elif self.strategia == "MACDshort":
			if self.df[f'EMA{self.Breve}'].iloc[t]>self.df[f'EMA{self.Lunga}'].iloc[t] or self.stopCallMacdshort(t,entrata):
				self.strategia = "-"
		return self.strategia == "-"

	def stopCallMacd(self, t, entrata):
		sar = self.moltiplicatore*(self.df['Close'].iloc[t]*(1-self.tassa)-entrata)/entrata>=0 and self.df['psar_di'].iloc[t]==True
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
		self.df[f'EMA{self.periodiB}'] = ema_indicator(self.df['Close'], self.periodiB, False)
		self.df[f'EMA{self.periodiL}'] = ema_indicator(self.df['Close'], self.periodiL, False)
		
		macd = MACD(self.df['Close'])
		self.df['macd_diff'] = macd.macd_diff()

		# Parabolic SAR
		parabolicSar = PSARIndicator(self.df['High'],self.df['Low'],self.df['Close'])
		self.df['psar'] = parabolicSar.psar()
		self.df['psar_di'] = self.df['psar']>self.df['Close']

		# Aroon
		aroon = AroonIndicator(self.df['Close'])
		self.df['aroon_indicator'] = aroon.aroon_indicator()
		
		
		# Bollinger Bands
		bollinger = BollingerBands(self.df['Close'],200)
		self.df['bollinger_wband'] = bollinger.bollinger_wband()
		self.df['bollinger_pband'] = bollinger.bollinger_pband()

		# ADX
		adxI = ADXIndicator(self.df['High'],self.df['Low'],self.df['Close'], self.ADXperiodo, False)
		self.df['pos_directional_indicator'] = adxI.adx_pos()
		self.df['neg_directional_indicator'] = adxI.adx_neg()
		self.df['adx'] = adxI.adx()

		# roc
		rocM = ROCIndicator(self.df['Close'])
		self.df['rocM'] = rocM.roc()
		rocBreve = ROCIndicator(self.df['Close'],3)
		self.df['rocBreve'] = rocBreve.roc()
		rocBreve = ROCIndicator(self.df['Close'],5)
		self.df['roc5'] = rocBreve.roc()
		rocLungo = ROCIndicator(self.df['Close'],95)
		self.df['rocLungo'] = rocLungo.roc()

		
		# RSI
		rsiI = RSIIndicator(self.df['Close'])
		self.df['rsi'] = rsiI.rsi()
		
		##
		a_osc = AwesomeOscillatorIndicator(self.df['High'],self.df['Low'])
		stoch_rsi = StochRSIIndicator(self.df['Close'])
		self.df['awesome_osc'] = a_osc.awesome_oscillator()
		self.df['stoch_rsi'] = stoch_rsi.stochrsi()
