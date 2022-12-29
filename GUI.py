from tkinter import *
from tkinter.ttk import Combobox, Treeview, Style
from tkinter import messagebox
import sql_commands
import time

# ========================== SQLWindow Setting ========================
SQLWindow = Tk()
SQLWindow.title("SQLWindow")
SQLWindow.geometry('650x350')
SQLWindow.resizable(width=False, height=False)


# ========================== SQLWindow Functions ========================
def clear_list1():
    pass


def fill_list1(items):
    pass


def view_sales_invoices():
    pass


def view_purchase_invoices():
    pass


def view_customers():
    pass


def view_sellers():
    pass


# ========================== SQLWindow Buttons ==========================
btn_sales_invoices = Button(SQLWindow, text="Sales invoices", width=15, height=2, command=view_sales_invoices)
btn_purchase_invoices = Button(SQLWindow, text="Purchase invoices", width=15, height=2, command=view_purchase_invoices)
btn_customers = Button(SQLWindow, text="Customers", width=15, height=2, command=view_customers)
btn_sellers = Button(SQLWindow, text="Sellers", width=15, height=2, command=view_sellers)

# ========================== SQLWindow ListBox And  Scrollbar ==========================
list1 = Listbox(SQLWindow, width=80, height=15, activestyle='none', bg='#F7FF99')
sb1 = Scrollbar(SQLWindow, width=20)
list1.configure(yscrollcommand=sb1.set)
sb1.configure(command=list1.yview)

# ==========================     Grids  objects =========================================
btn_sales_invoices.grid(row=1, column=1, padx=5, pady=10)
btn_purchase_invoices.grid(row=1, column=2, padx=5, pady=10)
btn_customers.grid(row=1, column=3, padx=5, pady=10)
btn_sellers.grid(row=1, column=4, padx=5, pady=10)

list1.grid(row=2, column=1, rowspan=6, columnspan=4, pady=10)
sb1.grid(row=2, column=5, rowspan=6, ipady=90)

# ==========================   Main Loop =========================================
SQLWindow.mainloop()
