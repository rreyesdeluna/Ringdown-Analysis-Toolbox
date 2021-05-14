'''
************************************************************************
Identification of Electromechanical Modes Driven by Multi-ERA Analysis
Graphic User Intreface

Jose Antonio de la O Serna
Mario Roberto Arrieta Paternina
Rodrigo David Reyes de Luna

April 2021
************************************************************************
'''

import sys, os
import csv
import xlrd
import math
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import tkinter as tk
import tkinter.scrolledtext as st
from tkinter import filedialog, messagebox, ttk
from scipy.fftpack import fft, fftfreq, fftshift
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk



class Window1():

	global font_text
	font_text = 'Courier'

	global color0, color1, color2, color3
	color0 = 'SteelBlue4'
	color1 = 'black'
	color2 = 'grey24'
	color3 = 'snow'


	def __init__(self, master):
		self.master = master
		self.master.title('Multi-ERA')
		self.master.geometry('1580x900')
		self.master.configure(bg = color1)
		self.frame = tk.Frame(self.master)
		self.frame.pack()
		self.master.bind('<Escape>', self.Quit)
		self.Create_Widgets()


	def Create_Widgets(self):

		# MASTER
		title = 'Identification of Electromechanical Modes Driven by Multi-ERA Analysis'
		self.lbl0 = tk.Label(self.master, text = title, font = (font_text, 14), fg = 'white', bg = color0, anchor = tk.CENTER)
		self.lbl0.pack(fill = 'x')

		self.lbl1 = tk.Label(self.master, text = '?', font = (font_text, 14), fg = 'white', bg = color1, anchor = tk.CENTER)
		self.lbl1.place(relx = 1.00, rely = 0.0, height = 28, width = 30,  anchor = tk.NE)
		self.lbl1.bind('<Button-1>', self.Info)

		# LABELFORM 1 - READ FILE
		self.lbfrm1 = tk.LabelFrame(self.master, text = 'Read File', font = (font_text, 10), fg = 'white', bg = color1)
		self.lbfrm1.place(x = 8, y = 35, height = 80, relwidth = 0.600, anchor = tk.NW)

		self.btn1 = tk.Button(self.lbfrm1, text = 'Browse', font = (font_text, 10), command = self.click_btn1, anchor = tk.CENTER)
		self.btn1.place(x = 4, y = 2, height = 24, width = 90)

		self.ent1 = tk.Entry(self.lbfrm1, fg = 'white', font = (font_text, 10), bg = color2)
		self.ent1.place(x = 96, y = 2, height = 24, relwidth = 0.86)
		self.ent1.insert(0, 'Select data file...')

		self.btn2 = tk.Button(self.lbfrm1, text = 'Edit', font = (font_text, 10), command = self.click_btn2, anchor = tk.CENTER)
		self.btn2.place(x = 4, y = 30, height = 24, width = 90)

		self.val_W1ent2 = tk.StringVar()
		self.val_W1ent2.set('Edit signals...')
		self.ent2 = tk.Entry(self.lbfrm1, textvariable = self.val_W1ent2, fg = 'white', font = (font_text, 10), bg = color2)
		self.ent2.place(x = 96, y = 30, height = 24, relwidth = 0.86)

		# MASTER
		self.btn3 = tk.Button(self.master, text = 'RUN', font = (font_text, 12), command = self.click_btn3, anchor = tk.CENTER)
		self.btn3.place(x = 14, y = 134, height = 42, width = 90)

		# LABELFORM 2 - SETTINGS
		self.lbfrm2 = tk.LabelFrame(self.master, text = 'Settings', font = (font_text, 10), fg = 'white', bg = color1)
		self.lbfrm2.place(x = 110, y = 126, height = 50, relwidth = 0.915, anchor = tk.NW)

		self.lbl2 = tk.Label(self.lbfrm2, text = 'Time interval [start][end]:', font = (font_text, 10), fg = 'white', bg = color1,  anchor = tk.E)
		self.lbl2.place(x = 4, y = 1, height = 24, width = 230)

		self.val_W1ent3 = tk.DoubleVar()
		self.ent3 = tk.Entry(self.lbfrm2, textvariable = self.val_W1ent3, fg = 'white', font = (font_text, 10), bg = color2)
		self.ent3.place(x = 235, y = 1, height = 24, width = 100)

		self.val_W1ent4 = tk.DoubleVar()
		self.ent4 = tk.Entry(self.lbfrm2, textvariable = self.val_W1ent4, fg = 'white', font = (font_text, 10), bg = color2)
		self.ent4.place(x = 340, y = 1, height = 24, width = 100)

		self.lbl3 = tk.Label(self.lbfrm2, text = 'Frequency interval (Hz.) [min][max]:', font = (font_text, 10), fg = 'white', bg = color1,  anchor = tk.E)
		self.lbl3.place(x = 528, y = 1, height = 24, width = 320)

		self.ent5 = tk.Entry(self.lbfrm2, fg = 'white', font = (font_text, 10), bg = color2)
		self.ent5.place(x = 850, y = 1, height = 24, width = 60)

		self.ent6 = tk.Entry(self.lbfrm2, fg = 'white', font = (font_text, 10), bg = color2)
		self.ent6.place(x = 915, y = 1, height = 24, width = 60)

		self.lbl4 = tk.Label(self.lbfrm2, text = 'Energy threshold (%):', font = (font_text, 10), fg = 'white', bg = color1,  anchor = tk.E)
		self.lbl4.place(x = 1048, y = 1, height = 24, width = 210)

		self.val_W1ent7 = tk.DoubleVar()
		self.val_W1ent7.set(100.0)
		self.ent7 = tk.Entry(self.lbfrm2, textvariable = self.val_W1ent7, fg = 'white', font = (font_text, 10), bg = color2)
		self.ent7.place(x = 1260, y = 1, height = 24, width = 70)

		self.btn4 = tk.Button(self.lbfrm2, text = 'Edit', font = (font_text, 10), command = self.click_btn4, anchor = tk.CENTER)
		self.btn4.place(x = 1336, y = 1, height = 24, width = 90)

		# LABELFORM 3 - RESULTS
		self.lbfrm3 = tk.LabelFrame(self.master, text = 'Results', font = (font_text, 10), fg = 'white', bg = color1)
		self.lbfrm3.place(x = 8, y = 190, relheight = 0.77, relwidth = 0.980, anchor = tk.NW)

		self.lbl5 = tk.Label(self.lbfrm3, text = 'Select a Signal to be Analized: ', font = (font_text, 10), fg = 'white', bg = color1,  anchor = tk.W)
		self.lbl5.place(relx = 0.00, rely = 0.006, relwidth = 0.17, anchor = tk.NW)

		self.val_opmn1 = tk.StringVar()
		self.opmn1 = tk.OptionMenu(self.lbfrm3, self.val_opmn1, ())
		self.opmn1.place(relx = 0.18, rely = 0.00, relwidth = 0.11, anchor = tk.NW)

		# TREE VIEW FOR SHOW MODAL DATA
		trv1_columns 	= ('#1', '#2', '#3', '#4', '#5', '#6', '#7', '#8', '#9', '#10')
		trv1_name		= ('Selection',	'Mode', 'Type', 'Frequency', 'Amplitude', 'Damping', 'Damping Ratio', 'Phase', 'Roots', 'Energy')
		self.trv1 = ttk.Treeview(self.lbfrm3,  show='headings', selectmode = 'browse', columns = trv1_columns)
		self.trv1.place(relx = .002, rely = 0.07, relheight = 0.92, relwidth = .29, anchor = tk.NW)

		for index, item in enumerate(trv1_columns):
			self.trv1.column(item, width = 100, minwidth=50, anchor=tk.CENTER)
			self.trv1.heading(item, text = trv1_name[index], anchor=tk.CENTER)

		self.treescrollx = tk.Scrollbar(self.trv1, orient = 'horizontal', command = self.trv1.xview)
		self.treescrolly = tk.Scrollbar(self.trv1, orient = 'vertical', command = self.trv1.yview)
		self.trv1.configure(xscrollcommand = self.treescrollx.set, yscrollcommand = self.treescrolly.set)
		self.treescrolly.pack(side = 'right', fill = tk.Y)
		self.treescrollx.pack(side = 'bottom', fill = tk.X)

		# NOTEBOOK FOR GRAPHICS
		self.tbctrl = ttk.Notebook(self.lbfrm3)
		self.tbctrl.place(relx = 0.297, rely = 0.00, relwidth = 0.70, relheight = 0.99, anchor = tk.NW)
		self.tab1 = ttk.Frame(self.tbctrl)
		self.tab2 = ttk.Frame(self.tbctrl)
		self.tab3 = ttk.Frame(self.tbctrl)
		self.tab4 = ttk.Frame(self.tbctrl)
		self.tbctrl.add(self.tab1, text ='Signals')
		self.tbctrl.add(self.tab2, text ='FFT')
		self.tbctrl.add(self.tab3, text ='Mode Shapes')
		self.tbctrl.add(self.tab4, text ='Roots')


	def Info(self, event = None):
		tx0 = 'Reference:\n\n'
		tx1 = 'Identification of Electromechanical Modes in Power Systems\n'
		tx2 = 'IEEE Power & Energy Society\n'
		tx3 = 'June 2012\n\n'
		tx4	= 'Autors:\n\n'
		tx5 = 'Jose Antonio de la O Serna\n'
		tx6 = 'Mario Roberto Arrieta Paternina\n'
		tx7 = 'Rodrigo David Reyes de Luna\n\n'
		tx8 = 'Version 0.0\napril 6th, 2021'

		info_text = tx0+tx1+tx2+tx3+tx4+tx5+tx6+tx7+tx8
		tk.messagebox.showinfo('Info', info_text)


	def click_btn1(self):

		# -------------------
		# |     BROWSE      |
		# -------------------

		self.ent1.delete(0, 'end')
		self.ent2.delete(0, 'end')
		self.ent3.delete(0, 'end')
		self.ent4.delete(0, 'end')

		file_path = filedialog.askopenfilename(title		='Select a file',
		                          	   		   filetype		=[('csv files', '*.csv'),('xlsx files', '*.xlsx')])
		self.ent1.insert(0, file_path)

		if self.Check_Data() == True:

			Data, h_vec, t_vec, y_vec =  self.Get_Data(file_path)

			h_vec = str(h_vec[1:]).replace("'", '')[1:-1]
			self.ent2.insert(0, h_vec)

			self.ent3.insert(0, t_vec[0])
			self.ent4.insert(0, t_vec[-1])


	def click_btn2(self):
		
		# -------------------
		# |      EDIT       |
		# -------------------

		if self.Check_Data() == True:

			file_path = self.ent1.get()

			Window2(tk.Toplevel(self.master), self.val_W1ent2, self.val_W1ent3, self.val_W1ent4, file_path)


	def click_btn3(self):

		# -------------------
		# |       RUN       |
		# -------------------

		if self.Check_Data(2, 34, 56, 7) == True:

			list_signals = self.List_Data_byComas(self.ent2.get())
			self.opmn1.destroy()
			self.opmn1 = tk.OptionMenu(self.lbfrm3, self.val_opmn1, *list_signals, command = self.Fig_Signals)
			self.opmn1.place(relx = 0.18, rely = 0.00, relwidth = 0.11, anchor = tk.NW)
			self.val_opmn1.set(list_signals[0])

			self.Multi_ERA()


	def Multi_ERA(self):

		global h_vec, can, t, y, list_signals, t_start, t_end, N, m, freq, damp, damprat, M_mag, M_ang, M_ene, roots

		file_path 		= self.ent1.get()
		list_signals	= self.List_Data_byComas(self.ent2.get())
		t_start 		= float(self.ent3.get())
		t_end 			= float(self.ent4.get())
		enrg_th 		= float(self.ent7.get())

		Data, h_vec, t_vec, y_vec 	= self.Get_Data(file_path)

		t_start 	= float(t_start)
		t_end 		= float(t_end)

		dt = float(t_vec[1] - t_vec[0])
		pa = int(round(t_start / dt, 0))
		pb = int(round(t_end / dt, 0))

		for i in range(len(h_vec[1:]), 0, -1):
			if h_vec[i] not in list_signals:
				y_vec = np.delete(y_vec, (i - 1), axis = 1)

		y1 	= y_vec[pa:pb , :]
		t 	= t_vec[pa:pb]
		N 	= len(t)

		y_mean 	= np.zeros([y1.shape[0] , y1.shape[1]])
		y 		= np.zeros([y1.shape[0] , y1.shape[1]])

		for j in range(y1.shape[1]):
			y_mean[: , j] = y1[: , j]
			y_mean[: , j] = y_mean[: , j] - np.mean(y_mean[: , j])
			y[:,j] = y_mean[: , j]

		med = y.shape[0]
		can = y.shape[1]
		r 	= int(np.around((med / 2.0) - 1.0, 0))

		# DTFT..................................................................

		y_z = np.zeros([2**14 , 1]) 
		medf = len(y[:,0])

		S0 = np.zeros([len(y_z) + medf , can])
		Es = np.zeros([len(y_z) + medf , can], dtype = np.complex)

		for i in range(can):
			S0[: , i] = np.concatenate((y[: , i], y_z), axis = None)
			Es[: , i] = fftshift(fft(S0[: , i]))

		fx = np.linspace(-1.0 / (2.0 * dt), 1.0 / (2.0 * dt), len(S0[: , 0]))

		self.Fig_DTFT(can, fx, Es, list_signals)

		# DTFT..................................................................

		H0 = np.zeros([r * can, r])
		H1 = np.zeros([r * can, r])
		for j in range(r):
			for i in range(r):
				H0[can*i: can*(i+1) , j] = y[j+i+1 , :]
				H1[can*i: can*(i+1) , j] = y[j+i+2 , :]

		u, s0, v0 = np.linalg.svd(H0, full_matrices=True)
		s = np.diag(s0)
		v = v0.T

		sum_s = sum(s0)
		sum_st = 0.0
		for m, i in enumerate(s0, start = 1):
			sum_st 		= sum_st + i
			pc_sum_st 	= (sum_st / sum_s) * 100.0
			if pc_sum_st > enrg_th: break
		
		U = u[: , 0:m]
		S = s[0:m , 0:m]
		V = v[: , 0:m]

		Srn = np.zeros((m,m))
		for i in range(m):
			Srn[i,i] = pow(S[i,i], -0.5)

		A = np.dot(Srn , U.T)
		A = np.dot(A , H1)
		A = np.dot(A , V)
		A = np.dot(A , Srn)

		eigA, z = np.linalg.eig(A)
		lam = np.log(eigA)/dt

		Z = np.zeros((N, m), dtype = np.complex)
		for i in range(N):
			Z[i, :] = pow(eigA, i)

		B = np.dot(np.linalg.pinv(Z), y)

		# Results ------------------------------------------------->
		roots 	= eigA.real
		damp 	= -lam.real
		freq 	= lam.imag / (2.0 * np.pi)
		M_mag 	= 2 * abs(B)
		M_ang 	= np.angle(B)

		# Change any zero in frequency vector by -0.0001
		zrs = list(np.where(freq == 0.0)[0])
		for z in zrs: freq[z] = -0.0001

		omga	= 2.0 * np.pi * freq
		damprat	= (damp / omga) * 100.0

		M_ene = np.zeros((len(freq) , can))
		for i in range(len(freq)):
			M_ene[i , :] = (1.0 / 2.0) * (omga[i]**2)  * (M_mag[i , :]**2)

		# Results -------------------------------------------------<

		print('\n')
		print('--> Inter-Area Oscillating Modes')
		print('Mode  Freq      Damping   DampRat   zReal')
		print('====  ========  ========  ========  ========')

		j = 0
		for i in range(len(freq)):
			fr = freq[i]
			zr = (eigA[i]).real
			da 	= damp[i]
			dr 	= damprat[i]
			j 	= j + 1
			md 	= j
			print('%4d, %8.4f, %8.4f, %8.4f, %8.4f' % (md, fr, da, dr, zr))

		self.Load_trv1()
		self.Fig_Signals()


	def Fig_DTFT(self, can, fx, Es, list_signals):

		try:
			self.canvas.get_tk_widget().pack_forget()
		except:
			pass

		plt.style.use('dark_background')
		self.fig = plt.Figure(dpi = 100) 
		ax = self.fig.add_subplot(111)
		ax.set_xlabel('Frequency (Hz.)')
		ax.set_ylabel('Magnitude')
		ax.set_xlim(float(self.ent5.get()), float(self.ent6.get()))
		self.fig.subplots_adjust(left = 0.09, bottom = 0.16, right = 0.90, top = 0.95)
		self.canvas = FigureCanvasTkAgg(self.fig, self.tab2)
		self.canvas.draw() 
		self.canvas.get_tk_widget().place(relheight = 1.00, relwidth = 1.00)
		self.toolbar = NavigationToolbar2Tk(self.canvas, self.tab2)
		self.toolbar.place(relx = 0.50, rely = 1.00, relwidth = 1.00, anchor = tk.S)
		self.toolbar.update()

		colors = plt.cm.get_cmap('gist_rainbow', can) #hsv
		for i in range(can):
			ax.plot(fx, abs(Es[: , i]) / (2**14), color = colors(i), label = list_signals[i], lw = '2')
		
		ax.legend(loc = 'center right', bbox_to_anchor = (1.12, 0.5))


	def Load_trv1(self):

		for index, i in enumerate(list_signals):
			if i == self.val_opmn1.get():
				i_signal = index
				break

		self.trv1.delete(*self.trv1.get_children())
		mode = 0
		for i in range(m):
			if freq[i] > 0:
				
				frq = freq[i]
				osc_mod = '-'
				# if frq >= 0.05 and frq < 0.40: osc_mod = 'Inter-Area'  #EPRI
				if frq >= 0.10 and frq < 0.80: osc_mod = 'Inter-Area'
				if frq >= 0.80 and frq < 2.00: osc_mod = 'Local'
				if frq >= 2.00 and frq < 3.00: osc_mod = 'Intra-Plant'

				mode = mode + 1
				row_val = ('✓', mode, osc_mod, round(freq[i], 4), round(M_mag[i, i_signal], 4), round(damp[i], 4), 
					round(damprat[i], 4), round(M_ang[i, i_signal], 4), round(roots[i], 4), round(M_ene[i, i_signal]), 4)
				self.trv1.insert('', i, text = True, values = row_val)

		self.trv1.bind('<<TreeviewSelect>>', self.Selection_trv1)


	def Selection_trv1(self, event):

		dic_item = {}
		for index, item in enumerate(self.trv1.get_children()):
			dic_item[index] = item

		index       = self.trv1.index(self.trv1.selection())
		row_data    = self.trv1.item(dic_item[index])['values']
		row_text    = self.trv1.item(dic_item[index])['text']

		if row_text == True:
			row_data[0] = ''
			text = False
		else:
			row_data[0] = '✓'
			text = True

		self.trv1.delete(dic_item[index])
		self.trv1.insert('', index, text = text, values = row_data)

		self.Fig_Signals()


	def Fig_Signals(self, *args):

		for index, i in enumerate(list_signals):
			if i == self.val_opmn1.get():
				i_signal = index
				break

		dic_item = {}
		for index, item in enumerate(self.trv1.get_children()):
			dic_item[index] = item
			row_data    = self.trv1.item(dic_item[index])['values']
			row_text    = self.trv1.item(dic_item[index])['text']

		t_era = np.linspace(0, t_end - t_start, N)
		y_era = np.zeros((N))

		dicc_mode = {}
		mode = 0
		for i in range(m):
			if freq[i] > 0:
				dicc_mode[i] = mode
				mode = mode + 1

		for i in range(m):
			if (freq[i] > 0) and (self.trv1.item(dic_item[dicc_mode[i]])['text'] == True):

				mgn = M_mag[i , :]
				ang = M_ang[i , :]
				dmp = damp[i]
				frq = freq[i]

				y_era = y_era + mgn[i_signal] * np.exp(-dmp * t_era) * np.cos((2 * np.pi * frq) * t_era + ang[i_signal])

		try:
			self.canvas.get_tk_widget().pack_forget()
		except:
			pass

		plt.style.use('dark_background')
		self.fig = plt.Figure(dpi = 100) 
		ax = self.fig.add_subplot(111)
		ax.set_xlabel('Time')
		ax.set_ylabel('Magnitude')
		ax.set_facecolor('k')
		self.fig.subplots_adjust(left = 0.08, bottom = 0.16, right = 0.96, top = 0.95)
		self.canvas = FigureCanvasTkAgg(self.fig, self.tab1)
		self.canvas.draw() 
		self.canvas.get_tk_widget().place(relheight = 1.00, relwidth = 1.00)
		self.toolbar = NavigationToolbar2Tk(self.canvas, self.tab1)
		self.toolbar.place(relx = 0.50, rely = 1.00, relwidth = 1.00, anchor = tk.S)
		self.toolbar.update()

		colors = plt.cm.get_cmap('gist_rainbow', can)
		# for i in range(can):

		s0 		= np.linalg.norm(list(y[: , i_signal]))
		s1 		= np.linalg.norm(list(y_era))
		sfull2 	= pow(s0 , 2)
		e2 		= pow(s0 - s1 , 2)
		SNR 	= round(10 * math.log10(sfull2 / e2) , 2)

		ax.plot(t, y[: , i_signal], color = colors(i_signal), label = list_signals[i_signal] + ': ' + str(SNR), lw = '2')
		ax.plot(t, y_era, dashes = [6,4], color = colors(i_signal), lw = '2')

		ax.legend(loc = 'upper right', title = 'Signal Noise Ratio [dB]')


	def click_btn4(self):
		
		# -------------------
		# |      EDIT       |
		# -------------------

		if self.Check_Data(2, 34, 7) == True:

			file_path 		= self.ent1.get()
			list_signals	= self.List_Data_byComas(self.ent2.get())
			t_start 		= self.ent3.get()
			t_end 			= self.ent4.get()
			energy_th 		= self.ent7.get()

			Data, h_vec, t_vec, y_vec 	= self.Get_Data(file_path)

			Window3(tk.Toplevel(self.master), self.val_W1ent7, file_path, list_signals, t_start, t_end, energy_th, h_vec, t_vec, y_vec)


	def List_Data_byComas(self, str_signals):

		str_signals = str_signals.replace(' ', '')

		if str_signals[0] 	== ',': str_signals = str_signals[1:]
		if str_signals[-1] 	== ',': str_signals = str_signals[:-1]

		list_signals = []

		a = 0
		for i in range(len(str_signals)):
			if str_signals[i] == ',':
				list_signals.append(str_signals[a : i])
				a = i + 1

		list_signals.append(str_signals[a : len(str_signals)])

		return list_signals


	def Check_Data(self, *args):

		file_path 	= self.ent1.get()
		str_signals = self.ent2.get()
		t_start 	= self.ent3.get()
		t_end 		= self.ent4.get()
		f_min		= self.ent5.get()
		f_max		= self.ent6.get()
		energy_th	= self.ent7.get()

		if os.path.isfile(file_path) == False:
			tk.messagebox.showerror('Error', 'The file you have chosen is not valid.')
			return False

		if ((file_path.endswith('.csv') == False) and (file_path.endswith('.xlsx') == False)):
			tk.messagebox.showerror('Error', 'The file you have chosen is not valid. Must be extension csv or xlsx.')
			return False

		Data, h_vec, t_vec, y_vec =  self.Get_Data(file_path)

		if len(Data) == 0:
			tk.messagebox.showerror('Error', 'The file you have chosen is empty.')
			return False

		if len(y_vec) == 0:
			tk.messagebox.showerror('Error', 'Invalid format. See Details.')
			return False


		if 2 in args:
			
			list_signals = self.List_Data_byComas(str_signals)

			for i in list_signals:
				if i not in h_vec:
					tk.messagebox.showerror('Error', 'The name signals are not valid. Check "' + str(i) + '"')
					return False

		if 34 in args:

			try:
				t_start = float(t_start)
				t_end 	= float(t_end)
			except:
				tk.messagebox.showerror('Error', 'Time interval data are not valid.')
				return False

			if (t_start < t_vec[0]) or (t_start >= t_end) or (t_end > t_vec[-1]):
				tk.messagebox.showerror('Error', 'Time interval is not valid.')
				return False

		if 56 in args:

			try:
				f_min = float(f_min)
				f_max = float(f_max)
			except:
				tk.messagebox.showerror('Error', 'Frecuency interval data are not valid.')
				return False

			if (f_min < 0) or (f_min >= f_max):
				tk.messagebox.showerror('Error', 'Frecuency interval is not valid.')
				return False

		if 7 in args:

			try:
				energy_th = float(energy_th)
			except:
				tk.messagebox.showerror('Error', 'Energy threshold data are not valid.')
				return False

			if (energy_th <= 0) or (energy_th > 100.0):
				tk.messagebox.showerror('Error', 'Energy threshold data out of range.')
				return False

		return True


	def Get_Data(self, file_path):

		Data 	= []
		Y 		= []

		if file_path.endswith('.csv'):
			csvData = csv.reader(open(file_path))
			for column in csvData:
				Data.append(column)

		if file_path.endswith('.xlsx'):
			wb = xlrd.open_workbook(file_path)
			sh = wb.sheet_by_index(0)
			for i in range(sh.nrows):
				Data.append(sh.row_values(i))

		if len(Data) > 0:
			if len(Data[0]) > 1:

				h_vec = Data[0]
				t, y = [], []
				for index, iData in enumerate(Data[1:]):
					t.append(float(iData[0]))
					y.append([])

					for jData in iData[1:]:
						y[index].append(float(jData))

				y_vec = np.array(y)
				t_vec = np.array(t)

				return Data, h_vec, t_vec, y_vec

		return Data, [], [], []


	def Quit(self, event = None):
		# QUIT
		self.master.destroy()



class Window2():

	def __init__(self, master, val_W1ent2,  val_W1ent3,  val_W1ent4, file_path):
		self.master = master
		self.val_W1ent2 = val_W1ent2
		self.val_W1ent3 = val_W1ent3
		self.val_W1ent4 = val_W1ent4
		self.master.title('Data Check')
		self.master.geometry('1600x900')
		self.master.configure(bg = color1)
		self.frame = tk.Frame(self.master)
		self.frame.pack()
		self.master.bind('<Escape>', self.click_btn4)
		self.Create_Widgets(file_path)


	def Create_Widgets(self, file_path):

		file_name = os.path.basename(file_path)
		Data, h_vec, t_vec, y_vec = self.Get_data(file_path)

		# TITLE LABEL
		self.lbl1 = tk.Label(self.master, text = 'file = ' + file_name, font = (font_text, 14), fg = 'white', bg = color0,  anchor = tk.CENTER)
		self.lbl1.place(height = 25, relwidth = 1)

		# LABELFORM 1 - DATA
		self.lbfrm1 = tk.LabelFrame(self.master, text = 'Data', font = (font_text, 10), fg = 'white', bg = color1)
		self.lbfrm1.place(y = 25, relx = 0.50, relheight = 0.28, relwidth = 0.99, anchor = tk.N)

		self.btn1 = tk.Button(self.lbfrm1, text = 'Select All', font = (font_text, 10), command = lambda: self.click_btn12(True, h_vec, t_vec, y_vec), anchor = tk.CENTER)
		self.btn1.place(y = 0, x = 4, height = 24, relwidth = 0.114, anchor = tk.NW)

		self.btn2 = tk.Button(self.lbfrm1, text = 'Deselect All', font = (font_text, 10), command = lambda: self.click_btn12(False, h_vec, t_vec, y_vec), anchor = tk.CENTER)
		self.btn2.place(y = 28, x = 4, height = 24, relwidth = 0.114, anchor = tk.NW)

		# TREE VIEW FOR SELECTING DATA
		self.trv1 = ttk.Treeview(self.lbfrm1, show = 'headings', selectmode = 'browse', height = 20, columns = ('#1', '#2'))
		self.trv1.place(y = 56, x = 4, relheight = 0.75, relwidth = 0.114, anchor = tk.NW)

		self.trv1.column('#1', minwidth = 0, width = 40, anchor = tk.CENTER, stretch = tk.NO)
		self.trv1.column('#2', minwidth = 0, width = 100, anchor = tk.CENTER)

		self.trv1.heading('#1', text='', anchor=tk.CENTER)
		self.trv1.heading('#2', text='Signal', anchor=tk.CENTER)

		for index, i in enumerate(h_vec[1:]):
			self.trv1.insert('', index, text = True, values = ('✓', i))

		self.vsb = ttk.Scrollbar(self.trv1, orient = 'vertical', command = self.trv1.yview)
		self.vsb.pack(side = 'right', fill = 'y')
		self.trv1.configure(yscrollcommand = self.vsb.set)
		self.trv1.bind('<<TreeviewSelect>>', lambda event: self.Select_trv1(event, h_vec, t_vec, y_vec))


		# TREE VIEW FOR SHOW DATA
		self.trv2 = ttk.Treeview(self.lbfrm1,  show='headings')
		self.trv2.place(relx = 1.00, rely = 0.50, relheight = 1.00, relwidth = .88, anchor = tk.E)
		self.treescrolly = tk.Scrollbar(self.trv2, orient = 'vertical', command = self.trv2.yview)
		self.treescrollx = tk.Scrollbar(self.trv2, orient = 'horizontal', command = self.trv2.xview)
		self.trv2.configure(xscrollcommand = self.treescrollx.set, yscrollcommand = self.treescrolly.set)
		self.treescrolly.pack(side = 'right', fill = tk.Y)
		self.treescrollx.pack(side = 'bottom', fill = tk.X)
		self.Load_trv2(Data)

		# LABELFORM 2 - CHART
		self.lbfrm2 = tk.LabelFrame(self.master, text = 'Chart', font = (font_text, 10), fg = 'white', bg = color1)
		self.lbfrm2.place(relx = 0.50, rely = 0.31, relheight = 0.63, relwidth = 0.99, anchor = tk.N)

		self.lbl3 = tk.Label(self.lbfrm2, text = 'Select time interval\nto be analized', font = (font_text, 10), fg = 'white', bg = color1, justify = tk.LEFT, anchor = tk.NW)
		self.lbl3.place(relx = 0.056, rely = 0.045, height = 40, relwidth = 0.11, anchor = tk.CENTER)

		self.lbl4 = tk.Label(self.lbfrm2, text = 'Initial time:', font = (font_text, 10), fg = 'white', bg = color1, anchor = tk.W)
		self.lbl4.place(relx = 0.036, rely = 0.145, height = 24, relwidth = 0.07, anchor = tk.CENTER)

		self.ent1 = tk.Entry(self.lbfrm2, fg = 'white', font = (font_text, 10), bg = color2)
		self.ent1.place(relx = 0.072, rely = 0.145, height = 24, relwidth = 0.038, anchor = tk.W)
		self.ent1.insert(0, float(self.val_W1ent3.get()))
		self.ent1.bind('<Return>', lambda event: self.Load_Chart(h_vec, t_vec, y_vec))

		self.lbl5 = tk.Label(self.lbfrm2, text = 'Final time:', font = (font_text, 10), fg = 'white', bg = color1, anchor = tk.W)
		self.lbl5.place(relx = 0.036, rely = 0.200, height = 24, relwidth = 0.07, anchor = tk.CENTER)

		self.ent2 = tk.Entry(self.lbfrm2, fg = 'white', font = (font_text, 10), bg = color2)
		self.ent2.place(relx = 0.072, rely = 0.200, height = 24, relwidth = 0.038, anchor = tk.W)
		self.ent2.insert(0, float(self.val_W1ent4.get()))
		self.ent2.bind('<Return>', lambda event: self.Load_Chart(h_vec, t_vec, y_vec))

		self.val_W2chb1 = tk.BooleanVar()
		self.val_W2chb1.set(True)
		self.chb1 = tk.Checkbutton(self.lbfrm2, variable = self.val_W2chb1, text = 'Remove mean value', 
			onvalue = True, offvalue = False, fg = 'white', bg = color1, anchor = tk.W, command = lambda: self.Load_Chart(h_vec, t_vec, y_vec))
		self.chb1.config(selectcolor="#000000")
		self.chb1.place(relx = 0.00, rely = 0.300, height = 24, relwidth = 0.11, anchor = tk.W)

		self.val_W2chb2 = tk.BooleanVar()
		self.val_W2chb2.set(True)
		self.chb2 = tk.Checkbutton(self.lbfrm2, variable = self.val_W2chb2, text = 'Normalize all signals', 
			onvalue = True, offvalue = False, fg = 'white', bg = color1, anchor = tk.W)
		self.chb2.config(selectcolor="#000000")
		self.chb2.place(relx = 0.00, rely = 0.360, height = 24, relwidth = 0.11, anchor = tk.W)

		self.Load_Chart(h_vec, t_vec, y_vec)

		# MASTER
		self.btn4 = tk.Button(self.master, text = 'Quit', font = (font_text, 10), command = self.click_btn4, anchor = tk.CENTER)
		self.btn4.place(relx = 0.820, rely = 0.970, height = 26, relwidth = 0.10, anchor = tk.CENTER)

		self.btn5 = tk.Button(self.master, text = 'Accept', font = (font_text, 10), command = lambda: self.click_btn5(h_vec), anchor = tk.CENTER)
		self.btn5.place(relx = 0.930, rely = 0.970, height = 26, relwidth = 0.10, anchor = tk.CENTER)


	def Get_data(self, file_path):

		Data = []
		Y = []

		if file_path.endswith('.csv'):
			csvData = csv.reader(open(file_path))
			for column in csvData:
				Data.append(column)

		if file_path.endswith('.xlsx'):
			wb = xlrd.open_workbook(file_path)
			sh = wb.sheet_by_index(0)
			for i in range(sh.nrows):
				Data.append(sh.row_values(i))

		h_vec = Data[0]
		t, y = [], []
		for index, iData in enumerate(Data[1:]):
			t.append(float(iData[0]))
			y.append([])

			for jData in iData[1:]:
				y[index].append(float(jData))

		y_vec = np.array(y)
		t_vec = np.array(t)

		return Data, h_vec, t_vec, y_vec

	
	def Select_trv1(self, event, h_vec, t_vec, y_vec):

		dic_item = {}
		for index, item in enumerate(self.trv1.get_children()):
			dic_item[index] = item

		index       = self.trv1.index(self.trv1.selection())
		row_data    = self.trv1.item(dic_item[index])['values']
		row_text    = self.trv1.item(dic_item[index])['text']

		if row_text == True:
			row_data[0] = ''
			text = False
		else:
			row_data[0] = '✓'
			text = True

		self.trv1.delete(dic_item[index])
		self.trv1.insert('', index, text = text, values = row_data)

		self.Load_Chart(h_vec, t_vec, y_vec)



	def Load_Chart(self, h_vec, t_vec, y_vec):

		try:
			float(self.ent1.get())
			float(self.ent2.get())

			if (float(self.ent1.get()) < t_vec[0]) or (float(self.ent1.get()) >= float(self.ent2.get())):
				self.ent1.delete(0, 'end')
				self.ent1.insert(0, t_vec[0])

			if (float(self.ent2.get()) <= float(self.ent1.get())) or (float(self.ent2.get()) > t_vec[-1]):
				self.ent2.delete(0, 'end')
				self.ent2.insert(0, t_vec[-1])

		except:
			self.ent1.delete(0, 'end')
			self.ent2.delete(0, 'end')
			self.ent1.insert(0, t_vec[0])
			self.ent2.insert(0, t_vec[-1])

		y_vec_plot = np.zeros([y_vec.shape[0] , y_vec.shape[1]])
		if self.val_W2chb1.get() == True:
			for i in range(y_vec.shape[1]):
				y_vec_plot[: , i] = y_vec[: , i] - np.mean(y_vec[: , i])
		else:
			y_vec_plot = y_vec

		try:
			self.canvas.get_tk_widget().pack_forget()
		except:
			pass

		plt.style.use('dark_background')
		self.fig = plt.Figure(dpi = 100)#, facecolor = 'grey') 
		ax = self.fig.add_subplot(111)
		ax.set_xlabel('Time')
		ax.set_ylabel('Magnitude')
		self.fig.subplots_adjust(left = 0.07, bottom = 0.16, right = None, top = 0.95)
		self.canvas = FigureCanvasTkAgg(self.fig, self.lbfrm2)
		self.canvas.draw() 
		self.canvas.get_tk_widget().place(relx = 0.995, rely = 0.50, relheight = 0.98, relwidth = .88, anchor = tk.E)
		self.toolbar = NavigationToolbar2Tk(self.canvas, self.lbfrm2)
		self.toolbar.place(height = 32, relx = 0.9950, rely = 0.99, relwidth = .88, anchor = tk.SE)
		self.toolbar.update()

		colors = plt.cm.get_cmap('gist_rainbow', len(h_vec))
		ax.axvline(float(self.ent1.get()), color = 'w', linestyle = 'dashed')
		ax.axvline(float(self.ent2.get()), color = 'w',  linestyle = 'dashed')

		for index, item in enumerate(self.trv1.get_children()):
			row_text = self.trv1.item(item)['text']

			if row_text == True:
				ax.plot(t_vec, y_vec_plot[:,index], label = h_vec[1:][index], lw = '2', color = colors(index))
			
		try:
			ax.legend(loc = 'center right', bbox_to_anchor = (1.12, 0.5))
		except:
			pass
		

	def Load_trv2(self, Data):

		h_vec = Data[0]
		self.trv2['column'] = h_vec

		for i in range(len(h_vec)):
			self.trv2.heading(i, text = h_vec[i])
			self.trv2.column('#' + str(int(i+1)), width = 100, minwidth = 20, stretch = tk.YES, anchor = tk.CENTER)

		for i in range(len(Data)):
			if i > 0: self.trv2.insert('','end', values = Data[i])


	def click_btn12(self, value, h_vec, t_vec, y_vec):
		# DE/SELECT ALL

		for index, item in enumerate(self.trv1.get_children()):

			row_data = self.trv1.item(item)['values']
			row_text = self.trv1.item(item)['text']

			if row_text == (not value):

				if value == True	: row_data[0] = '✓'
				if value == False	: row_data[0] = ''

				self.trv1.delete(item)
				self.trv1.insert('', index, text = value, values = row_data)

		self.Load_Chart(h_vec, t_vec, y_vec)


	def click_btn4(self, event = None):
		# QUIT
		self.master.destroy()


	def click_btn5(self, h_vec):
		# ACCEPT
		res = ''
		for item in self.trv1.get_children():

			row_text = self.trv1.item(item)['text']
			row_data = self.trv1.item(item)['values']

			if row_text == True:
				res = res + ', ' + str(row_data[1])

		self.val_W1ent2.set(res[2:])
		self.val_W1ent3.set(self.ent1.get())
		self.val_W1ent4.set(self.ent2.get())

		self.click_btn4()



class Window3():

	def __init__(self, master, val_W1ent7, file_path, list_signals, t_start, t_end, energy_th, h_vec, t_vec, y_vec):

		self.master = master
		self.val_W1ent7 = val_W1ent7
		self.master.title('Singular Values')
		self.master.geometry('1200x800')
		self.master.configure(bg = color1)
		self.frame = tk.Frame(self.master)
		self.frame.pack()
		self.master.bind('<Escape>', self.click_btn1)
		self.Create_Widgets(list_signals, t_start, t_end, h_vec, t_vec, y_vec)


	def Create_Widgets(self, list_signals, t_start, t_end, h_vec, t_vec, y_vec):

		# MASTER
		self.lbl1 = tk.Label(self.master, text = 'Singular Values', font = (font_text, 14), fg = 'white', bg = color0, anchor = tk.CENTER)
		self.lbl1.pack(fill = tk.X)

		# LABERFORM 1 - CHART
		self.lbfrm1 = tk.LabelFrame(self.master, text = 'Chart', font = (font_text, 10), fg = 'white', bg = color1)
		self.lbfrm1.place(y = 30, relx = 0.50, relheight = 0.90, relwidth = 0.99, anchor = tk.N)

		# MASTER
		self.lbl2 = tk.Label(self.master, text = 'Energy threshold (%):', font = (font_text, 10), fg = 'white', bg = color1,  anchor = tk.E)
		self.lbl2.place(relx = 0.100, rely = 0.955, height = 24, width = 220)

		self.ent1 = tk.Entry(self.master, fg = 'white', font = (font_text, 10), bg = color2)
		self.ent1.place(relx = 0.285, rely = 0.955, height = 24, width = 70)
		self.ent1.insert(0, float(self.val_W1ent7.get()))
		self.ent1.bind('<Return>', lambda event: self.Load_Chart(svn))

		svn = self.Get_SVN(list_signals, t_start, t_end, h_vec, t_vec, y_vec)
		self.Load_Chart(svn)

		# MASTER
		self.btn1 = tk.Button(self.master, text = 'Quit', font = (font_text, 10), command = self.click_btn1, anchor = tk.CENTER)
		self.btn1.place(relx = 0.780, rely = 0.955, height = 26, relwidth = 0.10)

		self.btn2 = tk.Button(self.master, text = 'Accept', font = (font_text, 10), command = self.click_btn2, anchor = tk.CENTER)
		self.btn2.place(relx = 0.890, rely = 0.955, height = 26, relwidth = 0.10)


	def click_btn1(self, event = None):
		# QUIT
		self.master.destroy()


	def click_btn2(self):
		# ACCEPT
		self.val_W1ent7.set(self.ent1.get())
		self.click_btn1()


	def Get_SVN(self, list_signals, t_start, t_end, h_vec, t_vec, y_vec):

		t_start 	= float(t_start)
		t_end 		= float(t_end)

		dt = float(t_vec[1] - t_vec[0])
		pa = int(round(t_start / dt, 0))
		pb = int(round(t_end / dt, 0))

		for i in range(len(h_vec[1:]), 0, -1):
			if h_vec[i] not in list_signals:
				y_vec = np.delete(y_vec, (i - 1), axis = 1)

		y1 	= y_vec[pa:pb , :]
		t 	= t_vec[pa:pb]
		N 	= len(t)

		y_mean 	= np.zeros([y1.shape[0] , y1.shape[1]])
		y 		= np.zeros([y1.shape[0] , y1.shape[1]])
		for j in range(y1.shape[1]):
			y_mean[: , j] = y1[: , j]
			y_mean[: , j] = y_mean[: , j] - np.mean(y_mean[: , j])
			y[:,j] = y_mean[: , j]

		med = y.shape[0]
		can = y.shape[1]
		r 	= int(np.around((med / 2.0) - 1.0, 0))

		H0 = np.zeros([r * can, r])
		H1 = np.zeros([r * can, r])
		for b in range(r):
			a = 0
			for c in range(r):
				ya = c + 1
				for j in range(can):
					yb = j
					H0[a, b] = y[ya + b, yb]
					H1[a, b] = y[ya + b + 1, yb]
					a = a + 1

		u, s, v = np.linalg.svd(H0)

		return s


	def Load_Chart(self, svn):

		try:
			float(self.ent1.get())

			if float(self.ent1.get()) < 0.0:
				self.ent1.delete(0, 'end')
				self.ent1.insert(0, 0)

			if float(self.ent1.get()) > 100.0:
				self.ent1.delete(0, 'end')
				self.ent1.insert(0, 100.0)

		except:
			self.ent1.delete(0, 'end')
			self.ent1.insert(0, self.val_W1ent7.get())

		enrg_th 	= float(self.ent1.get())
		sum_s 	= float(sum(svn))
		sum_st 	= float(0.0)
		m 		= int(0)
		for i in svn:
			sum_st 		= sum_st + i
			pc_sum_st 	= (sum_st / sum_s) * 100.0
			m 			= m + 1
			if pc_sum_st >= enrg_th: break

		n = range(1, len(svn) + 1)
		svn = np.log10(svn)

		plt.style.use('dark_background')
		self.fig = plt.Figure(dpi = 100)
		ax = self.fig.add_subplot(111)
		ax.axvline(m, color = 'w', linestyle = 'dashed', linewidth = 1.0)
		ax.plot(n, svn, 'm.-', linewidth = 1.0)
		ax.set_xlabel('Singular Value Number')
		ax.set_ylabel('log10(σ)')

		self.fig.subplots_adjust(left = 0.08, bottom = 0.16, right = 0.95, top = 0.95)
		self.canvas = FigureCanvasTkAgg(self.fig, self.lbfrm1)
		self.canvas.draw() 
		self.canvas.get_tk_widget().place(y = 5, relx = 0.50, relheight = 0.99, relwidth = 1.00, anchor = tk.N)
		self.toolbar = NavigationToolbar2Tk(self.canvas, self.lbfrm1)
		self.toolbar.place(relx = 0.50, rely = 1.00, relwidth = 1.00, anchor = tk.S)
		self.toolbar.update()


def main():
	root 	= tk.Tk()
	app		= Window1(root)
	root.mainloop()


if __name__ == '__main__':
	main()