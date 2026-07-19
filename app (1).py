
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, date
import json
import os
from io import BytesIO

# Page config
st.set_page_config(
    page_title="Amandla EHS Dashboard",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header { font-size: 2rem; font-weight: 700; color: #1f2937; }
    .sub-header { font-size: 1.1rem; color: #6b7280; }
    .kpi-card { background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%); padding: 1.5rem; border-radius: 12px; border-left: 4px solid #3b82f6; }
    .kpi-red { border-left-color: #ef4444; }
    .kpi-amber { border-left-color: #f59e0b; }
    .kpi-green { border-left-color: #10b981; }
    .kpi-value { font-size: 2.2rem; font-weight: 800; color: #1f2937; }
    .kpi-label { font-size: 0.85rem; color: #6b7280; text-transform: uppercase; letter-spacing: 0.05em; }
    .kpi-target { font-size: 0.8rem; color: #9ca3af; }
    .status-badge { display: inline-block; padding: 2px 10px; border-radius: 12px; font-size: 0.75rem; font-weight: 600; }
    .status-lti { background: #fee2e2; color: #991b1b; }
    .status-mtc { background: #fef3c7; color: #92400e; }
    .status-fa { background: #dbeafe; color: #1e40af; }
    .status-near { background: #d1fae5; color: #065f46; }
    .site-card { background: white; padding: 1rem; border-radius: 8px; border: 1px solid #e5e7eb; }
    .warning-text { color: #dc2626; font-weight: 600; }
    .success-text { color: #059669; font-weight: 600; }
    div[data-testid="stDataFrame"] td { font-size: 0.85rem; }
    div[data-testid="stDataFrame"] th { font-size: 0.8rem; }
</style>
""", unsafe_allow_html=True)

# ─── DATA STORE ───
# Use session state to persist data
if 'incidents' not in st.session_state:
    st.session_state.incidents = [
        {"no": 1, "date": "2026-01-20", "surname": "Bailey", "first_name": "Danielle", "emp_type": "LDC", "division": "Building", "site": "Rawsonville Sports Ground", "description": "Installing basketball poles, pole hit shoulder", "category": "LTI", "cause": "Struck by", "body_part": "Shoulder", "days_away": 1},
        {"no": 2, "date": "2026-01-22", "surname": "Bunu", "first_name": "Thembela", "emp_type": "Perm", "division": "Asphalt", "site": "Asphalt", "description": "Pinky finger caught in manhole lid", "category": "LTI", "cause": "Caught between", "body_part": "Finger", "days_away": 0},
        {"no": 3, "date": "2026-02-04", "surname": "Byron", "first_name": "Syster", "emp_type": "LDC", "division": "Civils", "site": "BlueBerry Hill - D583", "description": "Pulling bag net, broke, bumped back against digger bucket", "category": "LTI", "cause": "Struck by", "body_part": "Shoulder", "days_away": 1},
        {"no": 4, "date": "2026-01-09", "surname": "Mc Charlie", "first_name": "Keano", "emp_type": "LDC", "division": "Civils", "site": "Lainghville", "description": "Attacked by swarm of bees", "category": "MTC", "cause": "Snake & Insect bites", "body_part": "Multiple", "days_away": 0},
        {"no": 5, "date": "2026-02-16", "surname": "Fensters", "first_name": "Ethan", "emp_type": "LDC", "division": "Civils", "site": "BlueBerry Hill - D583", "description": "Knocked by public vehicle while fixing blades", "category": "MTC", "cause": "MVA", "body_part": "Arm", "days_away": 0},
        {"no": 6, "date": "2026-02-18", "surname": "Byron", "first_name": "Syster", "emp_type": "LDC", "division": "Civils", "site": "BlueBerry Hill - D583", "description": "Shutter board broke, hit thigh in trench", "category": "LTI", "cause": "Struck by", "body_part": "Leg", "days_away": 3},
        {"no": 7, "date": "2026-03-02", "surname": "Kalako", "first_name": "Wonke", "emp_type": "LDC", "division": "Civils", "site": "-", "description": "Fell in truck during emergency stop, bumped head", "category": "-", "cause": "Struck Against", "body_part": "Head", "days_away": 0},
        {"no": 8, "date": "2026-03-11", "surname": "Van Rooyen", "first_name": "Leslin", "emp_type": "Perm", "division": "Workshop", "site": "Workshop", "description": "Thumb caught between steel plate and machine", "category": "MTC", "cause": "Caught between", "body_part": "Finger", "days_away": 0},
        {"no": 9, "date": "2026-03-12", "surname": "Meyer", "first_name": "Tristin", "emp_type": "LDC", "division": "Civils", "site": "GrandWest", "description": "Concrete fragment into eye through goggles", "category": "MTC", "cause": "Foreign Object", "body_part": "Eye", "days_away": 0},
        {"no": 10, "date": "2026-03-14", "surname": "Mattheus", "first_name": "Gerhardus", "emp_type": "Perm", "division": "Structures", "site": "Lainghville", "description": "Dust blew into face after removing goggles", "category": "MTC", "cause": "Foreign Object", "body_part": "Eye", "days_away": 0},
        {"no": 11, "date": "2026-03-18", "surname": "Badenhorst", "first_name": "Rudi", "emp_type": "Perm", "division": "Workshop", "site": "Workshop", "description": "Metal piece shot into leg while hammering", "category": "MTC", "cause": "Struck by", "body_part": "Leg", "days_away": 0},
        {"no": 12, "date": "2026-03-19", "surname": "Radloff", "first_name": "Adrihano", "emp_type": "LDC", "division": "Civils", "site": "Jan Van Ribeek - D591", "description": "Finger stuck in hooker/fitting", "category": "LTI", "cause": "Caught between", "body_part": "Finger", "days_away": 1},
        {"no": 13, "date": "2026-04-16", "surname": "Mpotya", "first_name": "Siyamlela", "emp_type": "LDC", "division": "Civils", "site": "King Air", "description": "Twisted ankle running in front of grader", "category": "LTI", "cause": "Strains/Sprains", "body_part": "Ankle", "days_away": 2},
    ]

if 'manhours' not in st.session_state:
    st.session_state.manhours = {
        "Civils": {"Mar": 0, "Apr": 0, "May": 0, "Jun": 0, "Jul": 0, "Aug": 0, "Sep": 0, "Oct": 0, "Nov": 0, "Dec": 0, "Jan": 0, "Feb": 0},
        "Structures": {"Mar": 0, "Apr": 0, "May": 0, "Jun": 0, "Jul": 0, "Aug": 0, "Sep": 0, "Oct": 0, "Nov": 0, "Dec": 0, "Jan": 0, "Feb": 0},
        "Building": {"Mar": 0, "Apr": 0, "May": 0, "Jun": 0, "Jul": 0, "Aug": 0, "Sep": 0, "Oct": 0, "Nov": 0, "Dec": 0, "Jan": 0, "Feb": 0},
        "Workshop": {"Mar": 0, "Apr": 0, "May": 0, "Jun": 0, "Jul": 0, "Aug": 0, "Sep": 0, "Oct": 0, "Nov": 0, "Dec": 0, "Jan": 0, "Feb": 0},
        "Asphalt": {"Mar": 0, "Apr": 0, "May": 0, "Jun": 0, "Jul": 0, "Aug": 0, "Sep": 0, "Oct": 0, "Nov": 0, "Dec": 0, "Jan": 0, "Feb": 0},
        "Sub-Contractors": {"Mar": 14850, "Apr": 28116, "May": 24354, "Jun": 94248, "Jul": 42768, "Aug": 0, "Sep": 0, "Oct": 0, "Nov": 0, "Dec": 0, "Jan": 891, "Feb": 0}
    }

if 'sites' not in st.session_state:
    st.session_state.sites = [
        {"code": "D563", "name": "Muizenberg Seawall", "division": "Civils", "status": "Active"},
        {"code": "D583", "name": "BlueBerry Hill", "division": "Civils", "status": "Active"},
        {"code": "D585", "name": "Swartland Road", "division": "Civils", "status": "Active"},
        {"code": "D568", "name": "Wetton Road", "division": "Civils", "status": "Active"},
        {"code": "D016", "name": "Head Office", "division": "Admin", "status": "Active"},
        {"code": "D579", "name": "Ukuqala Substations", "division": "Building", "status": "Active"},
        {"code": "D591", "name": "Jan Van Ribeek", "division": "Civils", "status": "Active"},
        {"code": "D557", "name": "Hawston Stadium", "division": "Building", "status": "Active"},
        {"code": "D538", "name": "Sun Central", "division": "Civils", "status": "Active"},
        {"code": "D523", "name": "Tafelberg Road", "division": "Civils", "status": "Active"},
        {"code": "D570", "name": "Brackenfell High School", "division": "Civils", "status": "Active"},
        {"code": "D541", "name": "Kruskal Ave", "division": "Civils", "status": "Active"},
        {"code": "D547", "name": "Jakes Gewel 2", "division": "Civils", "status": "Active"},
        {"code": "D577", "name": "Vredenberg WTF", "division": "Building", "status": "Active"},
    ]

# ─── HELPER FUNCTIONS ───
def calculate_rates(incidents_df, total_hours):
    """Calculate TIFR, LTIFR, FIFR"""
    if total_hours == 0:
        return 0, 0, 0
    total_injuries = len(incidents_df)
    ltis = len(incidents_df[incidents_df['category'] == 'LTI'])
    fatalities = len(incidents_df[incidents_df['category'] == 'Fatality'])

    tifr = (total_injuries * 1000000) / total_hours
    ltifr = (ltis * 1000000) / total_hours
    fifr = (fatalities * 1000000) / total_hours
    return round(tifr, 2), round(ltifr, 2), round(fifr, 2)

def get_total_manhours():
    """Sum all manhours across all divisions"""
    total = 0
    for div, months in st.session_state.manhours.items():
        total += sum(months.values())
    return total

def get_category_badge(category):
    if category == 'LTI':
        return '<span class="status-badge status-lti">LTI</span>'
    elif category == 'MTC':
        return '<span class="status-badge status-mtc">MTC</span>'
    elif category == 'First Aid':
        return '<span class="status-badge status-fa">First Aid</span>'
    elif category == 'Near Miss':
        return '<span class="status-badge status-near">Near Miss</span>'
    else:
        return f'<span class="status-badge" style="background:#f3f4f6;color:#6b7280;">{category}</span>'

# ─── SIDEBAR ───
with st.sidebar:
    st.markdown("### 🏗️ Amandla Construction")
    st.markdown("<p class='sub-header'>EHS Management System</p>", unsafe_allow_html=True)
    st.divider()

    # Check for navigation override from landing page buttons
if 'nav_override' in st.session_state:
    page = st.session_state.nav_override
    del st.session_state.nav_override
else:
    page = st.radio("Navigate", [
        "🏠 Home",
        "📊 Dashboard",
        "🚨 Incident Register",
        "⏱️ Manhours",
        "📤 Import Site Data",
        "📈 Analytics",
        "📋 Monthly Report",
        "⚙️ Settings"
    ], label_visibility="collapsed")

    st.divider()

    # Quick Stats
    total_hours = get_total_manhours()
    incidents_df = pd.DataFrame(st.session_state.incidents)
    tifr, ltifr, fifr = calculate_rates(incidents_df, total_hours)

    st.markdown("#### Quick Stats (YTD)")
    st.markdown(f"**Total IODs:** {len(incidents_df)}")
    st.markdown(f"**LTIs:** {len(incidents_df[incidents_df['category']=='LTI'])}")
    st.markdown(f"**Manhours:** {total_hours:,}")
    st.markdown(f"**TIFR:** {tifr}")
    st.markdown(f"**LTIFR:** {ltifr}")

    st.divider()
    st.caption(f"Today: {datetime.now().strftime('%d %b %Y')}")


# ─── LANDING/WELCOME PAGE (Default) ───
if page == "🏠 Home":
    st.markdown("<div class='main-header'>Welcome to Amandla EHS</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-header'>Environmental, Health & Safety Management System</div>", unsafe_allow_html=True)
    st.write("")

    # Hero section
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("""
        ### What You Can Do Here

        **📊 Dashboard** — View real-time safety stats, TIFR/LTIFR, and trends  
        **🚨 Incident Register** — Report and track all incidents (LTI, MTC, Near Miss)  
        **⏱️ Manhours** — Track hours by division and site  
        **📤 Import Site Data** — Upload monthly stats from site supervisors  
        **📈 Analytics** — Deep-dive into injury causes, body parts, sites  
        **📋 Monthly Report** — Auto-generate EHS reports for management  

        ---

        **👆 Select a page from the sidebar to get started.**
        """)

        # Quick action buttons
        st.write("### Quick Actions")
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            if st.button("📊 View Dashboard", use_container_width=True):
                st.session_state.nav_override = "📊 Dashboard"
                st.rerun()
        with col_b:
            if st.button("🚨 Add Incident", use_container_width=True):
                st.session_state.nav_override = "🚨 Incident Register"
                st.rerun()
        with col_c:
            if st.button("📤 Import Data", use_container_width=True):
                st.session_state.nav_override = "📤 Import Site Data"
                st.rerun()

    with col2:
        # Summary card
        st.markdown("#### At a Glance (YTD)")
        total_hours = get_total_manhours()
        incidents_df = pd.DataFrame(st.session_state.incidents)
        tifr, ltifr, fifr = calculate_rates(incidents_df, total_hours)

        st.metric("Total IODs", len(incidents_df))
        st.metric("LTIs", len(incidents_df[incidents_df['category']=='LTI']))
        st.metric("TIFR", tifr)
        st.metric("LTIFR", ltifr)

        st.markdown("---")
        st.markdown(f"**Period:** Mar 2025 — Feb 2026")
        st.markdown(f"**Sites Active:** {len(st.session_state.sites)}")

    # Recent activity
    st.write("")
    st.markdown("### Recent Activity")
    recent = incidents_df.sort_values('date', ascending=False).head(5)
    if not recent.empty:
        for _, inc in recent.iterrows():
            cat_color = "🔴" if inc['category'] == 'LTI' else "🟡" if inc['category'] == 'MTC' else "🔵"
            st.markdown(f"{cat_color} **{inc['date']}** — {inc['surname']}, {inc['first_name']} | {inc['site']} | {inc['category']}")
    else:
        st.info("No recent incidents recorded.")


# ─── DASHBOARD PAGE ───
if page == "📊 Dashboard":
    st.markdown("<div class='main-header'>EHS Dashboard</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-header'>Real-time safety performance overview</div>", unsafe_allow_html=True)
    st.write("")

    # KPI Cards
    col1, col2, col3, col4 = st.columns(4)

    total_injuries = len(incidents_df)
    ltis = len(incidents_df[incidents_df['category'] == 'LTI'])
    mtcs = len(incidents_df[incidents_df['category'] == 'MTC'])

    with col1:
        st.markdown(f"""
        <div class="kpi-card kpi-red">
            <div class="kpi-label">Total Injuries</div>
            <div class="kpi-value">{total_injuries}</div>
            <div class="kpi-target">Target: &lt; 20 | YTD Mar 2025-26</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="kpi-card kpi-amber">
            <div class="kpi-label">Lost Time Injuries</div>
            <div class="kpi-value">{ltis}</div>
            <div class="kpi-target">Target LTIFR: 0.25</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="kpi-card kpi-red">
            <div class="kpi-label">TIFR</div>
            <div class="kpi-value">{tifr}</div>
            <div class="kpi-target">Target: 1.25 | {'⚠️ Above target' if tifr > 1.25 else '✅ On target'}</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div class="kpi-card kpi-red">
            <div class="kpi-label">LTIFR</div>
            <div class="kpi-value">{ltifr}</div>
            <div class="kpi-target">Target: 0.25 | {'⚠️ Above target' if ltifr > 0.25 else '✅ On target'}</div>
        </div>
        """, unsafe_allow_html=True)

    st.write("")

    # Charts Row
    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown("#### Injuries by Division")
        div_counts = incidents_df[incidents_df['division'] != '-']['division'].value_counts().reset_index()
        div_counts.columns = ['Division', 'Count']
        st.bar_chart(div_counts.set_index('Division'), use_container_width=True)

    with col_right:
        st.markdown("#### Injury Causes")
        cause_counts = incidents_df[incidents_df['cause'] != '']['cause'].value_counts().reset_index()
        cause_counts.columns = ['Cause', 'Count']
        st.bar_chart(cause_counts.set_index('Cause'), use_container_width=True)

    st.write("")

    # Body Part & Site
    col_left2, col_right2 = st.columns(2)

    with col_left2:
        st.markdown("#### Injuries by Body Part")
        body_counts = incidents_df[incidents_df['body_part'] != '']['body_part'].value_counts().reset_index()
        body_counts.columns = ['Body Part', 'Count']
        st.bar_chart(body_counts.set_index('Body Part'), use_container_width=True)

    with col_right2:
        st.markdown("#### Top Sites by Incidents")
        site_counts = incidents_df[incidents_df['site'] != '-']['site'].value_counts().head(8).reset_index()
        site_counts.columns = ['Site', 'Count']
        st.bar_chart(site_counts.set_index('Site'), use_container_width=True)

    st.write("")

    # Recent Incidents Table
    st.markdown("#### Recent Incidents")
    recent = incidents_df.sort_values('date', ascending=False).head(10)
    display_df = recent[['date', 'surname', 'first_name', 'site', 'division', 'category', 'days_away']].copy()
    display_df.columns = ['Date', 'Surname', 'First Name', 'Site', 'Division', 'Category', 'Days Away']
    st.dataframe(display_df, use_container_width=True, hide_index=True)

# ─── INCIDENT REGISTER PAGE ───
elif page == "🚨 Incident Register":
    st.markdown("<div class='main-header'>Incident Register</div>", unsafe_allow_html=True)

    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("➕ Add New Incident", type="primary", use_container_width=True):
            st.session_state.show_add_form = True

    # Add Incident Form
    if st.session_state.get('show_add_form', False):
        with st.form("add_incident_form"):
            st.markdown("### Add New Incident")
            col_a, col_b = st.columns(2)
            with col_a:
                date_input = st.date_input("Date *", value=date.today())
                surname = st.text_input("Surname *")
                emp_type = st.selectbox("Employment Type *", ["LDC", "Perm", "Sub-contractor"])
                division = st.selectbox("Division *", ["Civils", "Structures", "Building", "Workshop", "Asphalt", "Admin", "Road Marking"])
            with col_b:
                site = st.selectbox("Site *", [s["name"] for s in st.session_state.sites] + ["Other"])
                first_name = st.text_input("First Names *")
                category = st.selectbox("Category *", ["LTI", "MTC", "First Aid", "Near Miss", "Fatality"])
                days_away = st.number_input("Days Away (if LTI)", min_value=0, value=0)

            description = st.text_area("How Injury Occurred *", placeholder="Describe what happened...")
            preventative = st.text_area("Preventative Action", placeholder="What will be done to prevent recurrence?")
            cause = st.selectbox("Cause", ["Struck by", "Caught between", "Fall from height", "Slips/Trips", "MVA", "Foreign Object", "Strains/Sprains", "Snake & Insect bites", "Struck Against", "Other"])
            body_part = st.selectbox("Body Part Injured", ["Finger", "Shoulder", "Leg", "Eye", "Head", "Arm", "Ankle", "Hand", "Back", "Foot", "Knee", "Multiple", "Other"])

            submitted = st.form_submit_button("Save Incident", type="primary")
            if submitted:
                new_no = max([i["no"] for i in st.session_state.incidents]) + 1
                st.session_state.incidents.append({
                    "no": new_no,
                    "date": date_input.strftime("%Y-%m-%d"),
                    "surname": surname,
                    "first_name": first_name,
                    "emp_type": emp_type,
                    "division": division,
                    "site": site if site != "Other" else st.text_input("Specify Site"),
                    "description": description,
                    "category": category,
                    "cause": cause,
                    "body_part": body_part,
                    "days_away": days_away if category == "LTI" else 0
                })
                st.session_state.show_add_form = False
                st.success("✅ Incident added successfully!")
                st.rerun()

        if st.button("Cancel"):
            st.session_state.show_add_form = False
            st.rerun()

    st.write("")

    # Filters
    col_f1, col_f2, col_f3, col_f4 = st.columns([2, 1, 1, 1])
    with col_f1:
        search = st.text_input("🔍 Search", placeholder="Name, site, description...")
    with col_f2:
        filter_div = st.selectbox("Division", ["All"] + list(incidents_df['division'].unique()))
    with col_f3:
        filter_cat = st.selectbox("Category", ["All"] + list(incidents_df['category'].unique()))
    with col_f4:
        st.write("")
        st.write("")
        if st.button("Clear Filters", type="secondary"):
            st.rerun()

    # Filter logic
    filtered = incidents_df.copy()
    if search:
        mask = filtered.astype(str).apply(lambda x: x.str.contains(search, case=False, na=False)).any(axis=1)
        filtered = filtered[mask]
    if filter_div != "All":
        filtered = filtered[filtered['division'] == filter_div]
    if filter_cat != "All":
        filtered = filtered[filtered['category'] == filter_cat]

    st.write(f"Showing {len(filtered)} of {len(incidents_df)} incidents")

    display_cols = ['no', 'date', 'surname', 'first_name', 'emp_type', 'division', 'site', 'category', 'cause', 'days_away']
    display_filtered = filtered[display_cols].copy()
    display_filtered.columns = ['#', 'Date', 'Surname', 'First Name', 'Type', 'Division', 'Site', 'Category', 'Cause', 'Days']
    st.dataframe(display_filtered, use_container_width=True, hide_index=True)

    # Export
    col_ex1, col_ex2 = st.columns(2)
    with col_ex1:
        csv = display_filtered.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download CSV", csv, "incidents.csv", "text/csv")
    with col_ex2:
        excel_buffer = BytesIO()
        display_filtered.to_excel(excel_buffer, index=False, sheet_name='Incidents')
        st.download_button("📥 Download Excel", excel_buffer.getvalue(), "incidents.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

# ─── MANHOURS PAGE ───
elif page == "⏱️ Manhours":
    st.markdown("<div class='main-header'>Manhours Tracking</div>", unsafe_allow_html=True)

    # Summary cards
    col1, col2, col3 = st.columns(3)
    total_hours = get_total_manhours()
    with col1:
        st.metric("Total Manhours (YTD)", f"{total_hours:,}")
    with col2:
        avg_monthly = total_hours / 12
        st.metric("Avg Monthly Hours", f"{avg_monthly:,.0f}")
    with col3:
        st.metric("Peak Month", "Jun", "94,248 hrs")

    st.write("")

    # Manhours entry form
    st.markdown("### Add Monthly Manhours")
    with st.form("manhours_form"):
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            mh_division = st.selectbox("Division", list(st.session_state.manhours.keys()))
        with col_b:
            mh_month = st.selectbox("Month", ["Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec", "Jan", "Feb"])
        with col_c:
            mh_hours = st.number_input("Hours Worked", min_value=0, value=0, step=100)

        mh_submitted = st.form_submit_button("Update Manhours", type="primary")
        if mh_submitted:
            st.session_state.manhours[mh_division][mh_month] = mh_hours
            st.success(f"✅ Updated {mh_division} - {mh_month}: {mh_hours:,} hours")
            st.rerun()

    st.write("")

    # Display manhours table
    st.markdown("### Manhours by Division & Month")
    mh_df = pd.DataFrame(st.session_state.manhours).T
    mh_df['Total'] = mh_df.sum(axis=1)
    st.dataframe(mh_df, use_container_width=True)

    # Chart
    st.markdown("### Monthly Manhours Trend")
    months = ["Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec", "Jan", "Feb"]
    monthly_totals = [sum(st.session_state.manhours[div][m] for div in st.session_state.manhours) for m in months]
    chart_df = pd.DataFrame({"Month": months, "Hours": monthly_totals})
    st.bar_chart(chart_df.set_index("Month"), use_container_width=True)

# ─── IMPORT SITE DATA PAGE ───
elif page == "📤 Import Site Data":
    st.markdown("<div class='main-header'>Import Site Data</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-header'>Upload monthly EHS stats from sites. Auto-extracts manhours & incidents.</div>", unsafe_allow_html=True)

    st.write("")

    uploaded_file = st.file_uploader("📁 Drop site spreadsheet here", type=["xlsx", "xls", "csv"], 
                                     help="Upload the monthly EHS stats file from any site (e.g., D563 - Muizenberg)")

    if uploaded_file is not None:
        try:
            # Read the uploaded file
            xls_uploaded = pd.ExcelFile(uploaded_file)
            sheet_name = xls_uploaded.sheet_names[0]
            df_upload = pd.read_excel(xls_uploaded, sheet_name=sheet_name, header=None)

            st.success(f"✅ File uploaded: **{uploaded_file.name}** | Sheet: **{sheet_name}**")

            # Extract site info
            site_name = str(df_upload.iloc[5, 5]) if pd.notna(df_upload.iloc[5, 5]) else "Unknown"
            division = str(df_upload.iloc[6, 5]) if pd.notna(df_upload.iloc[6, 5]) else "Unknown"

            st.markdown(f"""
            <div class="site-card">
                <b>Site:</b> {site_name}<br>
                <b>Division:</b> {division}<br>
                <b>Period:</b> 2025
            </div>
            """, unsafe_allow_html=True)

            # Extract manhours data (rows 9-20, columns 1-7)
            months = ["January", "February", "March", "April", "May", "June", 
                     "July", "August", "September", "October", "November", "December"]

            manhours_data = []
            incidents_data = []

            for i, month in enumerate(months):
                row_idx = 9 + i
                if row_idx < len(df_upload):
                    row = df_upload.iloc[row_idx]

                    # Sub-contractor data (cols 1-3)
                    sub_contractors = int(row[1]) if pd.notna(row[1]) else 0
                    sub_employees = int(row[2]) if pd.notna(row[2]) else 0
                    sub_hours = int(row[3]) if pd.notna(row[3]) else 0

                    # Amandla direct data (cols 5-7)
                    ama_plant = int(row[5]) if pd.notna(row[5]) else 0
                    ama_employees = int(row[6]) if pd.notna(row[6]) else 0
                    ama_hours = int(row[7]) if pd.notna(row[7]) else 0

                    # Incidents (cols 9-21)
                    near_misses = int(row[9]) if pd.notna(row[9]) else 0
                    unsafe_acts = int(row[11]) if pd.notna(row[11]) else 0
                    first_aid = int(row[13]) if pd.notna(row[13]) else 0
                    mtc = int(row[15]) if pd.notna(row[15]) else 0
                    fatality = int(row[17]) if pd.notna(row[17]) else 0
                    lti = int(row[19]) if pd.notna(row[19]) else 0
                    vehicle = int(row[21]) if pd.notna(row[21]) else 0

                    manhours_data.append({
                        "Month": month,
                        "Sub-Contractors (hrs)": sub_hours,
                        "Amandla Direct (hrs)": ama_hours,
                        "Total Hours": sub_hours + ama_hours,
                        "Sub-Contractors (emp)": sub_employees,
                        "Amandla Direct (emp)": ama_employees,
                        "Plant Count": ama_plant
                    })

                    incidents_data.append({
                        "Month": month,
                        "Near Misses": near_misses,
                        "Unsafe Acts": unsafe_acts,
                        "First Aid": first_aid,
                        "MTC": mtc,
                        "LTI": lti,
                        "Fatality": fatality,
                        "Vehicle Incidents": vehicle
                    })

            # Display extracted data
            st.write("")
            st.markdown("### 📊 Extracted Manhours")
            mh_extracted = pd.DataFrame(manhours_data)
            st.dataframe(mh_extracted, use_container_width=True, hide_index=True)

            st.markdown("### 🚨 Extracted Incidents")
            inc_extracted = pd.DataFrame(incidents_data)
            st.dataframe(inc_extracted, use_container_width=True, hide_index=True)

            # Summary
            total_site_hours = mh_extracted["Total Hours"].sum()
            total_site_ltis = inc_extracted["LTI"].sum()
            total_site_mtcs = inc_extracted["MTC"].sum()

            st.write("")
            col_s1, col_s2, col_s3, col_s4 = st.columns(4)
            with col_s1:
                st.metric("Total Hours", f"{total_site_hours:,}")
            with col_s2:
                st.metric("LTIs", total_site_ltis)
            with col_s3:
                st.metric("MTCs", total_site_mtcs)
            with col_s4:
                site_tifr = round((total_site_ltis + total_site_mtcs) * 1000000 / total_site_hours, 2) if total_site_hours > 0 else 0
                st.metric("Site TIFR", site_tifr)

            # Import button
            st.write("")
            if st.button("✅ Import into Master Database", type="primary", use_container_width=True):
                # In real implementation, this would merge into the database
                st.success(f"🎉 Imported {sheet_name} data into master database!")
                st.info("Note: In the full version, this would auto-update all dashboards and reports.")

        except Exception as e:
            st.error(f"❌ Error reading file: {str(e)}")
            st.info("Make sure the file matches the standard site format (D563 template).")

    else:
        # Show expected format
        st.write("")
        st.markdown("### 📋 Expected Site Spreadsheet Format")

        expected_format = """
        | Row | Content | Columns |
        |-----|---------|---------|
        | 1-4 | Header / Title | Doc No, Rev No, Rev Date |
        | 5 | Period of statistics | Site Name: [D563 - Muizenberg Seawall] |
        | 6 | Division | [Civils] |
        | 7 | Column headers | Sub-Contractor / Amandla / Incidents |
        | 8 | Month headers | Jan-Dec with employee counts, hours, incidents |
        | 9-20 | Monthly data | One row per month |
        | 21 | TOTALS row | Sum of all months |
        """
        st.markdown(expected_format)

        st.info("💡 **Tip:** Sites should use the same template. The app auto-detects site code, division, manhours, and incidents from the standard format.")

# ─── ANALYTICS PAGE ───
elif page == "📈 Analytics":
    st.markdown("<div class='main-header'>Analytics & Trends</div>", unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["YTD Performance", "12-Month Rolling", "Yearly Comparison"])

    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### TIFR Trend")
            # Mock trend data
            trend_df = pd.DataFrame({
                "Month": ["Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec", "Jan", "Feb"],
                "TIFR": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 12.67, 12.67],
                "Target": [1.25]*12
            })
            st.line_chart(trend_df.set_index("Month"), use_container_width=True)

        with col2:
            st.markdown("#### LTIFR Trend")
            ltifr_df = pd.DataFrame({
                "Month": ["Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec", "Jan", "Feb"],
                "LTIFR": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5.85, 5.85],
                "Target": [0.25]*12
            })
            st.line_chart(ltifr_df.set_index("Month"), use_container_width=True)

        st.write("")
        st.markdown("#### Employment Type Breakdown")
        emp_data = pd.DataFrame({
            "Type": ["LDC", "Permanent", "Sub-contractor"],
            "IODs": [10, 4, 0],
            "LTIs": [5, 1, 0]
        })
        st.bar_chart(emp_data.set_index("Type"), use_container_width=True)

    with tab2:
        st.markdown("#### 12-Month Rolling Manhours")
        rolling_df = pd.DataFrame({
            "Month": ["Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec", "Jan", "Feb"],
            "Hours": [14850, 28116, 24354, 94248, 42768, 0, 0, 0, 0, 0, 891, 0]
        })
        st.area_chart(rolling_df.set_index("Month"), use_container_width=True)

    with tab3:
        st.markdown("#### Year-over-Year Comparison")
        yoy_df = pd.DataFrame({
            "Year": ["2022", "2023", "2024", "2025"],
            "LTIs": [0, 6, 0, 6],
            "TIFR": [0, 12.67, 0, 12.67]
        })
        st.bar_chart(yoy_df.set_index("Year"), use_container_width=True)

# ─── MONTHLY REPORT PAGE ───
elif page == "📋 Monthly Report":
    st.markdown("<div class='main-header'>Monthly EHS Report</div>", unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])
    with col1:
        report_month = st.selectbox("Select Month", ["March 2026", "February 2026", "January 2026"])
    with col2:
        st.write("")
        st.write("")
        if st.button("📥 Generate Report", type="primary", use_container_width=True):
            st.success("✅ Report generated!")

    st.write("")

    # Report preview
    st.markdown("### Report Preview: March 2026")

    col_r1, col_r2 = st.columns(2)
    with col_r1:
        st.markdown("""
        #### 1. Highlights
        - Client audit scores received from DBSA Cape Town Parliament project
        - Weekly audit schedule maintained

        #### 2. Lowlights
        - 6 IODs recorded this period
        - BlueBerry Hill site: 3 incidents (2 LTIs)
        - Workshop: 2 MTCs from machinery operations
        """)
    with col_r2:
        st.markdown("""
        #### 3. Stats Summary
        | Metric | Value |
        |--------|-------|
        | Total IODs | 6 |
        | LTIs | 2 |
        | MTCs | 0 |
        | Fatalities | 0 |
        | Manhours | 47,322 |
        | TIFR | 12.67 |
        | LTIFR | 5.85 |
        """)

    st.write("")
    st.markdown("#### 4. Focus Areas")
    st.markdown("""
    - ⚠️ **PPE Compliance:** Re-evaluate safety goggles quality (2 eye injuries from inadequate protection)
    - ⚠️ **Supervision:** Stricter supervision during high-risk activities (trench work, machinery)
    - ⚠️ **Near-Miss Reporting:** Very low reporting rate — hidden risks not being captured
    - ⚠️ **Training:** Required supervisor training (Construction Regulations, Scaffold Inspector, WAH)
    """)

    st.write("")
    st.markdown("#### 5. Division Breakdown")
    div_report = pd.DataFrame({
        "Division": ["Civils", "Workshop", "Building", "Structures", "Asphalt"],
        "Hours": [0, 0, 0, 0, 0],
        "IODs": [8, 2, 1, 1, 1],
        "LTIs": [4, 0, 1, 0, 1],
        "TIFR": [0, 0, 0, 0, 0],
        "LTIFR": [0, 0, 0, 0, 0]
    })
    st.dataframe(div_report, use_container_width=True, hide_index=True)

    # Export options
    st.write("")
    col_ex1, col_ex2 = st.columns(2)
    with col_ex1:
        st.download_button("📄 Download as PDF", b"PDF placeholder", "EHS_Report_Mar_2026.pdf", "application/pdf")
    with col_ex2:
        report_excel = BytesIO()
        div_report.to_excel(report_excel, index=False, sheet_name='Report')
        st.download_button("📊 Download as Excel", report_excel.getvalue(), "EHS_Report_Mar_2026.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

# ─── SETTINGS PAGE ───
elif page == "⚙️ Settings":
    st.markdown("<div class='main-header'>Settings</div>", unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["Company Setup", "Sites & Divisions", "Targets & Alerts"])

    with tab1:
        st.markdown("### Company Information")
        company_name = st.text_input("Company Name", value="Amandla Construction")
        fy_start = st.selectbox("Financial Year Start", ["March", "January", "April"])
        st.text_input("SHEQ Officer", value="Kumble Mati")

        st.markdown("### Report Configuration")
        st.selectbox("Reporting Period", ["Monthly", "Quarterly", "Yearly"])
        st.text_input("Auto-Email Recipients", value="safety@amandla.co.za")
        st.selectbox("Generate Report On", ["1st of month", "5th of month", "Manual only"])

    with tab2:
        st.markdown("### Site Management")
        sites_df = pd.DataFrame(st.session_state.sites)
        st.dataframe(sites_df, use_container_width=True, hide_index=True)

        with st.form("add_site"):
            st.markdown("#### Add New Site")
            col_s1, col_s2 = st.columns(2)
            with col_s1:
                new_code = st.text_input("Site Code (e.g., D588)")
                new_name = st.text_input("Site Name")
            with col_s2:
                new_div = st.selectbox("Division", ["Civils", "Structures", "Building", "Workshop", "Asphalt", "Admin"])
                new_status = st.selectbox("Status", ["Active", "On Hold", "Completed"])
            if st.form_submit_button("Add Site"):
                st.session_state.sites.append({"code": new_code, "name": new_name, "division": new_div, "status": new_status})
                st.success(f"✅ Added site: {new_name}")
                st.rerun()

    with tab3:
        st.markdown("### Safety Targets")
        col_t1, col_t2 = st.columns(2)
        with col_t1:
            st.number_input("TIFR Target", value=1.25, step=0.05)
            st.number_input("LTIFR Target", value=0.25, step=0.05)
        with col_t2:
            st.number_input("FIFR Target", value=0.0, step=0.05)
            st.number_input("Max Monthly IODs", value=5, step=1)

        st.markdown("### Alert Thresholds")
        st.checkbox("Alert when TIFR exceeds target", value=True)
        st.checkbox("Alert when LTIFR exceeds target", value=True)
        st.checkbox("Alert on fatality (immediate)", value=True)
        st.checkbox("Alert on overdue incident investigation (>7 days)", value=True)

# ─── FOOTER ───
st.divider()
st.caption("🏗️ Amandla Construction EHS Dashboard | Built with Streamlit | v1.0 Prototype")
