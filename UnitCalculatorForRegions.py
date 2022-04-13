import numpy as np
import xlwings

"""Assuming enough market research is obtained we will solve systems of equations to back calculate the units sold in each region
overall satisfaction = Home_units * Home_satisfaction + Dom_units * Dom_satisfaction + For_units * For_satisfaction
units = Home_units + Dom_units + For_units
Profit / ROS = Home_units * Home_price + Dom_units * Dom_price + For_units * For_price

Revenue = Price * Units
ROS = Profit / Revenue
-> Revenue = Profit / ROS


substituting x for Home_units, y for Dom_units, and z for For_units"""

wb = xlwings.Book("New Shoes.xlsx")
for sheet in wb.sheets:
	if "_" in sheet.name:
		run_rows = [3, 4, 5, 6, 7, 8, 9, 10]
	else:
		run_rows = [3, 4, 5, 6, 7, 8, 9]
	print("Running on sheet {}".format(sheet.name))
	sht = wb.sheets[sheet]
	for row in run_rows:
		"""Equation 1: Profit + Dev = Hrev-ads + Drev-ads + Frev-ads (this is only needed when foreign data is present"""
		profit = sht.range("E{}".format(row)).value
		dev = sht.range("B{}".format(row)).value
		"""Equation 2: Satisfaction equals unit weighted satisfaction by region"""
		overall_satisfaction = sht.range("I{}".format(row)).value
		home_satisfaction = sht.range("P{}".format(row)).value
		domestic_satisfaction = sht.range("W{}".format(row)).value
		foreign_satisfaction = sht.range("AD{}".format(row)).value
		"""Equation 2: Sum of units equals total units"""
		total_units = sht.range("D{}".format(row)).value
		"""Equation 3: Return on sales equals profit / revenue"""
		return_on_sales = sht.range("H{}".format(row)).value
		home_price = sht.range("K{}".format(row)).value
		domestic_price = sht.range("R{}".format(row)).value
		foreign_price = sht.range("Y{}".format(row)).value
		try:
			if not foreign_price:
				A = np.array([
					[1.0, 1.0],
					[home_price, domestic_price]])
				b = np.array([
						total_units,
						profit / (return_on_sales / 100.)
					])
			else:
				h_ad_cost = sht.range("L{}".format(row)).value + sht.range(
					"M{}".format(row)).value + 80000.0 * sht.range("N{}".format(row)).value + sht.range(
					"O{}".format(row)).value
				d_ad_cost = sht.range("S{}".format(row)).value + sht.range(
					"T{}".format(row)).value + 80000.0 * sht.range("U{}".format(row)).value + sht.range(
					"V{}".format(row)).value
				f_ad_cost = sht.range("Z{}".format(row)).value + sht.range(
					"AA{}".format(row)).value + 80000.0 * sht.range("AB{}".format(row)).value + sht.range(
					"AC{}".format(row)).value
				A = np.array([
					[home_price, domestic_price, foreign_price],
					[1.0, 1.0, 1.0],
					[home_satisfaction, domestic_satisfaction, foreign_satisfaction]])
				b = np.array([profit + dev + h_ad_cost + d_ad_cost + f_ad_cost, total_units, overall_satisfaction])
		except TypeError:
			print("Error on row {}".format(row))
			sht.range("J{}".format(row)).value = None
			sht.range("Q{}".format(row)).value = None
			sht.range("X{}".format(row)).value = None
			continue
		# print(A)
		# print(b)
		try:
			x = np.linalg.solve(A, b)
		except np.linalg.LinAlgError as bad_case:
			print("Error on row {}: {}".format(row, bad_case))
			sht.range("J{}".format(row)).value = None
			sht.range("Q{}".format(row)).value = None
			sht.range("X{}".format(row)).value = None
			continue
		sht.range("J{}".format(row)).value = x[0]
		sht.range("Q{}".format(row)).value = x[1]
		if foreign_price:
			sht.range("X{}".format(row)).value = x[2]
		# print("Sheet {}, row {}: {}".format(sheet, row, x))
		# print("Prices: {}, {}, {}".format(home_price, domestic_price, foreign_price))
		# print("satisfactions: {}, {}, {}".format(home_satisfaction, domestic_satisfaction, foreign_satisfaction))
		# print("total units: {:,}, overall_satisfaction: {}, profit: {}, ROS: {}".format(total_units, overall_satisfaction, profit, return_on_sales))






