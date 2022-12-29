import pyodbc

DRV = '{SQL Server}'
SRV = '(local)'
DB = 'Test_Sale_DB'


# ================================ Get All Customers by A view Called V_Customers ======================================
def view_customers():
    conn = pyodbc.connect('DRIVER={};Server={};Database={}; Trusted_Connection=yes;'.format(DRV, SRV, DB))
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM V_Customers")  # V_Customers is A view
    rows = cursor.fetchall()
    conn.close()
    return rows


# ================================ Get All Sellers From Users Table ======================================
def view_sellers():
    conn = pyodbc.connect('DRIVER={};Server={};Database={}; Trusted_Connection=yes;'.format(DRV, SRV, DB))
    cursor = conn.cursor()
    cursor.execute("SELECT ID,Name,Family,Sex,Address FROM Users WHERE Is_Seller=1")
    rows = cursor.fetchall()
    conn.close()
    return rows


# ================================ Get All items From Categories Table ======================================
def view_categories():
    conn = pyodbc.connect('DRIVER={};Server={};Database={}; Trusted_Connection=yes;'.format(DRV, SRV, DB))
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Categories")
    rows = cursor.fetchall()
    conn.close()
    return rows


# ================================ Get All items From Brands Table ======================================
def view_brands():
    conn = pyodbc.connect('DRIVER={};Server={};Database={}; Trusted_Connection=yes;'.format(DRV, SRV, DB))
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Brands")
    rows = cursor.fetchall()
    conn.close()
    return rows


# ======== Get All items From Sells Table And join With Users To Find Out Customers Name ====================
def view_sells():
    conn = pyodbc.connect('DRIVER={};Server={};Database={}; Trusted_Connection=yes;'.format(DRV, SRV, DB))
    cursor = conn.cursor()
    query = "SELECT S.ID,S.Total_amount,U.Name + ' ' + U.Family As FullName ,S.Date FROM" \
            " Sales S INNER JOIN Users U ON S.User_ID = U.ID"
    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()
    return rows


# ================================ Get All items From Buys Table ======================================
def view_buys():
    conn = pyodbc.connect('DRIVER={};Server={};Database={}; Trusted_Connection=yes;'.format(DRV, SRV, DB))
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Buys")
    rows = cursor.fetchall()
    conn.close()
    return rows


# ================================ Get Default Sell Price From Wares Table ======================================
def get_sell_price(ware_id):
    conn = pyodbc.connect('DRIVER={};Server={};Database={}; Trusted_Connection=yes;'.format(DRV, SRV, DB))
    cursor = conn.cursor()
    query = "SELECT Sell_Price FROM Wares WHERE ID={}".format(ware_id)
    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()
    if len(rows) > 0:
        rows = rows[0][0]
    else:
        rows = 0
    return rows


# ============================ Get All items From WAres Table By brand_ID and Categories_Id ====================
def view_wares(brand_id, category_id):
    conn = pyodbc.connect('DRIVER={};Server={};Database={}; Trusted_Connection=yes;'.format(DRV, SRV, DB))
    cursor = conn.cursor()
    query = "SELECT * FROM Wares WHERE Brand_ID={} AND Category_ID={}".format(brand_id, category_id)
    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()
    return rows


# ============================ We Made A Function To Execute Any Stored Procedure ====================
# We just have to give it the name of the Stored Procedure And arguments
def exec_query(sp_name, **kwargs):
    params = ''
    for key, value in kwargs.items():
        if type(value) is str:
            params += "@" + key + "='" + value + "', "
        else:
            params += "@" + key + "=" + str(value) + ", "

    params = params[:-2]  # Delete Last --> ", "
    conn = pyodbc.connect('DRIVER={};Server={};Database={}; Trusted_Connection=yes;'.format(DRV, SRV, DB))
    cursor = conn.cursor()
    query = "EXEC {} {} ".format(sp_name, params)
    next_cursor = cursor.execute(query)
    rows = []
    while next_cursor:  # To Get OUTPUT if stored procedures had any output
        try:
            row_c = cursor.fetchone()
            while row_c:
                rows.append(row_c)
                row_c = cursor.fetchone()
        except pyodbc.ProgrammingError:
            next_cursor = cursor.nextset()
            continue
        next_cursor = cursor.nextset()

    cursor.commit()
    conn.close()
    return rows


# ============= We Call  USP_ADD_USER Stored Procedure And Execute it By Last Function in the Upper part =============
def add_user(name, family, sex, address, is_seller=0, phone=""):
    exec_query('USP_ADD_USER', Name=name, Family=family, Sex=sex, Address=address, Is_Seller=is_seller, Phone=phone)


# ============= Call  USP_ADD_BUY Stored Procedure And  we also get the output (Buy_ID) =====================
def add_buy(user_id, total_amount, date):
    res = exec_query('USP_ADD_BUY', User_ID=user_id, Total_amount=total_amount, Date=date)
    if len(res) > 0:
        res = res[0][0]  # this is SALE_ID
    return res


# ============= Call  USP_ADD_SALE Stored Procedure And  we also get the output (Sale_ID) =====================
def add_sale(user_id, total_amount, date):
    res = exec_query('USP_ADD_SALE', User_ID=user_id, Total_amount=total_amount, Date=date)
    if len(res) > 0:
        res = res[0][0]  # this is SALE_ID
    return res


# ============= Call  USP_ADD_BUY_DETAILS Stored Procedure to Adding purchase invoices  =====================
def add_buy_details(id_buy, ware_id, value, price):
    exec_query('USP_ADD_BUY_DETAILS', ID_Buy=id_buy, Ware_ID=ware_id, Value=value, Price=price)


# ============= Call  USP_ADD_SALE_DETAILS Stored Procedure to Adding Sell invoices  =====================
def add_sale_details(id_sale, ware_id, value, sale_price):
    exec_query('USP_ADD_SALE_DETAILS', ID_Sale=id_sale, Ware_ID=ware_id, Value=value, Sale_Price=sale_price)
