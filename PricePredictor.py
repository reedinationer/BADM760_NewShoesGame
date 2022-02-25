import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from pandas.plotting import register_matplotlib_converters
import pandas as pd
import numpy as np
from PlotSettings import *
import tkinter as tk
from tkinter import ttk
from threading import Thread

register_matplotlib_converters()

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

	def get_x_y_by_phase(self, x_index, y_index):  # Index should be multivariate like ["Home", "Price"]
		result_x = []
		result_y = []
		for phase in self.sheets:  # Iterate over sheets in Excel
			x_data = self.get_index(x_index, df_key=phase)
			y_data = self.get_index(y_index, df_key=phase)
			result_x.append(x_data)
			result_y.append(y_data)
		return result_x, result_y

class InputFrame(tk.Frame):
	def __init__(self, parent, calc_obj, graph_frame, *args, **kwargs):
		tk.Frame.__init__(self, parent, *args, **kwargs)
		self.parent = parent
		self.calculator = calc_obj
		self.fields = calc_obj.df["1"].columns
		self.graph = graph_frame
		self.x_vars = {}
		self.y_vars = {}
		for field in self.fields:
			row_frame = tk.Frame(self)
			tk.Label(row_frame, text=" ".join(field)).pack(side="left", fill="both", expand=True)
			checkbutton_frame = tk.Frame(row_frame)
			x_var = tk.BooleanVar()
			self.x_vars[field] = x_var
			tk.Checkbutton(checkbutton_frame, variable=x_var, command=self.run_calculation).pack(side="left", fill="both")
			y_var = tk.BooleanVar()
			self.y_vars[field] = y_var
			tk.Checkbutton(checkbutton_frame, variable=y_var, command=self.run_calculation).pack(side="right", fill="both")
			checkbutton_frame.pack(side="right", fill="x")
			row_frame.pack(fill="both")

	def run_calculation(self):
		print("Computing changes")
		used_x_vars = dict(filter(lambda elem: elem[1].get() is True, self.x_vars.items()))  # Filter variables to only have user selections into a new dictionary
		used_y_vars = dict(filter(lambda elem: elem[1].get() is True, self.y_vars.items()))
		if len(used_x_vars) == 1 and len(used_y_vars) == 1:
			self.graph.clear_graph()
			x_var = list(used_x_vars.keys())[0]
			y_var = list(used_y_vars.keys())[0]
			print("graphing {} vs {}".format(x_var, y_var))
			x_dfs, y_dfs = self.calculator.get_x_y_by_phase(x_var, y_var)
			max_x, min_x, max_y, min_y = -1 * np.inf, np.inf, -1 * np.inf, np.inf
			for x, y in zip(x_dfs, y_dfs):
				self.graph.axis.scatter(x, y)
				max_x = max(max(x), max_x)
				min_x = min(min(x), min_x)
				max_y = max(max(y), max_y)
				min_y = min(min(y), min_y)
			self.graph.axis.set_xlabel(" ".join(x_var))
			self.graph.axis.set_ylabel(" ".join(y_var))
			self.graph.axis.grid(which='major', alpha=0.85)
			self.graph.axis.grid(which="minor", alpha=0.3)

			# self.graph.axis.set_xticks(np.linspace(min_x, max_x, 20))
			# self.graph.axis.set_yticks(np.linspace(min_y, max_y, 20))


class GraphFrame(tk.Frame):
	def __init__(self, parent, *args, **kwargs):
		tk.Frame.__init__(self, parent, *args, **kwargs)
		self.parent = parent
		self.fig = Figure(facecolor="white", dpi=100, figsize=(10, 10))
		self.axis = self.fig.add_subplot(111)
		self.fig.set_tight_layout(True)
		self.canvas = FigureCanvasTkAgg(self.fig, master=self)
		self.canvas.get_tk_widget().grid(row=0, column=0, sticky='nsew')
		self.canvas.get_tk_widget().rowconfigure(0, weight=1)
		self.canvas.get_tk_widget().columnconfigure(0, weight=1)

	def clear_graph(self):
		self.axis.clear()
		self.canvas.draw_idle()

	def scatter_data(self, x_data, y_data, x_label=None, y_label=None):
		if x_label:
			self.axis.set_xlabel(x_label)
		if y_label:
			self.axis.set_ylabel(y_label)
		self.axis.scatter(x_data, y_data)
		self.canvas.draw_idle()



if __name__ == "__main__":
	calculator = Calculator(pd.read_excel("/Users/reed/PycharmProjects/760_Marketing/New Shoes.xlsx", sheet_name=None, index_col=0, header=[0, 1]))
	root = tk.Tk()
	graph = GraphFrame(root)
	graph.grid(row=0, column=1)
	InputFrame(root, calculator, graph).grid(row=0, column=0)
	root.columnconfigure(1, weight=1)
	root.rowconfigure(0, weight=1)

	root.wm_title("New Shoes Calculator")
	root.mainloop()

	# plot_by_company_over_time(["Home", "Price"])
	# plot_two_metrics(["Domestic", "Price"], ["Domestic", "Customer Satisfaction"])

