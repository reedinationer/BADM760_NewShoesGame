import pandas as pd
from scipy.optimize import curve_fit
import numpy as np


df = pd.read_excel("/Users/reed/PycharmProjects/760_Marketing/MyResults.xlsx", index_col=0, header=[0, 1])


def region_sales(func_inputs, a, c, d, p):
	advertising, cons_pro, sales, deal_pro, price = func_inputs
	return a*advertising + c*cons_pro + sales + d*deal_pro + p**2*price

def get_region_df(region_text):
	applicable_columns = [col for col in df.columns if region_text in col]
	return df[applicable_columns].droplevel(0, axis=1)

home_df = get_region_df("Home")

print(curve_fit(region_sales, (home_df["Advertising"], home_df["Consumer Promotions"], home_df["Sales People"], home_df["Dealer Promotions"], home_df["Price"]), home_df["Units Sold"], (1, 1, 1, 1)))

# some artificially noisy data to fit
x = np.linspace(0.1,1.1,101)
y = np.linspace(1.,2., 101)
a, b, c = 10., 4., 6.

# initial guesses for a,b,c:
p0 = 8., 2., 7.


