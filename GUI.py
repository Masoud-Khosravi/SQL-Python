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
btn_add_Sell = Button(SQLWindow, text="Add Sell", width=15, height=2, command=lambda: new_window(False))
btn_add_Buy = Button(SQLWindow, text="Add Buy", width=15, height=2, command=lambda: new_window(True))

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


# ========================== SQL_New_Window Setting =======================
def new_window(is_buy=False):
    new_win = Toplevel(SQLWindow)
    new_win.geometry("850x280")
    s = Style()
    s.theme_use('clam')

    new_win.resizable(width=False, height=False)

    users = []
    user_id = []
    if is_buy:
        new_win.title("New Buy")
        text_lbl = "Select the seller"
        result = sql_commands.view_sellers()
    else:
        new_win.title("New Sell")
        text_lbl = "Select the customer"
        result = sql_commands.view_customers()
    for s in result:
        user_id.append(s[0])
        users.append(s[1])

    # ===================== Commands functions =============================
    def clear_list_invoice():
        for item in list_invoice.get_children():
            list_invoice.delete(item)
        calculate_sum()
        default_values()

    def fill_list_invoice():
        item = [ware_index, All_wares.get(), All_brands.get(), All_categories.get(), ent_values.get(), ent_price.get()]
        list_invoice.insert('', 'end', values=item)
        All_brands.current(0)
        All_categories.current(0)
        All_wares.set("")
        All_wares.config(state="disabled")
        btn_add_to_list.config(state="disabled")
        ent_values.delete(0, END)
        ent_price.delete(0, END)
        All_users.config(state="disabled")
        btn_save.config(state="normal")
        btn_clear_list.config(state="normal")
        calculate_sum()

    def default_values():
        ent_values.delete(0, END)
        ent_price.delete(0, END)
        All_users.config(state="readonly")
        btn_save.config(state="disabled")
        btn_add_to_list.config(state="disabled")
        btn_clear_list.config(state="disabled")
        All_wares.config(state="disabled")
        All_wares.set("")
        All_brands.current(0)
        All_categories.current(0)
        All_users.current(0)

    def save_fuc():
        Now = time.strftime('%Y-%m-%d %H:%M:%S')
        if is_buy:
            # print("Buy")
            invoice_id = sql_commands.add_buy(user_index, ent_sum.get(), Now)
            if invoice_id > 0:
                for child in list_invoice.get_children():
                    item = list_invoice.item(child)["values"]
                    ware_id = int(item[0])
                    value = int(item[4])
                    price = float(item[5])
                    sql_commands.add_buy_details(invoice_id, ware_id, value, price)
        else:
            # print("Sell")
            invoice_id = sql_commands.add_sale(user_index, ent_sum.get(), Now)
            if invoice_id > 0:
                for child in list_invoice.get_children():
                    item = list_invoice.item(child)["values"]
                    ware_id = int(item[0])
                    value = int(item[4])
                    price = float(item[5])
                    sql_commands.add_sale_details(invoice_id, ware_id, value, price)
        messagebox.showinfo(message=f'All Data Saved -> time:{Now} , ID: {invoice_id}')
        new_win.destroy()

    def calculate_sum():
        sum_vals = 0
        for child in list_invoice.get_children():
            item = list_invoice.item(child)["values"]
            value = int(item[4])
            price = float(item[5])
            sum_vals += value * price
        sum_vals = str(sum_vals)
        ent_sum.config(state="normal")
        ent_sum.delete(0, END)  # this will delete everything inside the entry
        ent_sum.insert(END, sum_vals)
        ent_sum.config(state="readonly")

    # =======================  Labels ============================================
    lbl_user = Label(new_win, text=text_lbl, font=("Times New Roman", 12))
    lbl_catq = Label(new_win, text='Select The Categories', font=("Times New Roman", 12))
    lbl_brands = Label(new_win, text='Select The Brands', font=("Times New Roman", 12))
    lbl_wares = Label(new_win, text='Select The ware', font=("Times New Roman", 12))
    lbl_vals = Label(new_win, text='How many : ', font=("Times New Roman", 12))
    lbl_price = Label(new_win, text='Enter The Price', font=("Times New Roman", 12))
    lbl_sum = Label(new_win, text='SUM :', font=("Times New Roman", 12))

    # ================================ Combo boxes==========================================
    user = StringVar()
    All_users = Combobox(new_win, width=15, textvariable=user, state='readonly')
    All_users['values'] = users

    categories = []
    categories_id = []
    res = sql_commands.view_categories()
    for s in res:
        categories_id.append(s[0])
        categories.append(s[1])
    cat = StringVar()
    All_categories = Combobox(new_win, width=15, textvariable=cat, values=categories, state='readonly')

    brands = []
    brands_id = []
    res = sql_commands.view_brands()
    for s in res:
        brands_id.append(s[0])
        brands.append(s[1])
    brand = StringVar()
    All_brands = Combobox(new_win, width=15, textvariable=brand, state='readonly')
    All_brands['values'] = brands

    ware = StringVar()
    All_wares = Combobox(new_win, width=15, textvariable=ware, state='readonly')

    # =================== Entries ==========================================
    txt_values = StringVar()
    ent_values = Entry(new_win, textvariable=txt_values)

    txt_sum = StringVar()
    ent_sum = Entry(new_win, textvariable=txt_sum)

    txt_price = StringVar()
    ent_price = Entry(new_win, textvariable=txt_price)

    # ==========================  Buttons ==========================
    btn_add_to_list = Button(new_win, text="Add To List ->", width=12, height=1, font=("Times New Roman", 12),
                             foreground="green", activeforeground="red", activebackground="white",
                             command=fill_list_invoice)

    btn_clear_list = Button(new_win, text=" < Clear List >", width=12, height=1, font=("Times New Roman", 12),
                            command=clear_list_invoice)

    btn_save = Button(new_win, text="Save All", width=12, height=1, font=("Times New Roman", 12),
                      foreground="black", activeforeground="red", activebackground="yellow", bg="#77CA00",
                      command=save_fuc)
    # ====================== List Boxes / TreeViews ====================================
    # Add a Treeview widget
    list_invoice = Treeview(new_win, column=("c1", "c2", "c3", "c4", "c5", "c6"), show='headings', height=8)

    list_invoice.column("c1", width=25)
    list_invoice.heading("c1", text="ID")
    list_invoice.column("c2", width=80, anchor=CENTER)
    list_invoice.heading("c2", text="Name")
    list_invoice.column("c3", width=80, anchor=CENTER)
    list_invoice.heading("c3", text="Brand")
    list_invoice.column("c4", width=80, anchor=CENTER)
    list_invoice.heading("c4", text="Categories")
    list_invoice.column("c5", width=60, anchor=CENTER)
    list_invoice.heading("c5", text="Value")
    list_invoice.column("c6", width=80, anchor=CENTER)
    list_invoice.heading("c6", text="Price")

    sb_invoice = Scrollbar(new_win, width=20)
    list_invoice.configure(yscrollcommand=sb_invoice.set)
    sb_invoice.configure(command=list_invoice.yview)
    # =================== Grids  ==========================================
    lbl_user.grid(row=1, column=1, pady=5)
    All_users.grid(row=1, column=2, pady=5)
    lbl_catq.grid(row=2, column=1, pady=5)
    All_categories.grid(row=2, column=2, pady=5)
    lbl_brands.grid(row=3, column=1, pady=5)
    All_brands.grid(row=3, column=2, pady=5)
    lbl_wares.grid(row=4, column=1, pady=5)
    All_wares.grid(row=4, column=2, pady=5)
    lbl_vals.grid(row=5, column=1, pady=5)
    ent_values.grid(row=5, column=2, pady=5)
    lbl_price.grid(row=6, column=1, pady=5)
    ent_price.grid(row=6, column=2, pady=5)
    lbl_sum.grid(row=6, column=4, pady=5)
    ent_sum.grid(row=6, column=5, pady=5)

    btn_add_to_list.grid(row=5, column=3, pady=5, padx=10)
    btn_clear_list.grid(row=3, column=3, pady=5, padx=10)
    btn_save.grid(row=6, column=6, pady=5, padx=10)

    list_invoice.grid(row=1, column=4, rowspan=5, columnspan=4, pady=5)
    sb_invoice.grid(row=1, column=8, rowspan=5, ipady=60)

    btn_save.config(state="disabled")
    btn_add_to_list.config(state="disabled")
    btn_clear_list.config(state="disabled")
    All_wares.config(state="disabled")
    ent_sum.config(state="readonly")

    # ===================== event functions ==============================
    def changed_users(event):
        global user_index
        selected_user = All_users.get()
        user_selected = users.index(selected_user)
        user_index = user_id[user_selected]

    def changed_wares(event):
        global ware_index
        selected_ware = All_wares.get()
        ware_selected = wares.index(selected_ware)
        ware_index = wares_id[ware_selected]
        btn_add_to_list.config(state="normal")
        price = str(sql_commands.get_sell_price(ware_index))
        ent_price.delete(0, END)  # this will delete everything inside the entry
        ent_price.insert(END, price)

    def changed_combos(event):
        selected_cat = All_categories.get()
        selected_brand = All_brands.get()
        counter = 0
        global cat_index, brand_index
        if len(selected_cat) > 0:
            counter += 1
            cat_selected = categories.index(selected_cat)
            cat_index = categories_id[cat_selected]
        else:
            cat_index = None

        if len(selected_brand) > 0:
            counter += 1
            brand_selected = brands.index(selected_brand)
            brand_index = brands_id[brand_selected]
        else:
            brand_index = None
        # print(selected_cat, " ", cat_index, " ", categories_id[cat_index])
        if counter == 2:
            # print(brand_index, " ", cat_index)
            result = sql_commands.view_wares(brand_index, cat_index)
            global wares_id, wares, ware_index
            wares = []
            wares_id = []
            for any_res in result:
                wares_id.append(any_res[0])
                wares.append(any_res[1])
            All_wares['values'] = wares
            if len(wares) > 0:
                All_wares.current(0)
                All_wares.config(state="readonly")
                ware_index = wares_id[0]
                btn_add_to_list.config(state="normal")
                price = str(sql_commands.get_sell_price(ware_index))
                ent_price.delete(0, END)  # this will delete everything inside the entry
                ent_price.insert(END, price)
            else:
                All_wares.set("")
                ware_index = None
                All_wares.config(state="disabled")
                btn_add_to_list.config(state="disabled")
                ent_price.delete(0, END)  # this will delete everything inside the entry
                ent_price.insert(END, "")
        else:
            All_wares.config(state="disabled")

    # ====================== Binds =======================================
    All_categories.bind('<<ComboboxSelected>>', changed_combos)
    All_brands.bind('<<ComboboxSelected>>', changed_combos)
    All_wares.bind('<<ComboboxSelected>>', changed_wares)
    All_users.bind('<<ComboboxSelected>>', changed_users)

    default_values()
    new_win.wait_window()


# ==========================   Main Loop =========================================
SQLWindow.mainloop()
