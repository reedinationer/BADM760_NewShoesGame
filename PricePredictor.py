import matplotlib.pyplot as plt
import pandas as pd
from PlotSettings import *
import tkinter as tk
from tkinter import ttk
from threading import Thread


class Calculator:
	def __init__(self, df):
		self.df = df
		self.sheets = sorted(self.df.keys())

	def get_index(self, multi_level_index, df_key=None):  # Used for getting an index like ["Home", "Price"] within a sheet
		if df_key:
			some_df = self.df[df_key]
		else:
			some_df = self.df.copy()
		for index_key in multi_level_index:
			some_df = some_df.get(index_key)
		return some_df

	def plot_by_company_over_time(self, index):  # Index should be multivariate like ["Home", "Price"]
		plot_data = []
		for phase in self.sheets:  # Iterate over sheets in Excel
			plot_data.append(self.get_index(index, df_key=phase))  # Add a small DataFrame
		plot_df = pd.concat(plot_data, axis=1)
		fig, ax = get_plot()
		for company in plot_df.index:
			ax.plot(self.sheets, plot_df.loc[company].values, label=company)
		plt.legend()
		plt.show()

	def plot_two_metrics(self, index1, index2):  # Index should be multivariate like ["Home", "Price"]
		fig, ax = get_plot()
		for phase in self.sheets:  # Iterate over sheets in Excel
			x_data = self.get_index(index1, df_key=phase)
			y_data = self.get_index(index2, df_key=phase)
			ax.scatter(x_data, y_data, label=phase)
		plt.xlabel(" ".join(index1))
		plt.ylabel(" ".join(index2))
		plt.legend()

class InputFrame(tk.Frame):
	def __init__(self, parent, fields, *args, **kwargs):
		tk.Frame.__init__(self, parent, *args, **kwargs)
		self.parent = parent
		self.fields = fields
		self.x_vars = {}
		self.y_vars = {}
		for field in self.fields:
			tk.Label(self, text=" ".join(field)).pack(side="left", fill="both", expand=True)
			check_frame = tk.Frame(self).pack(side="right")
			x_var = tk.BooleanVar()
			self.x_vars[field] = x_var
			tk.Checkbutton(check_frame, variable=x_var).pack(side="left", fill="x")
			y_var = tk.BooleanVar()
			self.y_vars[field] = y_var
			tk.Checkbutton(check_frame, variable=y_var).pack(side="right", fill="x")
			self.pack(fill="both")


class GraphFrame(tk.Frame):
	def __init__(self, parent, *args, **kwargs):
		tk.Frame.__init__(self, parent, *args, **kwargs)
		self.parent = parent
		tk.Label(self, text="GRAPH AREA").pack(expand=True, fill="both")


if __name__ == "__main__":
	calculator = Calculator(pd.read_excel("/Users/reed/PycharmProjects/760_Marketing/New Shoes.xlsx", sheet_name=None, index_col=0, header=[0, 1]))
	root = tk.Tk()
	InputFrame(root, calculator.df["1"].columns).grid(row=0, column=0)
	GraphFrame(root).grid(row=0, column=1)
	root.wm_title("New Shoes Calculator")
	root.mainloop()

	# plot_by_company_over_time(["Home", "Price"])
	# plot_two_metrics(["Domestic", "Price"], ["Domestic", "Customer Satisfaction"])

