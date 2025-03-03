import streamlit as st
import sqlite3

def init_login_db():
    conn = sqlite3.connect('pharmacy.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (username TEXT PRIMARY KEY,
                  password TEXT,
                  is_admin INTEGER)''')
    
    # Create default admin user
    c.execute("""
        INSERT OR IGNORE INTO users (username, password, is_admin) 
        VALUES ('admin', 'admin123', 1)
    """)
    conn.commit()
    conn.close()

def check_login(username, password):
    conn = sqlite3.connect('pharmacy.db')
    c = conn.cursor()
    result = c.execute("""
        SELECT * FROM users 
        WHERE username = ? AND password = ? AND is_admin = 1
    """, (username, password)).fetchone()
    conn.close()
    return result is not None

def login_page():
    st.markdown("""
        <style>
        .login-header {
            color: #4CAF50;
            text-align: center;
            margin-bottom: 30px;
            margin-top: 100px;  /* Added margin to move everything down */
            font-size: 2.5em;
        }
        .stButton > button {
            margin-top: 25px;  /* Added margin above the login button */
            background-color: #4CAF50;
            color: white;
            font-weight: bold;
            padding: 10px 25px;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<h1 class="login-header">Admin Login</h1>', unsafe_allow_html=True)
    
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    # Show credentials hint
    st.info("Username: admin, Password: admin123")
    
    if st.button("Login"):
        if check_login(username, password):
            st.session_state['logged_in'] = True
            st.success("Login successful!")
            st.rerun()
        else:
            st.error("Invalid username or password!")
    
    st.markdown('</div>', unsafe_allow_html=True) 