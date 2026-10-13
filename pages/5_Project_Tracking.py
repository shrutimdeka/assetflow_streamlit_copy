import streamlit as st
from utils.styles import apply_global_styles

apply_global_styles()

st.markdown('<div class="eyebrow">Delivery</div>', unsafe_allow_html=True)
st.markdown('<div class="page-title">Project Tracking</div>', unsafe_allow_html=True)
st.markdown('<div class="page-description">Monitor active projects, milestones, owners and delivery health.</div>', unsafe_allow_html=True)

projects = [
    ("Global Retail Portal", "Phase 2", "72%", "12 members", "On Track"),
    ("Cloud Migration - Alpha", "Build", "58%", "8 members", "On Track"),
    ("Payment Gateway v2", "Testing", "83%", "6 members", "In Review"),
]
for name, milestone, progress, team, status in projects:
    with st.container(border=True):
        c1, c2, c3 = st.columns([2.5, 1.5, 1])
        with c1:
            st.markdown(f"**{name}**")
            st.caption(f"Milestone: {milestone} • {team}")
        with c2:
            st.progress(int(progress[:-1]))
            st.caption(progress + " complete")
        with c3:
            st.info(status)
