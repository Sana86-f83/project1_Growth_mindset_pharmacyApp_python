import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime
import plotly.express as px
from login import init_login_db, login_page
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
import io

# Page configuration
st.set_page_config(
    page_title="Pharmacy Management System",
    page_icon="💊",
    layout="wide"
)

# Add this enhanced CSS at the start of your file
st.markdown("""
    <style>
    /* Main theme with animations */
    @keyframes gradientBG {
        0% { background-position: 0% 50% }
        50% { background-position: 100% 50% }
        100% { background-position: 0% 50% }
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-20px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .main {
        background-color: #1E1E1E;
        color: white;
        padding: 0 !important;
    }
    
    /* Enhanced Header styling */
    .main-header {
        color: #00E676;
        text-align: center;
        font-size: 2.8em;
        padding: 25px;
        font-weight: bold;
        text-shadow: 0 0 10px rgba(0,230,118,0.5);
        animation: fadeIn 1.5s ease-out;
    }
    
    /* Enhanced Navigation tabs */
    .stTabs {
        animation: fadeIn 1s ease-out;
    }
    
    .stTab {
        background: linear-gradient(45deg, #00C853, #00E676);
        background-size: 200% 200%;
        animation: gradientBG 3s ease infinite;
        transition: all 0.3s ease;
    }
    
    .stTab:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 10px rgba(0,230,118,0.3);
    }
    
    /* Enhanced Button styling */
    .stButton > button {
        background: linear-gradient(45deg, #00C853, #00E676) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 12px 24px !important;
        font-weight: bold !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 2px 5px rgba(0,0,0,0.2) !important;
        animation: fadeIn 0.5s ease-out;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 15px rgba(0,230,118,0.4) !important;
    }
    
    /* Enhanced Input fields */
    .stTextInput > div > div,
    .stNumberInput > div > div,
    .stSelectbox > div > div {
        background-color: #2D2D2D !important;
        border: 2px solid #00E676 !important;
        border-radius: 8px !important;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div:hover,
    .stNumberInput > div > div:hover,
    .stSelectbox > div > div:hover {
        border-color: #00E676 !important;
        box-shadow: 0 0 10px rgba(0,230,118,0.2) !important;
    }
    
    /* Enhanced Table styling */
    [data-testid="stDataFrame"] {
        background-color: #2D2D2D !important;
        border-radius: 10px !important;
        overflow: hidden !important;
        animation: fadeIn 1s ease-out;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2) !important;
    }
    
    [data-testid="stDataFrame"] th {
        background: linear-gradient(45deg, #00C853, #00E676) !important;
        color: white !important;
        font-weight: bold !important;
        text-align: center !important;
        padding: 12px !important;
    }
    
    [data-testid="stDataFrame"] td {
        color: white !important;
        text-align: center !important;
        padding: 10px !important;
        border-bottom: 1px solid rgba(0,230,118,0.1) !important;
    }
    
    /* Status colors with glow effect */
    .status-in-stock {
        color: #00E676 !important;
        text-shadow: 0 0 5px rgba(0,230,118,0.3) !important;
    }
    
    .status-low-stock {
        color: #FFC107 !important;
        text-shadow: 0 0 5px rgba(255,193,7,0.3) !important;
    }
    
    .status-out-of-stock {
        color: #FF5252 !important;
        text-shadow: 0 0 5px rgba(255,82,82,0.3) !important;
    }
    
    /* Enhanced Charts */
    .js-plotly-plot {
        animation: fadeIn 1s ease-out;
        border-radius: 10px !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2) !important;
    }
    
    /* Enhanced Footer */
    .footer {
        text-align: center;
        padding: 20px;
        color: #00E676;
        font-size: 18px;
        margin-top: 30px;
        font-style: italic;
        animation: fadeIn 1s ease-out;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize login system
init_login_db()

# Check if user is logged in
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if not st.session_state['logged_in']:
    login_page()
else:
    # Main Header with small logout icon
    col1, col2 = st.columns([15, 1])  # Changed ratio to make logout smaller
    with col1:
        st.markdown("""
            <h1 class="main-header" style="
                font-size: 3.5em;  /* Increased font size */
                font-weight: bold;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
                padding: 30px 0;  /* Added more padding */
                margin-bottom: 30px;
            ">💊 Pharmacy Management System 💊</h1>
        """, unsafe_allow_html=True)
    with col2:
        if st.button("🔓"):  # Changed to a better looking lock icon
            st.session_state['logged_in'] = False
            st.rerun()

    # Database initialization
    def init_db():
        conn = sqlite3.connect('pharmacy.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS medicines
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      name TEXT NOT NULL,
                      manufacturer TEXT,
                      price REAL,
                      quantity INTEGER,
                      category TEXT)''')
        
        # Create sales table
        c.execute('''CREATE TABLE IF NOT EXISTS sales
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      medicine_id INTEGER,
                      quantity INTEGER,
                      total_price REAL,
                      sale_date DATE,
                      FOREIGN KEY (medicine_id) REFERENCES medicines(id))''')
        conn.commit()
        conn.close()

    init_db()

    # Update the navigation section with working tabs
    tabs = st.tabs(["📋 Manage Products", "💰 Sales", "📊 Analytics", "🔍 Search"])

    # Products Tab (Your existing code goes here)
    with tabs[0]:
        st.subheader("Add/Update Product")

        col1, col2, col3 = st.columns(3)

        with col1:
            name = st.text_input("Product Name")
            manufacturer = st.text_input("Manufacturer")

        with col2:
            price = st.number_input("Price (Rs.)", min_value=0.0, step=0.5)
            quantity = st.number_input("Quantity", min_value=0)

        with col3:
            category = st.selectbox("Category", ["Pain Relief", "Antibiotics", "Gastric", "Other"])

        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("➕ Add Product"):
                conn = sqlite3.connect('pharmacy.db')
                c = conn.cursor()
                c.execute("""
                    INSERT INTO medicines (name, manufacturer, price, quantity, category)
                    VALUES (?, ?, ?, ?, ?)
                """, (name, manufacturer, price, quantity, category))
                conn.commit()
                conn.close()
                st.success("✅ Product added successfully!")
                st.rerun()

        with col2:
            if st.button("🔄 Update Product"):
                conn = sqlite3.connect('pharmacy.db')
                c = conn.cursor()
                c.execute("""
                    UPDATE medicines 
                    SET manufacturer=?, price=?, quantity=?, category=?
                    WHERE name=?
                """, (manufacturer, price, quantity, category, name))
                conn.commit()
                conn.close()
                st.success("✅ Product updated successfully!")
                st.rerun()

        with col3:
            if st.button("❌ Delete Product"):
                conn = sqlite3.connect('pharmacy.db')
                c = conn.cursor()
                c.execute("DELETE FROM medicines WHERE name=?", (name,))
                conn.commit()
                conn.close()
                st.success("✅ Product deleted successfully!")
                st.rerun()

        # Current Inventory
        st.subheader("Current Inventory")
        conn = sqlite3.connect('pharmacy.db')
        inventory = pd.read_sql_query("""
            SELECT 
                printf('%03d', id) as 'ID',  /* Format ID with leading zeros */
                name as 'Product Name',
                manufacturer as Manufacturer,
                printf('Rs. %.2f', price) as 'Price (Rs.)',
                printf('%d', quantity) as 'Quantity',  /* Format quantity as plain number */
                category as Category,
                CASE 
                    WHEN quantity > 10 THEN 'In Stock'
                    WHEN quantity > 0 THEN 'Low Stock'
                    ELSE 'Out of Stock'
                END as Status
            FROM medicines
            ORDER BY name
        """, conn)
        conn.close()

        # Apply custom formatting to the Status column
        def color_status(val):
            if val == "In Stock":
                return 'color: #4CAF50; font-weight: bold'
            elif val == "Low Stock":
                return 'color: #ffa726; font-weight: bold'
            else:
                return 'color: #ef5350; font-weight: bold'

        styled_inventory = inventory.style\
            .applymap(color_status, subset=['Status'])\
            .set_properties(subset=['ID', 'Quantity'], **{'text-align': 'center'})\
            .set_properties(
                subset=['ID'],
                **{
                    'text-align': 'center',
                    'background-color': 'rgba(70, 130, 180, 0.1)',  # Light steel blue
                    'font-weight': 'bold',
                    'color': '#4682B4'  # Steel blue
                }
            )
        st.dataframe(styled_inventory, use_container_width=True)

        # Create PDF button
        def convert_df_to_pdf():
            buffer = io.BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=letter)
            elements = []
            
            # Convert DataFrame to list for PDF table
            data = [inventory.columns.tolist()] + inventory.values.tolist()
            
            # Create table
            table = Table(data)
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 14),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 12),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ]))
            
            elements.append(table)
            doc.build(elements)
            
            pdf = buffer.getvalue()
            buffer.close()
            return pdf

        # After the inventory dataframe display
        st.write("")  # Add some space
        st.write("Download Inventory:")  # Add a label
        st.download_button(
            label="📥 Download as CSV",
            data=inventory.to_csv(index=False),
            file_name="pharmacy_inventory.csv",
            mime="text/csv"
        )
        st.download_button(
            label="📥 Download as PDF",
            data=convert_df_to_pdf(),
            file_name="pharmacy_inventory.pdf",
            mime="application/pdf"
        )

    # Sales Tab
    with tabs[1]:
        st.subheader("Sales Management")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Make a sale
            st.write("Make New Sale")
            conn = sqlite3.connect('pharmacy.db')
            medicines = pd.read_sql_query("SELECT id, name, price, quantity FROM medicines WHERE quantity > 0", conn)
            
            selected_medicine = st.selectbox("Select Medicine", medicines['name'].tolist())
            med_data = medicines[medicines['name'] == selected_medicine].iloc[0]
            
            sale_quantity = st.number_input("Quantity", min_value=1, max_value=int(med_data['quantity']))
            total_price = sale_quantity * med_data['price']
            
            if st.button("Complete Sale"):
                c = conn.cursor()
                # Record sale
                c.execute("""
                    INSERT INTO sales (medicine_id, quantity, total_price, sale_date)
                    VALUES (?, ?, ?, date('now'))
                """, (med_data['id'], sale_quantity, total_price))
                
                # Update stock
                c.execute("""
                    UPDATE medicines 
                    SET quantity = quantity - ?
                    WHERE id = ?
                """, (sale_quantity, med_data['id']))
                
                conn.commit()
                st.success(f"Sale completed! Total: Rs. {total_price:.2f}")
            
            conn.close()
        
        with col2:
            # Recent sales
            st.write("Recent Sales")
            conn = sqlite3.connect('pharmacy.db')
            recent_sales = pd.read_sql_query("""
                SELECT 
                    m.name as 'Medicine',
                    s.quantity as 'Quantity',
                    s.total_price as 'Total',
                    s.sale_date as 'Date'
                FROM sales s
                JOIN medicines m ON s.medicine_id = m.id
                ORDER BY s.sale_date DESC
                LIMIT 5
            """, conn)
            st.dataframe(recent_sales, use_container_width=True)
            conn.close()

    # Analytics Tab
    with tabs[2]:
        st.subheader("Analytics Dashboard")
        
        # Create new database connection for analytics
        conn = sqlite3.connect('pharmacy.db')
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Products by Category Pie Chart
            category_data = pd.read_sql_query("""
                SELECT 
                    category as Category,
                    COUNT(*) as Count,
                    (COUNT(*) * 100.0 / (SELECT COUNT(*) FROM medicines)) as Percentage
                FROM medicines
                GROUP BY category
            """, conn)
            
            fig1 = px.pie(
                category_data, 
                values='Count', 
                names='Category',
                title="Products by Category",
                hole=0.3,  # Makes it a donut chart
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            
            fig1.update_traces(
                textposition='inside',
                textinfo='percent+label',
                textfont=dict(size=14, color='black')
            )
            
            fig1.update_layout(
                title={
                    'text': "Products by Category",
                    'y':0.95,
                    'x':0.5,
                    'xanchor': 'center',
                    'yanchor': 'top',
                    'font': dict(size=24, color='#4CAF50')
                },
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(size=14),
                showlegend=True,
                legend=dict(
                    title="Categories",
                    bgcolor='rgba(0,0,0,0)',
                    font=dict(size=12)
                ),
                margin=dict(t=100, l=20, r=20, b=20)
            )
            
            st.plotly_chart(fig1, use_container_width=True)

        with col2:
            # Daily Sales by Product Bar Chart
            daily_sales = pd.read_sql_query("""
                SELECT 
                    m.name as product_name,
                    s.sale_date,
                    SUM(s.quantity) as total_sold
                FROM sales s
                JOIN medicines m ON s.medicine_id = m.id
                GROUP BY m.name, s.sale_date
                ORDER BY s.sale_date DESC
                LIMIT 10
            """, conn)
            
            fig2 = px.bar(
                daily_sales,
                x='sale_date',
                y='total_sold',
                color='product_name',
                title="Daily Sales by Product",
                labels={'total_sold': 'Units Sold', 'sale_date': 'Sale Date', 'product_name': 'Product'},
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            
            fig2.update_layout(
                barmode='group',
                title={
                    'text': "Daily Sales by Product",
                    'y':0.95,
                    'x':0.5,
                    'xanchor': 'center',
                    'yanchor': 'top',
                    'font': dict(size=24, color='#4CAF50')
                },
                xaxis_title="Sale Date",
                yaxis_title="Units Sold",
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(size=14),
                showlegend=True,
                legend=dict(
                    title="Products",
                    bgcolor='rgba(0,0,0,0)',
                    font=dict(size=12),
                    yanchor="top",
                    y=0.99,
                    xanchor="right",
                    x=0.99
                ),
                xaxis=dict(
                    showgrid=True,
                    gridwidth=1,
                    gridcolor='rgba(128, 128, 128, 0.2)',
                    tickfont=dict(size=12)
                ),
                yaxis=dict(
                    showgrid=True,
                    gridwidth=1,
                    gridcolor='rgba(128, 128, 128, 0.2)',
                    tickfont=dict(size=12)
                ),
                margin=dict(t=100, l=80, r=80, b=80)
            )

            # Add hover template
            fig2.update_traces(
                hovertemplate="<b>%{x}</b><br>" +
                             "Product: %{customdata}<br>" +
                             "Units Sold: %{y}<extra></extra>",
                customdata=daily_sales['product_name']
            )

            st.plotly_chart(fig2, use_container_width=True)

        # Remove the CSS for background colors
        st.markdown("""
            <style>
            [data-testid="stHorizontalBlock"] {
                padding: 20px;
                border-radius: 10px;
                margin-bottom: 20px;
            }
            </style>
        """, unsafe_allow_html=True)

        # Close the database connection
        conn.close()

    # Search Tab
    with tabs[3]:
        st.subheader("Search Products")
        
        search_term = st.text_input("🔍 Search by medicine name or manufacturer")
        
        if search_term:
            conn = sqlite3.connect('pharmacy.db')
            results = pd.read_sql_query(f"""
                SELECT 
                    name as 'Medicine Name',
                    manufacturer as Manufacturer,
                    printf('Rs. %.2f', price) as Price,
                    quantity as Stock,
                    category as Category,
                    CASE 
                        WHEN quantity > 10 THEN 'In Stock'
                        WHEN quantity > 0 THEN 'Low Stock'
                        ELSE 'Out of Stock'
                    END as Status
                FROM medicines
                WHERE name LIKE '%{search_term}%'
                OR manufacturer LIKE '%{search_term}%'
            """, conn)
            
            if not results.empty:
                st.dataframe(results.style.applymap(color_status, subset=['Status']), 
                            use_container_width=True)
            else:
                st.info("No products found matching your search.")
            
            conn.close()
            
    st.markdown("--------------------------------")        

    # Simple one-line footer
    st.markdown("""
        <div style='
            text-align: center;
            padding: 15px;
            color: white;
            font-size: 20px;
            margin-top: 30px;
        '>
            © 2025 Pharmacy Management System | Developed by<p style = 'color: #00E676'>Sana Faisal </p>
        </div>
    """, unsafe_allow_html=True) 