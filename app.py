import streamlit as st
import matplotlib.pyplot as plt
from environment import WorkdayEnv

st.title("🌊 FocusFlow AI")
st.info("🧬 **Scientific Fact:** The brain can only maintain 'Deep Work' for 90-minute cycles before productivity drops by 50%. Plan your breaks to stay in the **Flow Zone**!")

# --- STABILITY & HUD ---
st.set_page_config(page_title="FocusFlow AI", layout="wide")
st.markdown("<style>html { overflow-anchor: none !important; } .stButton button { border-radius: 8px; }</style>", unsafe_allow_html=True)

if 'env' not in st.session_state:
    st.session_state.env = WorkdayEnv()

env = st.session_state.env
day_over = env.time_elapsed >= 8

# --- SIDEBAR: THE PLANNER (Select/Unselect) ---
with st.sidebar:
    st.header("📋 Daily Planner")
    st.caption("Add tasks here, then execute your plan.")
    
    # Selection Area
    new_task = st.selectbox("Choose Task", ["Deep Work", "Meeting/Admin", "Break"])
    if st.button("➕ Add to Plan", use_container_width=True, disabled=day_over):
        env.add_to_plan(new_task)
        st.rerun()

    st.divider()
    st.subheader("Current Plan")
    if not env.pending_tasks:
        st.write("Plan is empty.")
    else:
        # Unselect Logic
        for idx, task in enumerate(env.pending_tasks):
            cols = st.columns([3, 1])
            cols[0].write(f"{idx+1}. {task}")
            if cols[1].button("🗑️", key=f"del_{idx}"):
                env.remove_from_plan(idx)
                st.rerun()
        
        if st.button("🚀 EXECUTE ALL", type="primary", use_container_width=True):
            env.execute_plan()
            st.rerun()

# --- MAIN DASHBOARD ---
st.title("🌊 FocusFlow AI")

# Metrics
m1, m2, m3 = st.columns(3)
m1.metric("⚡ Energy", f"{env.energy}%")
m2.metric("📈 Productivity", env.productivity)
m3.metric("🕒 Progress", f"{env.time_elapsed}/8h")
st.progress(env.energy / 100)

st.write("---")

# Visualizing the day
col_log, col_graph = st.columns([1, 2])

with col_log:
    st.subheader("📝 Accomplishments")
    if not env.log:
        st.info("No work completed yet. Add tasks in the sidebar!")
    for entry in reversed(env.log):
        st.write(entry)

with col_graph:
    df = env.get_history_df()
    if len(df) > 1:
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.plot(df["Time"], df["Energy"], color='red', label="Energy", marker="o")
        ax.plot(df["Time"], df["Productivity"], color='blue', label="Prod", marker="s")
        ax.set_ylim(0, max(120, env.productivity + 20))
        ax.legend()
        st.pyplot(fig)

if day_over:
    st.success("Workday Complete!")
    if st.button("Restart"):
        st.session_state.env = WorkdayEnv()
        st.rerun()
