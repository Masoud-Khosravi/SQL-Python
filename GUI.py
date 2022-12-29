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
    list1.delete(0, END)


def fill_list1(items):
    for item in items:
        list1.insert(END, item)


def view_sales_invoices():
    clear_list1()
    sales = sql_commands.view_sells()
    fill_list1(sales)


def view_purchase_invoices():
    clear_list1()
    buys = sql_commands.view_buys()
    fill_list1(buys)


def view_customers():
    clear_list1()
    customers = sql_commands.view_customers()
    fill_list1(customers)


def view_sellers():
    clear_list1()
    sellers = sql_commands.view_sellers()
    fill_list1(sellers)


# ========================== SQLWindow Buttons ==========================
btn_sales_invoices = Button(SQLWindow, text="Sales invoices", width=15, height=2, command=view_sales_invoices)
btn_purchase_invoices = Button(SQLWindow, text="Purchase invoices", width=15, height=2, command=view_purchase_invoices)
btn_customers = Button(SQLWindow, text="Customers", width=15, height=2, command=view_customers)
btn_sellers = Button(SQLWindow, text="Sellers", width=15, height=2, command=view_sellers)
btn_add_Sell = Button(SQLWindow, text="Add Sell", width=15, height=2)
btn_add_Buy = Button(SQLWindow, text="Add Buy", width=15, height=2)

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

btn_add_Sell.grid(row=2, column=7, padx=5)
btn_add_Buy.grid(row=3, column=7, padx=5)

# ==========================   Main Loop =========================================
SQLWindow.mainloop()
