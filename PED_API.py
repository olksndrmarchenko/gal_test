from sklearn.linear_model import LinearRegression
import pandas as pd
import numpy as np

class PED(object):
	"""Price elasticity of demand estimation operations"""
	def __init__(self, sample):
		self.sample = sample
		
	def _perform_data_split(self):
		self.sample.WEEK_END_DATE = pd.to_datetime(self.sample.WEEK_END_DATE)
		last_two_weeks = self.sample.WEEK_END_DATE.unique()[-2:]
		
		self.test_data = self.sample[(self.sample['WEEK_END_DATE'] == last_two_weeks[0])|(self.sample['WEEK_END_DATE'] == last_two_weeks[1])]
		self.train_data = self.sample.drop(index=self.test_data.index)

	def perform_fit(self):
		self._perform_data_split()
		lr = LinearRegression()
		lr.fit(X = self.train_data[['PRICE']], y = self.train_data['UNITS'])

		self.x = np.arange(self.train_data.PRICE.min(), self.train_data.PRICE.max()+1, 0.01)
		self.y = []

		for i in range(self.x.shape[0]):
   			self.y.append((self.x[i])*(lr.intercept_+lr.coef_[0]*self.x[i]))
		self.intercept, self.coef = lr.intercept_, lr.coef_[0]

	def get_estimates(self):
		self.current_price, self.current_estimated_revenue = self.train_data.PRICE.iloc[-1],\
			 (self.train_data.PRICE.iloc[-1])*(self.intercept+self.coef*self.train_data.PRICE.iloc[-1])

		self.recommended_price, self.estimated_revenue = self.x[np.array(self.y).argmax(axis=0)], np.array(self.y).max()

		self.test_data_price, self.test_data_revenue = self.test_data.PRICE, self.test_data.SPEND	

	def print_results(self):
		print('last observed price is {:.2f}\ncurrent estimated revenue is {:.2f}\nrecommended price is {:.2f}\
			\nestimated revenue is {:.2f}\nthe next two weeks prices are: {}, {}\
			\napplying recommended prices increases mean revenue by {:.2%}'\
				.format(self.current_price,
				self.current_estimated_revenue,
				self.recommended_price,
				self.estimated_revenue,
				self.test_data_price.values[0], self.test_data_price.values[1],
				((self.estimated_revenue - self.test_data_revenue) / self.test_data_revenue).mean())
		     )

	def get_results(self):	
		# create a json structure {'store_num':num,UPC's:['UPC0':{price, rev, ...}, 'UPC1':{price, rev, ...}]}
		return {'STORE_NUM':self.sample.STORE_NUM.unique().tolist(),
				'UPC':self.sample.UPC.unique().tolist(),
				'current_price': self.current_price,
				'current_est_revenue': self.current_estimated_revenue,
				'recommended_price': self.recommended_price,
				'estimated_revenue': self.estimated_revenue,
				'week_1_price': self.test_data_price.values[0],'week_2_price': self.test_data_price.values[1],
				'mean_revenue_increase':((self.estimated_revenue - self.test_data_revenue) / self.test_data_revenue).mean()}
