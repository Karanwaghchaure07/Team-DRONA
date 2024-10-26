import streamlit as st
import json
import os
import bcrypt

# Set the page configuration
st.set_page_config(page_title="Admin Login", page_icon="💬")

# Custom CSS for styling
st.markdown(
    """
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: "Poppins", sans-serif;
        }
        body {
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            background: url("https://wallpaperbat.com/img/902969-southwest-missouris-event-planning-guide.jpg");
            background-size: cover;
            background-position: center;
        }
        .wrapper {
            width: 420px;
            background: rgba(255, 255, 255, .1);
            border: 2px solid rgba(255, 255, 255, .2);
            backdrop-filter: blur(9px);
            color: black;
            border-radius: 12px;
            padding: 30px 40px;
        }
        .wrapper h1 {
            font-size: 36px;
            text-align: center;
        }
        .input-box {
            position: relative;
            width: 100%;
            height: 50px;
            margin: 30px 0;
        }
        .input-box input {
            width: 100%;
            height: 100%;
            background: white;
            border: none;
            outline: none;
            border: 2px solid rgba(255, 255, 255, .2);
            border-radius: 40px;
            font-size: 16px;
            color: black;
            padding: 20px 45px 20px 20px;
        }
        .input-box input::placeholder {
            color: black;
        }
        .wrapper .remember-forgot {
            display: flex;
            justify-content: space-between;
            font-size: 14.5px;
            margin: -15px 0 15px;
        }
        .remember-forgot label input {
            accent-color: black;
            margin-right: 3px;
        }
        .wrapper .btn {
            width: 100%;
            height: 45px;
            background: #fff;
            border: none;
            outline: none;
            border-radius: 40px;
            box-shadow: 0 0 10px rgba(0, 0, 0, .1);
            cursor: pointer;
            font-size: 16px;
            color: #333;
            font-weight: 600;
        }
        .register-link {
            color: black;
            font-size: 14.5px;
            text-align: center;
            margin: 20px 0 15px;
        }
        .register-link a {
            color: black;
            text-decoration: none;
            font-weight: 600;
        }
        .register-link a:hover {
            text-decoration: underline;
        }
        #errorMessage {
            text-align: center;
            margin-top: 10px;
            font-size: 14px;
            color: red;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Load user data from JSON
def load_users():
    if os.path.exists('users.json'):
        with open('users.json', 'r') as f:
            data = json.load(f)
        return data['users']
    return []

# Wrapper for the login form
st.markdown('<div class="wrapper">', unsafe_allow_html=True)
st.markdown("<h1>Login</h1>", unsafe_allow_html=True)

# Form for user input
with st.form(key='login_form'):
    username = st.text_input("Username", placeholder="Username")
    password = st.text_input("Password", placeholder="Password", type="password")
    
    # Remember me checkbox
    remember_me = st.checkbox("Remember Me")
    
    # Submit button
    submitted = st.form_submit_button("Login")
    
    if submitted:
        # Load users
        users = load_users()
        
        # Check if credentials match using bcrypt
        user_found = next((user for user in users if user['username'] == username), None)
        
        if user_found and bcrypt.checkpw(password.encode('utf-8'), user_found['password'].encode('utf-8')):
            st.success("Login successful!")
            st.markdown("Redirecting to the admin page...")
            # Redirect logic can go here
            # st.experimental_rerun('/admin')  # Example redirect
        else:
            st.error("Incorrect username or password!")

# Register link

st.markdown('</div>', unsafe_allow_html=True)  # Closing the wrapper div
