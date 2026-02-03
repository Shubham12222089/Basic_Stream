# streamlit_sales_app.py
import streamlit as st
import sqlite3
from fpdf import FPDF
from datetime import datetime
import io

DB = "sales.db"

# ---------- DB utils ----------
def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.executescript("""
    CREATE TABLE IF NOT EXISTS customers (
      id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, phone TEXT, email TEXT, address TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    CREATE TABLE IF NOT EXISTS products (
      id INTEGER PRIMARY KEY AUTOINCREMENT, sku TEXT, name TEXT, selling_price REAL, stock INTEGER DEFAULT 0
    );
    CREATE TABLE IF NOT EXISTS sales (
      id INTEGER PRIMARY KEY AUTOINCREMENT, invoice_no TEXT UNIQUE, customer_id INTEGER, date TIMESTAMP DEFAULT CURRENT_TIMESTAMP, subtotal REAL, tax REAL, total REAL
    );
    CREATE TABLE IF NOT EXISTS sale_items (
      id INTEGER PRIMARY KEY AUTOINCREMENT, sale_id INTEGER, product_id INTEGER, qty INTEGER, unit_price REAL, line_total REAL
    );
    """)
    conn.commit()
    conn.close()

def query(sql, params=()):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute(sql, params)
    rows = c.fetchall()
    conn.commit()
    conn.close()
    return rows

# ---------- Receipt PDF ----------
class Receipt(FPDF):
    def header(self):
        self.set_font("Arial", "B", 14)
        self.cell(0, 8, "Your Clinic / Store Name", ln=True, align="C")
        self.set_font("Arial", "", 10)
        self.cell(0, 6, "Address | Phone", ln=True, align="C")
        self.ln(4)

def generate_receipt_pdf(invoice_no, customer, items, subtotal, tax, total):
    pdf = Receipt()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", "", 11)
    pdf.cell(0, 6, f"Invoice: {invoice_no}", ln=True)
    pdf.cell(0, 6, f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}", ln=True)
    pdf.ln(4)
    pdf.cell(0, 6, f"Customer: {customer['name']}", ln=True)
    if customer.get('phone'):
        pdf.cell(0, 6, f"Phone: {customer['phone']}", ln=True)
    if customer.get('address'):
        pdf.multi_cell(0, 6, f"Address: {customer['address']}")
    pdf.ln(4)
    # table header
    pdf.set_font("Arial", "B", 10)
    pdf.cell(80, 6, "Product", border=1)
    pdf.cell(25, 6, "Qty", border=1, align="R")
    pdf.cell(30, 6, "Unit", border=1, align="R")
    pdf.cell(35, 6, "Total", border=1, align="R")
    pdf.ln()
    pdf.set_font("Arial", "", 10)
    for it in items:
        pdf.cell(80, 6, it['name'], border=1)
        pdf.cell(25, 6, str(it['qty']), border=1, align="R")
        pdf.cell(30, 6, f"{it['unit_price']:.2f}", border=1, align="R")
        pdf.cell(35, 6, f"{it['line_total']:.2f}", border=1, align="R")
        pdf.ln()
    pdf.ln(4)
    pdf.cell(135, 6, "Subtotal", align="R")
    pdf.cell(35, 6, f"{subtotal:.2f}", border=1, align="R"); pdf.ln()
    pdf.cell(135, 6, "Tax", align="R")
    pdf.cell(35, 6, f"{tax:.2f}", border=1, align="R"); pdf.ln()
    pdf.cell(135, 6, "Total", align="R")
    pdf.cell(35, 6, f"{total:.2f}", border=1, align="R"); pdf.ln(10)
    pdf.set_font("Arial", "I", 9)
    pdf.multi_cell(0, 5, "Thank you for your purchase!")
    # return bytes
    return pdf.output(dest='S').encode('latin1')

# ---------- Streamlit UI ----------
st.title("Simple Sales & Receipt System (MVP)")

init_db()

tab = st.sidebar.radio("Navigate", ["Customers", "Products", "Create Sale", "Sales History"])

if tab == "Customers":
    st.header("Customers")
    with st.form("add_cust", clear_on_submit=True):
        name = st.text_input("Name")
        phone = st.text_input("Phone")
        email = st.text_input("Email")
        address = st.text_area("Address")
        submitted = st.form_submit_button("Add Customer")
        if submitted:
            query("INSERT INTO customers(name,phone,email,address) VALUES (?,?,?,?)", (name,phone,email,address))
            st.success("Customer added")
    st.subheader("All customers")
    rows = query("SELECT id, name, phone, email FROM customers ORDER BY id DESC")
    for r in rows:
        st.write(f"{r[0]} - {r[1]} | {r[2]} | {r[3]}")

if tab == "Products":
    st.header("Products")
    with st.form("add_prod", clear_on_submit=True):
        sku = st.text_input("SKU")
        name = st.text_input("Product Name")
        price = st.number_input("Price", min_value=0.0, value=0.0, format="%.2f")
        stock = st.number_input("Stock", min_value=0, value=0)
        addp = st.form_submit_button("Add Product")
        if addp:
            query("INSERT INTO products(sku,name,selling_price,stock) VALUES (?,?,?,?)", (sku,name,price,stock))
            st.success("Product added")
    st.subheader("Catalog")
    rows = query("SELECT id, sku, name, selling_price, stock FROM products ORDER BY id DESC")
    for r in rows:
        st.write(f"{r[0]} - {r[2]} (SKU:{r[1]}) ₹{r[3]:.2f} | stock: {r[4]}")

if tab == "Create Sale":
    st.header("Create Sale / Invoice")
    customers = query("SELECT id, name FROM customers")
    products = query("SELECT id, name, selling_price FROM products")
    cust_map = {str(r[0]): r[1] for r in customers}
    prod_map = {str(r[0]): {'name':r[1],'price':r[2]} for r in products}

    if not customers:
        st.warning("Add customers first.")
    if not products:
        st.warning("Add products first.")

    cust_choice = st.selectbox("Customer", options=["-- Select --"] + [f"{r[0]}: {r[1]}" for r in customers])
    num_items = st.number_input("Number of line items", min_value=1, max_value=10, value=1)
    items = []
    for i in range(num_items):
        col1, col2, col3 = st.columns([4,1,1])
        prod_sel = col1.selectbox(f"Product {i+1}", options=["--"] + [f"{r[0]}: {r[1]} (₹{r[2]:.2f})" for r in products], key=f"prod_{i}")
        qty = col2.number_input("Qty", min_value=0, value=1, key=f"qty_{i}")
        price_override = col3.number_input("Unit Price", value=0.0, format="%.2f", key=f"price_{i}")
        if prod_sel != "--" and qty > 0:
            pid = int(prod_sel.split(":")[0])
            pname = prod_map[str(pid)]['name']
            unit_price = price_override if price_override>0 else prod_map[str(pid)]['price']
            items.append({'product_id': pid, 'name':pname, 'qty': qty, 'unit_price': unit_price, 'line_total': unit_price*qty})

    if st.button("Create Invoice & Generate Receipt") and items and cust_choice != "-- Select --":
        invoice_no = f"INV{int(datetime.now().timestamp())}"
        cust_id = int(cust_choice.split(":")[0])
        subtotal = sum([it['line_total'] for it in items])
        tax = 0.0
        total = subtotal + tax
        # insert sale
        query("INSERT INTO sales (invoice_no, customer_id, subtotal, tax, total) VALUES (?, ?, ?, ?, ?)",
              (invoice_no, cust_id, subtotal, tax, total))
        sale_id = query("SELECT id FROM sales WHERE invoice_no = ?", (invoice_no,))[0][0]
        for it in items:
            query("INSERT INTO sale_items (sale_id, product_id, qty, unit_price, line_total) VALUES (?, ?, ?, ?, ?)",
                  (sale_id, it['product_id'], it['qty'], it['unit_price'], it['line_total']))
        st.success(f"Invoice {invoice_no} saved")
        # get customer details
        c = query("SELECT name, phone, address FROM customers WHERE id = ?", (cust_id,))[0]
        cust = {'name': c[0], 'phone': c[1], 'address': c[2]}
        pdf_bytes = generate_receipt_pdf(invoice_no, cust, items, subtotal, tax, total)
        st.download_button("Download Receipt (PDF)", data=pdf_bytes, file_name=f"{invoice_no}.pdf", mime="application/pdf")
        st.button("Open Print Dialog", on_click=lambda: st.write("Open the downloaded PDF in browser and press Ctrl+P / Print."))

if tab == "Sales History":
    st.header("Sales History")
    rows = query("SELECT s.id, invoice_no, date, subtotal, total, c.name FROM sales s LEFT JOIN customers c ON s.customer_id = c.id ORDER BY s.date DESC LIMIT 50")
    for r in rows:
        st.write(f"{r[1]} | {r[2]} | {r[5]} | ₹{r[4]:.2f}")
