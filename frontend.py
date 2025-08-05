import streamlit as st
import requests

API_BASE = "http://127.0.0.1:8000"

st.set_page_config(page_title="Smart Task Manager", layout="centered")

# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_id" not in st.session_state:
    st.session_state.user_id = None
if "username" not in st.session_state:
    st.session_state.username = ""

# Redirect logic
def login_user(username, user_id):
    st.session_state.logged_in = True
    st.session_state.username = username
    st.session_state.user_id = user_id

def logout_user():
    st.session_state.logged_in = False
    st.session_state.user_id = None
    st.session_state.username = ""

def get_user_id_by_username(username):
    res = requests.get(f"{API_BASE}/users/all")
    if res.status_code == 200:
        users = res.json()
        if isinstance(users, list):
            for u in users:
                if isinstance(u, dict) and u.get("username") == username:
                    return u.get("id")
    return None

# Header
st.title("📝 Smart Task Manager")

# Auth Flow
if not st.session_state.logged_in:
    auth_page = st.radio("Choose", ["Login", "Register"])

    if auth_page == "Register":
        st.subheader("Register")
        username = st.text_input("Username", key="reg_user")
        password = st.text_input("Password", type="password", key="reg_pass")
        if st.button("Register"):
            res = requests.post(f"{API_BASE}/users/register", json={
                "username": username,
                "password": password
            })
            if res.status_code == 200:
                st.success("Registration successful! Please log in.")
            else:
                st.error("User already exists.")

    else:
        st.subheader("Login")
        username = st.text_input("Username", key="log_user")
        password = st.text_input("Password", type="password", key="log_pass")
        if st.button("Login"):
            res = requests.post(f"{API_BASE}/users/login", json={
                "username": username,
                "password": password
            })
            if res.status_code == 200:
                user_id = get_user_id_by_username(username)
                if user_id:
                    login_user(username, user_id)
                    st.success("Logged in successfully!")
                    st.rerun()
                else:
                    st.error("User ID not found.")
            else:
                st.error("Invalid credentials")

else:
    st.sidebar.success(f"Logged in as: {st.session_state.username}")
    if st.sidebar.button("Logout"):
        logout_user()
        st.rerun()

    # App Main
    menu = st.sidebar.radio("Go to", ["Create Task", "View Tasks"])

    if menu == "Create Task":
        st.subheader("Create New Task")
        title = st.text_input("Task Title")
        description = st.text_area("Task Description")
        status = st.selectbox("Status", ["Pending", "In Progress", "Done"])
        if st.button("Create Task"):
            res = requests.post(f"{API_BASE}/tasks/create", json={
                "title": title,
                "description": description,
                "status": status,
                "user_id": st.session_state.user_id
            })
            if res.status_code == 200:
                st.success("Task created successfully!")
            else:
                st.error("Failed to create task.")

    elif menu == "View Tasks":
        st.subheader("Your Tasks")
        res = requests.get(f"{API_BASE}/tasks/user/{st.session_state.user_id}")
        if res.status_code == 200:
            tasks = res.json()
            if tasks:
                for task in tasks:
                    st.markdown(f"**{task['title']}** - _{task['status']}_  \n{task['description']}  \n---")
            else:
                st.info("No tasks found.")
        else:
            st.error("Failed to fetch tasks.")
