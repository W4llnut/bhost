class AI:
	def __init__(self):
		pass

	def curvature(self, df, t, who):
		derivative2 = (df[who][t]-df[who][t-1])/1
		derivative1 = (df[who][t-1]-df[who][t-2])/1
		return (derivative2-derivative1)/1

	def longCurvature(self, df, t, who, span):
		derivative2 = (df[who][t]-df[who][t-int(span/2)])/int(span/2)
		derivative1 = (df[who][t-int(span/2)]-df[who][t-span])/int(span/2)
		return (derivative2-derivative1)/2

	def inclination(self, df, t, who):
		return (df[who][t]-df[who][t-5])/5

	def longInclination(self, df, t, who):
		return (df[who][t]-df[who][t-100])/100

	def eval(self, df, t):
		# enter conditions
		increasing = df['macd_diff'][t]>df['macd_diff'][t-2]>df['macd_diff'][t-4]>df['macd_diff'][t-6] and 4>df['macd_diff'][t]>=0.2
		above100 = df['Close'][t]>df['EMA100'][t]+10
		curves = self.longCurvature(df,t,'EMA100',75)>-0.2 and self.inclination(df,t,'EMA100')>0.1 and (self.curvature(df,t,'macd_diff')>0 and self.inclination(df,t,'macd_diff')>0.1)
		passed = df['roc5'][t]<1
		# stop stopcall
		stopLoss = ((df['Close'][t]-df['EMA100'][t])/df['Close'][t])
		is_okay = increasing and above100 and curves and passed
		if is_okay: print(f"{t}: {self.longCurvature(df,t,'EMA100',75)}")
		return is_okay,[stopLoss*2,stopLoss]

	def stopCall(self, df, t, entrata):
		out_but_okay = self.inclination(df,t,'macd_diff')<-1 and df['Close'][t]>entrata #  df['rsi'][t]>70 and self.inclination(df,t,'macd_diff')<-0.1
		crashing = df['roc5'][t]<df['roc5'][t-2]-1
		#peaked = self.curvature(df,t,'macd_diff')<-1
		return crashing

