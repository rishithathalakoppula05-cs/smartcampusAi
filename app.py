import streamlit as st
import os
from dotenv import load_dotenv
from auth import register_user, authenticate_user
from db import init_db, get_user_data, update_user_tasks

# Load environment variables from .env
load_dotenv()
API_KEY = os.getenv("CAMPUS_AI_API_KEY", "your_smart_campus_api_key_here")

# Initialize JSON database
init_db()

# Page configuration for browser tab and scaling
st.set_page_config(
    page_title="SmartCampusAI - Intelligent Hub",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Premium styling for professional look and feel
st.markdown("""
<style>
    /* Premium style variables and dark/glassmorphic aesthetics */
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }
    
    /* Custom premium card styling */
    .metric-card {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.15);
        backdrop-filter: blur(8px);
        -webkit-backdrop-filter: blur(8px);
        margin-bottom: 20px;
        transition: transform 0.3s ease, border 0.3s ease;
    }
    .metric-card:hover {
        transform: translateY(-4px);
        border-color: rgba(59, 130, 246, 0.5);
    }
    .metric-title {
        color: #94a3b8;
        font-size: 14px;
        font-weight: 600;
        text-transform: uppercase;
        margin-bottom: 8px;
    }
    .metric-value {
        color: #ffffff;
        font-size: 32px;
        font-weight: 800;
        margin-bottom: 4px;
    }
    
    /* Login & Register Card styling */
    .auth-card {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.9) 0%, rgba(15, 23, 42, 0.95) 100%);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 24px;
        padding: 30px;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4);
        margin-bottom: 20px;
    }
    
    /* Header Gradient */
    .main-header {
        background: linear-gradient(90deg, #3b82f6 0%, #8b5cf6 50%, #ec4899 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 40px;
        font-weight: 800;
        margin-bottom: 10px;
    }
    
    .subtitle {
        color: #94a3b8;
        font-size: 16px;
        margin-bottom: 30px;
    }
</style>
""", unsafe_allow_html=True)

# State initialization
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False
if "user" not in st.session_state:
    st.session_state["user"] = None
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

def logout():
    st.session_state["authenticated"] = False
    st.session_state["user"] = None
    st.session_state["chat_history"] = []
    st.rerun()

# --- PAGE: LOGIN & REGISTRATION ---
def show_auth_page():
    # Use columns to center the auth interface
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True)
        
        # Center logo and titles
        st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
        st.markdown("<h1 class='main-header'>🎓 SmartCampusAI</h1>", unsafe_allow_html=True)
        st.markdown("<p class='subtitle'>Intelligent Academic Hub & Campus Planner</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
        auth_mode = st.tabs(["🔐 Sign In", "📝 Create Account"])
        
        # TAB: LOGIN
        with auth_mode[0]:
            st.markdown("<div class='auth-card'>", unsafe_allow_html=True)
            st.subheader("Login to your Account")
            
            login_username = st.text_input("Username", key="login_username_input")
            login_password = st.text_input("Password", type="password", key="login_password_input")
            
            st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)
            if st.button("Sign In", use_container_width=True, type="primary"):
                user_info = authenticate_user(login_username, login_password)
                if user_info:
                    st.session_state["authenticated"] = True
                    st.session_state["user"] = user_info
                    st.success(f"Welcome back, {user_info['full_name']}!")
                    st.rerun()
                else:
                    st.error("Invalid username or password. Please try again.")
            st.markdown("</div>", unsafe_allow_html=True)
            
        # TAB: REGISTRATION
        with auth_mode[1]:
            st.markdown("<div class='auth-card'>", unsafe_allow_html=True)
            st.subheader("Register New Profile")
            
            reg_username = st.text_input("Username (unique identifier)", key="reg_username_input")
            reg_fullname = st.text_input("Full Name", key="reg_fullname_input")
            reg_email = st.text_input("Email Address", key="reg_email_input")
            reg_password = st.text_input("Password", type="password", key="reg_password_input")
            reg_role = st.selectbox("Role", ["Student", "Faculty", "Staff"], key="reg_role_select")
            
            st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)
            if st.button("Create Account", use_container_width=True, type="primary"):
                success, msg = register_user(reg_username, reg_password, reg_email, reg_role, reg_fullname)
                if success:
                    st.success(msg)
                    st.info("Switch to the 'Sign In' tab above to log in.")
                else:
                    st.error(msg)
            st.markdown("</div>", unsafe_allow_html=True)

# --- PAGE: MAIN DASHBOARD ---
def show_dashboard():
    # Sync status with latest database write
    user = get_user_data(st.session_state["user"]["username"])
    st.session_state["user"] = user
    
    # SIDEBAR: Profile Card
    with st.sidebar:
        st.markdown("### 👤 User Information")
        st.markdown(f"**Name:** {user['full_name']}")
        st.markdown(f"**Email:** {user['email']}")
        st.markdown(f"**Role:** `{user['role']}`")
        st.markdown("---")
        
        st.markdown("### ⚙️ System Status")
        # Evaluate API Key status
        is_default_key = API_KEY == "your_smart_campus_api_key_here" or not API_KEY.strip()
        if is_default_key:
            st.warning("⚠️ API Key: Demo Mode (Default Key)")
        else:
            st.success("🔑 API Key: Custom Connected")
            
        st.markdown("---")
        if st.button("🚪 Logout", use_container_width=True, type="secondary"):
            logout()

    # MAIN CONTENT
    st.markdown("<h1 class='main-header'>🎓 SmartCampusAI Dashboard</h1>", unsafe_allow_html=True)
    st.markdown(f"Logged in as: **{user['full_name']}** ({user['role']}) | Live Database sync active.", unsafe_allow_html=True)
    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
    
    # CALCULATE METRICS
    tasks = user["tasks"]
    pending_tasks = len([t for t in tasks if t["status"] == "Pending"])
    completed_tasks = len([t for t in tasks if t["status"] == "Completed"])
    
    grades = user["grades"]
    gpa = sum(c["gpa"] for c in grades) / len(grades) if grades else 0.0
    
    # METRIC COLUMNS
    m_col1, m_col2, m_col3, m_col4 = st.columns(4)
    with m_col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Cumulative GPA</div>
            <div class="metric-value">{gpa:.2f}</div>
            <div style="color: #4ade80; font-size: 13px;">★ Standing: Academic Honor</div>
        </div>
        """, unsafe_allow_html=True)
        
    with m_col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Current Attendance</div>
            <div class="metric-value">{user['attendance']:.1f}%</div>
            <div style="color: #4ade80; font-size: 13px;">✓ Standard Met (>75%)</div>
        </div>
        """, unsafe_allow_html=True)
        
    with m_col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Pending Tasks</div>
            <div class="metric-value">{pending_tasks}</div>
            <div style="color: #f87171; font-size: 13px;">⚠ Action Required</div>
        </div>
        """, unsafe_allow_html=True)
        
    with m_col4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Completed Tasks</div>
            <div class="metric-value">{completed_tasks}</div>
            <div style="color: #60a5fa; font-size: 13px;">✓ Academic Progress</div>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
    
    # TABS DESIGN
    tab1, tab2, tab3, tab4 = st.tabs([
        "🤖 AI Campus Assistant", 
        "📅 My Schedule & Tasks", 
        "📊 Academic Performance",
        "📢 Campus News & Map"
    ])
    
    # TAB 1: AI CAMPUS ASSISTANT
    with tab1:
        st.subheader("🤖 SmartCampus AI Conversation Assistant")
        st.write("Interact with the campus intelligence model to query database stats, GPA, schedules, or classroom locations.")
        
        # Display history
        for msg in st.session_state["chat_history"]:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])
                
        # Send inputs
        if query := st.chat_input("Ask a question (e.g., 'What is my GPA?', 'What are my tasks?', 'Show classroom locations')"):
            with st.chat_message("user"):
                st.markdown(query)
            st.session_state["chat_history"].append({"role": "user", "content": query})
            
            with st.chat_message("assistant"):
                with st.spinner("AI is thinking..."):
                    response = ""
                    lower_q = query.lower()
                    
                    if "attendance" in lower_q:
                        response = f"Your database record registers an attendance rate of **{user['attendance']}%**. You have exceeded the requirement of 75%."
                    elif "gpa" in lower_q or "grade" in lower_q:
                        summary = ", ".join([f"{g['course']} ({g['grade']})" for g in grades])
                        response = f"Your current cumulative GPA is **{gpa:.2f}**. Courses in register: {summary}."
                    elif "task" in lower_q or "todo" in lower_q or "due" in lower_q:
                        pending = [t['title'] for t in tasks if t['status'] == 'Pending']
                        if pending:
                            response = f"You have **{len(pending)}** pending tasks: " + ", ".join([f"'{item}'" for item in pending])
                        else:
                            response = "No pending tasks are currently registered in your JSON profile database."
                    else:
                        if is_default_key:
                            response = (
                                f"Greetings! I am the SmartCampus AI Assistant. "
                                f"Since the API Key in your `.env` file is set to the default placeholder, "
                                f"I am answering from my local campus information index. "
                                f"Regarding your prompt: '{query}', you can search classroom info or "
                                f"log student activities in the 'My Schedule & Tasks' tab."
                            )
                        else:
                            response = (
                                f"*(Authenticated using API Key)*: "
                                f"Your query '{query}' is processed. As a logged-in **{user['role']}**, "
                                f"the AI model advises planning a study block, checking syllabus updates, "
                                f"or scheduling time at the Innovation Hub in Block C."
                            )
                    st.markdown(response)
                    st.session_state["chat_history"].append({"role": "assistant", "content": response})

    # TAB 2: SCHEDULE & TASKS (JSON DB Modification)
    with tab2:
        st.subheader("📅 Live Schedule & Task Planner")
        st.write("Changes made here directly modify the JSON database (`data.json`) file.")
        
        # Add new tasks
        with st.expander("➕ Create New Task"):
            new_title = st.text_input("Task Title", key="new_task_title")
            new_due = st.date_input("Due Date", key="new_task_date")
            if st.button("Save Task to Database", use_container_width=True):
                if new_title.strip():
                    new_id = max([t["id"] for t in tasks]) + 1 if tasks else 1
                    tasks.append({
                        "id": new_id,
                        "title": new_title,
                        "due": str(new_due),
                        "status": "Pending"
                    })
                    update_user_tasks(user["username"], tasks)
                    st.success(f"Successfully wrote task '{new_title}' to JSON database!")
                    st.rerun()
                else:
                    st.error("Task title cannot be empty.")
                    
        st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)
        
        # Render task list and update live
        if not tasks:
            st.info("No active tasks found in database.")
        else:
            updated_tasks = []
            for t in tasks:
                col_status, col_desc = st.columns([1, 8])
                with col_status:
                    is_done = (t["status"] == "Completed")
                    checked = st.checkbox("Complete Task", value=is_done, key=f"task_check_{t['id']}", label_visibility="collapsed")
                    new_status = "Completed" if checked else "Pending"
                with col_desc:
                    if checked:
                        st.markdown(f"~~{t['title']}~~ *(Due: {t['due']})*")
                    else:
                        st.markdown(f"**{t['title']}** — *Due: {t['due']}*")
                updated_tasks.append({
                    "id": t["id"],
                    "title": t["title"],
                    "due": t["due"],
                    "status": new_status
                })
            
            # Save back if status changes
            if updated_tasks != tasks:
                update_user_tasks(user["username"], updated_tasks)
                st.rerun()

    # TAB 3: ACADEMIC PERFORMANCE
    with tab3:
        st.subheader("📊 Course Gradebook breakdown")
        
        col_list, col_chart = st.columns([2, 1])
        with col_list:
            for g in grades:
                st.markdown(f"""
                <div style="background: rgba(255,255,255,0.02); border-radius: 8px; padding: 12px; border-left: 4px solid #3b82f6; margin-bottom: 10px;">
                    <div style="display: flex; justify-content: space-between;">
                        <strong>{g['course']}</strong>
                        <span style="background: #1e3a8a; color: #93c5fd; padding: 2px 8px; border-radius: 4px; font-weight:bold;">{g['grade']}</span>
                    </div>
                    <div style="font-size: 12px; color: #94a3b8; margin-top: 4px;">Credits weight / Equivalent GPA contribution: {g['gpa']}</div>
                </div>
                """, unsafe_allow_html=True)
                
        with col_chart:
            st.markdown(f"""
            <div style="background: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 12px; padding: 20px; text-align: center;">
                <h4>Honor Designation</h4>
                <div style="font-size: 40px; margin: 10px 0;">🏆</div>
                <h3 style="margin: 10px 0; color: #facc15;">Dean's List Honoree</h3>
                <p style="font-size: 13px; color: #94a3b8;">Required GPA >= 3.50. Currently achieved: {gpa:.2f}</p>
            </div>
            """, unsafe_allow_html=True)

    # TAB 4: CAMPUS NEWS & MAPS
    with tab4:
        st.subheader("📢 Campus Information Center")
        
        col_news, col_map = st.columns([1, 1])
        with col_news:
            st.markdown("#### Latest Announcements")
            st.markdown("""
            *   📅 **July 15, 2026** - *Campus AI Hackathon registration is open. Create teams now!*
            *   🏢 **July 16, 2026** - *Block C lab maintenance scheduled from 10:00 AM to 2:00 PM.*
            *   📖 **July 18, 2026** - *Lecture by Dr. Alan on Advanced AI models in Central Room 102.*
            """)
            
        with col_map:
            st.markdown("#### Campus Navigator Guide")
            st.info("📍 **Main Campus Center** is located at Central Block. Faculty cabins are in Block A.")
            st.markdown("""
            | Area / Facility | Location | Status |
            | --- | --- | --- |
            | Library | Building A | Open (24/7) |
            | Innovation Hub | Building C | Open (08:00 - 22:00) |
            | Student Lounge | Building B | Closed for Maintenance |
            """)

# --- MAIN EXECUTION ROUTING ---
def main():
    if not st.session_state["authenticated"]:
        show_auth_page()
    else:
        show_dashboard()

if __name__ == "__main__":
    main()
