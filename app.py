import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, date
import json
import os

# ─── PAGE CONFIG ───
st.set_page_config(
    page_title="Amandla EHS Management System",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── CUSTOM CSS ───
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1f4e79;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #555;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .metric-value {
        font-size: 2.5rem;
        font-weight: bold;
    }
    .metric-label {
        font-size: 0.9rem;
        opacity: 0.9;
    }
    .highlight-box {
        background-color: #fff3cd;
        border: 1px solid #ffc107;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .filter-section {
        background-color: #f8f9fa;
        border-radius: 8px;
        padding: 1rem;
        margin-bottom: 1rem;
        border: 1px solid #dee2e6;
    }
    .home-card {
        text-align: center;
        padding: 1.5rem;
        border: 2px solid #e0e0e0;
        border-radius: 10px;
        margin: 0.5rem;
        transition: all 0.3s;
    }
    .home-card:hover {
        border-color: #1f4e79;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# ─── DATA PERSISTENCE ───
DATA_FILE = "ehs_data.json"

if "ehs_data" not in st.session_state:
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            st.session_state.ehs_data = json.load(f)
    else:
        st.session_state.ehs_data = {
            "incidents": [],
            "sites": [],
            "employees": [],
            "man_hours": []
        }

def save_data():
    with open(DATA_FILE, "w") as f:
        json.dump(st.session_state.ehs_data, f, indent=2, default=str)

# ─── SAMPLE DATA ───
def load_sample_data():
    sample_incidents = [
        {
            "id": "INC-2021-001", "date": "2021-03-15", "site": "Site A", "division": "Construction",
            "type": "First Aid Case", "description": "Cut on hand while handling material", 
            "severity": "Low", "body_part": "Hand", "days_lost": 0, "reported_by": "J. Smith",
            "status": "Closed", "contractor": "Amandla", "year": 2021,
            "employee_name": "John Doe", "employment_type": "Permanent",
            "preventative_action": "Provided cut-resistant gloves", "cause": "Cuts and Wounds"
        },
        {
            "id": "INC-2021-002", "date": "2021-06-22", "site": "Site B", "division": "Engineering",
            "type": "MTC", "description": "Back strain from lifting", 
            "severity": "Medium", "body_part": "Back", "days_lost": 3, "reported_by": "M. Jones",
            "status": "Closed", "contractor": "Amandla", "year": 2021,
            "employee_name": "Mike Johnson", "employment_type": "LDC",
            "preventative_action": "Manual handling training provided", "cause": "Sprains and Strains"
        },
        {
            "id": "INC-2022-001", "date": "2022-01-10", "site": "Site A", "division": "Construction",
            "type": "LTI", "description": "Fall from scaffolding", 
            "severity": "High", "body_part": "Leg", "days_lost": 15, "reported_by": "P. Brown",
            "status": "Closed", "contractor": "BuildRight Pty", "year": 2022,
            "employee_name": "Peter Brown", "employment_type": "Subcontractor",
            "preventative_action": "Scaffolding inspection protocol updated", "cause": "Slip Trips"
        },
        {
            "id": "INC-2022-002", "date": "2022-04-05", "site": "Site C", "division": "Maintenance",
            "type": "First Aid Case", "description": "Eye irritation from dust", 
            "severity": "Low", "body_part": "Eye", "days_lost": 0, "reported_by": "S. Wilson",
            "status": "Closed", "contractor": "Amandla", "year": 2022,
            "employee_name": "Sam Wilson", "employment_type": "Permanent",
            "preventative_action": "Dust masks issued to all workers", "cause": "Chemical Burns"
        },
        {
            "id": "INC-2023-001", "date": "2023-02-14", "site": "Site B", "division": "Construction",
            "type": "LTI", "description": "Crushed finger in machinery", 
            "severity": "High", "body_part": "Hand", "days_lost": 7, "reported_by": "T. Davis",
            "status": "Open", "contractor": "SteelFix Ltd", "year": 2023,
            "employee_name": "Tom Davis", "employment_type": "Subcontractor",
            "preventative_action": "Machine guarding installed", "cause": "Caught Between"
        },
        {
            "id": "INC-2023-002", "date": "2023-07-20", "site": "Site D", "division": "Engineering",
            "type": "MTC", "description": "Chemical splash on arm", 
            "severity": "Medium", "body_part": "Arm", "days_lost": 1, "reported_by": "R. Green",
            "status": "Closed", "contractor": "Amandla", "year": 2023,
            "employee_name": "Rob Green", "employment_type": "Permanent",
            "preventative_action": "Chemical handling PPE upgraded", "cause": "Chemical Burns"
        },
        {
            "id": "INC-2024-001", "date": "2024-01-08", "site": "Site A", "division": "Construction",
            "type": "First Aid Case", "description": "Minor burn from welding spark", 
            "severity": "Low", "body_part": "Arm", "days_lost": 0, "reported_by": "K. White",
            "status": "Closed", "contractor": "Amandla", "year": 2024,
            "employee_name": "Kevin White", "employment_type": "LDC",
            "preventative_action": "Welding sleeves provided", "cause": "Struck Against"
        },
        {
            "id": "INC-2024-002", "date": "2024-03-12", "site": "Site E", "division": "Maintenance",
            "type": "LTI", "description": "Twisted ankle on uneven ground", 
            "severity": "Medium", "body_part": "Ankle", "days_lost": 5, "reported_by": "L. Black",
            "status": "Open", "contractor": "GroundWorks Inc", "year": 2024,
            "employee_name": "Luke Black", "employment_type": "Subcontractor",
            "preventative_action": "Site leveling completed", "cause": "Slip Trips"
        },
        {
            "id": "INC-2024-003", "date": "2024-05-30", "site": "Site C", "division": "Construction",
            "type": "MTC", "description": "Respiratory irritation from fumes", 
            "severity": "Medium", "body_part": "Lungs", "days_lost": 2, "reported_by": "N. Gray",
            "status": "Closed", "contractor": "Amandla", "year": 2024,
            "employee_name": "Nick Gray", "employment_type": "Permanent",
            "preventative_action": "Ventilation system installed", "cause": "Chemical Burns"
        },
        {
            "id": "INC-2025-001", "date": "2025-01-15", "site": "Site B", "division": "Engineering",
            "type": "First Aid Case", "description": "Small cut from sharp edge", 
            "severity": "Low", "body_part": "Finger", "days_lost": 0, "reported_by": "O. Red",
            "status": "Open", "contractor": "BuildRight Pty", "year": 2025,
            "employee_name": "Oscar Red", "employment_type": "Subcontractor",
            "preventative_action": "Edge guards installed", "cause": "Cuts and Wounds"
        },
        {
            "id": "INC-2025-002", "date": "2025-04-22", "site": "Site D", "division": "Construction",
            "type": "LTI", "description": "Knee injury from slip", 
            "severity": "High", "body_part": "Knee", "days_lost": 12, "reported_by": "Q. Blue",
            "status": "Open", "contractor": "Amandla", "year": 2025,
            "employee_name": "Quinn Blue", "employment_type": "Permanent",
            "preventative_action": "Anti-slip mats placed", "cause": "Slip Trips"
        },
        {
            "id": "INC-2026-001", "date": "2026-01-15", "site": "Site A", "division": "Construction",
            "type": "First Aid Case", "description": "Minor scratch from wire brush", 
            "severity": "Low", "body_part": "Hand", "days_lost": 0, "reported_by": "A. Green",
            "status": "Open", "contractor": "Amandla", "year": 2026,
            "employee_name": "Alex Green", "employment_type": "Permanent",
            "preventative_action": "Wire brush inspection protocol", "cause": "Cuts and Wounds"
        },
        {
            "id": "INC-2026-002", "date": "2026-03-10", "site": "Site B", "division": "Engineering",
            "type": "LTI", "description": "Shoulder injury from overhead work", 
            "severity": "High", "body_part": "Shoulder", "days_lost": 8, "reported_by": "B. Yellow",
            "status": "Open", "contractor": "Amandla", "year": 2026,
            "employee_name": "Ben Yellow", "employment_type": "LDC",
            "preventative_action": "Overhead work rotation schedule", "cause": "Sprains and Strains"
        },
        {
            "id": "INC-2026-003", "date": "2026-05-20", "site": "Site C", "division": "Maintenance",
            "type": "MTC", "description": "Burn from hot pipe contact", 
            "severity": "Medium", "body_part": "Arm", "days_lost": 2, "reported_by": "C. Orange",
            "status": "Open", "contractor": "Amandla", "year": 2026,
            "employee_name": "Chris Orange", "employment_type": "Permanent",
            "preventative_action": "Heat warning signs posted", "cause": "Struck Against"
        },
    ]

    sample_sites = [
        {"name": "Site A", "location": "Johannesburg", "status": "Active", "start_date": "2020-01-01", "end_date": None, "division": "Amandla"},
        {"name": "Site B", "location": "Pretoria", "status": "Active", "start_date": "2020-03-01", "end_date": None, "division": "Amandla"},
        {"name": "Site C", "location": "Cape Town", "status": "Active", "start_date": "2021-06-01", "end_date": None, "division": "Amandla"},
        {"name": "Site D", "location": "Durban", "status": "Active", "start_date": "2022-01-01", "end_date": None, "division": "Amandla"},
        {"name": "Site E", "location": "Port Elizabeth", "status": "Completed", "start_date": "2022-05-01", "end_date": "2024-12-31", "division": "Subcontractor"},
        {"name": "Site F", "location": "Bloemfontein", "status": "Completed", "start_date": "2021-02-01", "end_date": "2023-08-31", "division": "Subcontractor"},
    ]

    sample_man_hours = [
        {"site": "Site A", "year": 2021, "month": 1, "amandla_hours": 8000, "subcontractor_hours": 3000},
        {"site": "Site A", "year": 2022, "month": 1, "amandla_hours": 8500, "subcontractor_hours": 3500},
        {"site": "Site A", "year": 2023, "month": 1, "amandla_hours": 9000, "subcontractor_hours": 4000},
        {"site": "Site A", "year": 2024, "month": 1, "amandla_hours": 9200, "subcontractor_hours": 4200},
        {"site": "Site A", "year": 2025, "month": 1, "amandla_hours": 9500, "subcontractor_hours": 4500},
        {"site": "Site A", "year": 2026, "month": 1, "amandla_hours": 9800, "subcontractor_hours": 4800},
        {"site": "Site B", "year": 2021, "month": 1, "amandla_hours": 6000, "subcontractor_hours": 2000},
        {"site": "Site B", "year": 2022, "month": 1, "amandla_hours": 6500, "subcontractor_hours": 2500},
        {"site": "Site B", "year": 2023, "month": 1, "amandla_hours": 7000, "subcontractor_hours": 3000},
        {"site": "Site B", "year": 2024, "month": 1, "amandla_hours": 7200, "subcontractor_hours": 3200},
        {"site": "Site B", "year": 2025, "month": 1, "amandla_hours": 7500, "subcontractor_hours": 3500},
        {"site": "Site B", "year": 2026, "month": 1, "amandla_hours": 7800, "subcontractor_hours": 3800},
        {"site": "Site C", "year": 2021, "month": 1, "amandla_hours": 5000, "subcontractor_hours": 1500},
        {"site": "Site C", "year": 2022, "month": 1, "amandla_hours": 5500, "subcontractor_hours": 1800},
        {"site": "Site C", "year": 2023, "month": 1, "amandla_hours": 6000, "subcontractor_hours": 2000},
        {"site": "Site C", "year": 2024, "month": 1, "amandla_hours": 6200, "subcontractor_hours": 2200},
        {"site": "Site C", "year": 2025, "month": 1, "amandla_hours": 6500, "subcontractor_hours": 2500},
        {"site": "Site C", "year": 2026, "month": 1, "amandla_hours": 6800, "subcontractor_hours": 2800},
        {"site": "Site D", "year": 2022, "month": 1, "amandla_hours": 4000, "subcontractor_hours": 1000},
        {"site": "Site D", "year": 2023, "month": 1, "amandla_hours": 4500, "subcontractor_hours": 1200},
        {"site": "Site D", "year": 2024, "month": 1, "amandla_hours": 4800, "subcontractor_hours": 1500},
        {"site": "Site D", "year": 2025, "month": 1, "amandla_hours": 5000, "subcontractor_hours": 1800},
        {"site": "Site D", "year": 2026, "month": 1, "amandla_hours": 5200, "subcontractor_hours": 2000},
        {"site": "Site E", "year": 2022, "month": 1, "amandla_hours": 0, "subcontractor_hours": 5000},
        {"site": "Site E", "year": 2023, "month": 1, "amandla_hours": 0, "subcontractor_hours": 5500},
        {"site": "Site E", "year": 2024, "month": 1, "amandla_hours": 0, "subcontractor_hours": 6000},
        {"site": "Site F", "year": 2021, "month": 1, "amandla_hours": 0, "subcontractor_hours": 4000},
        {"site": "Site F", "year": 2022, "month": 1, "amandla_hours": 0, "subcontractor_hours": 4500},
        {"site": "Site F", "year": 2023, "month": 1, "amandla_hours": 0, "subcontractor_hours": 3000},
    ]

    st.session_state.ehs_data["incidents"] = sample_incidents
    st.session_state.ehs_data["sites"] = sample_sites
    st.session_state.ehs_data["man_hours"] = sample_man_hours
    save_data()

# Load sample data if empty
if not st.session_state.ehs_data.get("incidents"):
    load_sample_data()

# ─── HELPER FUNCTIONS ───
def get_all_years():
    incidents = st.session_state.ehs_data.get("incidents", [])
    years = sorted(set([inc["year"] for inc in incidents if "year" in inc]), reverse=True)
    if not years:
        years = [datetime.now().year]
    return years

def get_active_sites():
    return [s["name"] for s in st.session_state.ehs_data.get("sites", []) if s.get("status") == "Active"]

def get_all_sites():
    return [s["name"] for s in st.session_state.ehs_data.get("sites", [])]

def get_sites_by_status(include_completed=False):
    sites = st.session_state.ehs_data.get("sites", [])
    if include_completed:
        return sites
    return [s for s in sites if s.get("status") == "Active"]

def calculate_stats(incidents, man_hours_data, year_filter=None, contractor_filter="Combined", site_filter=None):
    filtered_incidents = list(incidents)

    if year_filter:
        if isinstance(year_filter, list):
            filtered_incidents = [i for i in filtered_incidents if i.get("year") in year_filter]
        else:
            filtered_incidents = [i for i in filtered_incidents if i.get("year") == year_filter]

    if contractor_filter != "Combined":
        if contractor_filter == "Amandla":
            filtered_incidents = [i for i in filtered_incidents if i.get("contractor") == "Amandla" or i.get("division") == "Amandla"]
        elif contractor_filter == "Subcontractor":
            filtered_incidents = [i for i in filtered_incidents if i.get("contractor") != "Amandla" and i.get("division") == "Subcontractor"]

    if site_filter and site_filter != "All Sites":
        filtered_incidents = [i for i in filtered_incidents if i.get("site") == site_filter]

    filtered_hours = list(man_hours_data)
    if year_filter:
        if isinstance(year_filter, list):
            filtered_hours = [h for h in filtered_hours if h.get("year") in year_filter]
        else:
            filtered_hours = [h for h in filtered_hours if h.get("year") == year_filter]

    if site_filter and site_filter != "All Sites":
        filtered_hours = [h for h in filtered_hours if h.get("site") == site_filter]

    if contractor_filter == "Amandla":
        total_hours = sum(h.get("amandla_hours", 0) for h in filtered_hours)
    elif contractor_filter == "Subcontractor":
        total_hours = sum(h.get("subcontractor_hours", 0) for h in filtered_hours)
    else:
        total_hours = sum(h.get("amandla_hours", 0) + h.get("subcontractor_hours", 0) for h in filtered_hours)

    total_injuries = len(filtered_incidents)
    lti_count = len([i for i in filtered_incidents if i.get("type") == "LTI"])
    medical_treatment = len([i for i in filtered_incidents if i.get("type") == "MTC"])
    first_aid = len([i for i in filtered_incidents if i.get("type") == "First Aid Case"])
    total_days_lost = sum(i.get("days_lost", 0) for i in filtered_incidents)

    million_hours = total_hours / 1000000.0 if total_hours > 0 else 1
    tifr = (total_injuries / million_hours) if million_hours > 0 else 0
    ltifr = (lti_count / million_hours) if million_hours > 0 else 0

    return {
        "total_hours": total_hours,
        "total_injuries": total_injuries,
        "lti_count": lti_count,
        "medical_treatment": medical_treatment,
        "first_aid": first_aid,
        "total_days_lost": total_days_lost,
        "tifr": tifr,
        "ltifr": ltifr,
        "incidents": filtered_incidents
    }

def calculate_site_breakdown(incidents, man_hours_data, year_filter=None, contractor_filter="Combined"):
    sites = get_sites_by_status(include_completed=True)
    breakdown = []

    for site in sites:
        site_name = site["name"]
        site_status = site.get("status", "Active")

        site_incidents = [i for i in incidents if i.get("site") == site_name]
        if year_filter:
            if isinstance(year_filter, list):
                site_incidents = [i for i in site_incidents if i.get("year") in year_filter]
            else:
                site_incidents = [i for i in site_incidents if i.get("year") == year_filter]

        if contractor_filter != "Combined":
            if contractor_filter == "Amandla":
                site_incidents = [i for i in site_incidents if i.get("contractor") == "Amandla" or i.get("division") == "Amandla"]
            elif contractor_filter == "Subcontractor":
                site_incidents = [i for i in site_incidents if i.get("contractor") != "Amandla" and i.get("division") == "Subcontractor"]

        site_hours = [h for h in man_hours_data if h.get("site") == site_name]
        if year_filter:
            if isinstance(year_filter, list):
                site_hours = [h for h in site_hours if h.get("year") in year_filter]
            else:
                site_hours = [h for h in site_hours if h.get("year") == year_filter]

        if contractor_filter == "Amandla":
            total_hours = sum(h.get("amandla_hours", 0) for h in site_hours)
        elif contractor_filter == "Subcontractor":
            total_hours = sum(h.get("subcontractor_hours", 0) for h in site_hours)
        else:
            total_hours = sum(h.get("amandla_hours", 0) + h.get("subcontractor_hours", 0) for h in site_hours)

        total_injuries = len(site_incidents)
        lti_count = len([i for i in site_incidents if i.get("type") == "LTI"])
        total_days_lost = sum(i.get("days_lost", 0) for i in site_incidents)

        million_hours = total_hours / 1000000.0 if total_hours > 0 else 1
        tifr = (total_injuries / million_hours) if million_hours > 0 else 0
        ltifr = (lti_count / million_hours) if million_hours > 0 else 0

        breakdown.append({
            "site": site_name,
            "status": site_status,
            "location": site.get("location", ""),
            "total_hours": total_hours,
            "total_injuries": total_injuries,
            "lti_count": lti_count,
            "days_lost": total_days_lost,
            "tifr": round(tifr, 2),
            "ltifr": round(ltifr, 2)
        })

    return breakdown

# ─── SIDEBAR NAVIGATION ───
st.sidebar.markdown("## 🛡️ Amandla EHS")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigation",
    ["Home", "Dashboard", "Incident Register", "Add Incident", "Site Management", "Import Data", "Settings"]
)

# ─── HOME PAGE ───
if page == "Home":
    st.markdown('<div class="main-header">Amandla EHS Management System</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Occupational Health & Safety Dashboard</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="home-card" style="border-color: #1f4e79;">
            <h2>📊</h2>
            <h4>View Dashboard</h4>
            <p style="font-size: 0.85rem;">Comprehensive safety statistics, trends, and analytics</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="home-card" style="border-color: #f5576c;">
            <h2>🚨</h2>
            <h4>Report Incident</h4>
            <p style="font-size: 0.85rem;">Log new incidents, injuries, and near misses</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="home-card" style="border-color: #43e97b;">
            <h2>📤</h2>
            <h4>Import Data</h4>
            <p style="font-size: 0.85rem;">Upload site hours and bulk incident data</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # YTD Summary
    current_year = datetime.now().year
    ytd_stats = calculate_stats(
        st.session_state.ehs_data.get("incidents", []),
        st.session_state.ehs_data.get("man_hours", []),
        year_filter=current_year,
        contractor_filter="Combined"
    )

    st.subheader("Year-to-Date Summary (%d)" % current_year)

    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        st.metric("Total Incidents", ytd_stats["total_injuries"])
    with c2:
        st.metric("Lost Time Injuries", ytd_stats["lti_count"])
    with c3:
        st.metric("Days Lost", ytd_stats["total_days_lost"])
    with c4:
        st.metric("TIFR", "%.2f" % ytd_stats['tifr'])
    with c5:
        st.metric("LTIFR", "%.2f" % ytd_stats['ltifr'])

    # Recent Activity
    st.markdown("---")
    st.subheader("Recent Activity")

    recent_incidents = sorted(
        st.session_state.ehs_data.get("incidents", []),
        key=lambda x: x.get("date", ""),
        reverse=True
    )[:5]

    if recent_incidents:
        df_recent = pd.DataFrame(recent_incidents)
        df_recent = df_recent[["id", "date", "site", "type", "severity", "status"]]
        st.dataframe(df_recent, use_container_width=True, hide_index=True)
    else:
        st.info("No recent incidents recorded.")

# ─── DASHBOARD ───
elif page == "Dashboard":
    st.markdown('<div class="main-header">Safety Statistics Dashboard</div>', unsafe_allow_html=True)

    # FILTERS
    st.markdown('<div class="filter-section">', unsafe_allow_html=True)

    col_f1, col_f2, col_f3 = st.columns(3)

    with col_f1:
        all_years = get_all_years()
        year_options = ["All Years (Cumulative)", "YTD"] + [str(y) for y in all_years] + ["Last 3 Years", "Last 4 Years"]
        selected_year = st.selectbox("Year Filter", year_options, index=1)

    with col_f2:
        contractor_view = st.selectbox(
            "Contractor View", 
            ["Combined", "Amandla", "Subcontractor"],
            index=0
        )

    with col_f3:
        include_completed = st.checkbox("Show Completed Sites", value=False)
        sites_list = [s["name"] for s in get_sites_by_status(include_completed=include_completed)]
        site_options = ["All Sites"] + sites_list
        selected_site = st.selectbox("Site Filter", site_options, index=0)

    st.markdown('</div>', unsafe_allow_html=True)

    # Parse year filter
    if selected_year == "YTD":
        year_filter = datetime.now().year
    elif selected_year == "All Years (Cumulative)":
        year_filter = None
    elif selected_year == "Last 3 Years":
        year_filter = list(range(datetime.now().year - 2, datetime.now().year + 1))
    elif selected_year == "Last 4 Years":
        year_filter = list(range(datetime.now().year - 3, datetime.now().year + 1))
    else:
        year_filter = int(selected_year)

    # Calculate stats
    incidents = st.session_state.ehs_data.get("incidents", [])
    man_hours = st.session_state.ehs_data.get("man_hours", [])

    stats = calculate_stats(incidents, man_hours, year_filter, contractor_view, selected_site)

    # KPI CARDS
    st.subheader("Key Performance Indicators")

    kpi1, kpi2, kpi3, kpi4, kpi5, kpi6 = st.columns(6)

    with kpi1:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">%d</div>
            <div class="metric-label">Total Incidents</div>
        </div>
        """ % stats['total_injuries'], unsafe_allow_html=True)

    with kpi2:
        st.markdown("""
        <div class="metric-card" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);">
            <div class="metric-value">%d</div>
            <div class="metric-label">Lost Time Injuries</div>
        </div>
        """ % stats['lti_count'], unsafe_allow_html=True)

    with kpi3:
        st.markdown("""
        <div class="metric-card" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);">
            <div class="metric-value">%d</div>
            <div class="metric-label">Days Lost</div>
        </div>
        """ % stats['total_days_lost'], unsafe_allow_html=True)

    with kpi4:
        st.markdown("""
        <div class="metric-card" style="background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);">
            <div class="metric-value">%s</div>
            <div class="metric-label">Man Hours Worked</div>
        </div>
        """ % "{:,}".format(stats['total_hours']), unsafe_allow_html=True)

    with kpi5:
        st.markdown("""
        <div class="metric-card" style="background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);">
            <div class="metric-value">%.2f</div>
            <div class="metric-label">TIFR</div>
        </div>
        """ % stats['tifr'], unsafe_allow_html=True)

    with kpi6:
        st.markdown("""
        <div class="metric-card" style="background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);">
            <div class="metric-value">%.2f</div>
            <div class="metric-label">LTIFR</div>
        </div>
        """ % stats['ltifr'], unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # CHARTS - TABS
    tab1, tab2, tab3, tab4 = st.tabs(["Trends", "Site Breakdown", "Incident Types", "Year Comparison"])

    with tab1:
        col_t1, col_t2 = st.columns(2)

        with col_t1:
            if stats["incidents"]:
                df_monthly = pd.DataFrame(stats["incidents"])
                df_monthly["date"] = pd.to_datetime(df_monthly["date"])
                df_monthly["month"] = df_monthly["date"].dt.strftime("%Y-%m")

                monthly_counts = df_monthly.groupby("month").size().reset_index(name="count")
                monthly_counts = monthly_counts.sort_values("month")

                fig = px.line(monthly_counts, x="month", y="count", 
                             title="Incident Trend Over Time",
                             labels={"month": "Month", "count": "Number of Incidents"},
                             markers=True)
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No incident data available for trend analysis.")

        with col_t2:
            if stats["incidents"]:
                df_sev = pd.DataFrame(stats["incidents"])
                sev_counts = df_sev["severity"].value_counts().reset_index()
                sev_counts.columns = ["severity", "count"]

                fig = px.pie(sev_counts, values="count", names="severity",
                            title="Incident Severity Distribution",
                            color_discrete_sequence=px.colors.sequential.RdBu)
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No severity data available.")

    with tab2:
        breakdown = calculate_site_breakdown(incidents, man_hours, year_filter, contractor_view)

        if breakdown:
            df_breakdown = pd.DataFrame(breakdown)

            if selected_site != "All Sites":
                df_breakdown = df_breakdown[df_breakdown["site"] == selected_site]

            if not include_completed:
                df_breakdown = df_breakdown[df_breakdown["status"] == "Active"]

            if not df_breakdown.empty:
                st.dataframe(
                    df_breakdown[["site", "status", "location", "total_hours", "total_injuries", 
                                 "lti_count", "days_lost", "tifr", "ltifr"]],
                    use_container_width=True,
                    hide_index=True
                )

                fig = px.bar(df_breakdown, x="site", y=["total_injuries", "lti_count"],
                            title="Incidents by Site",
                            labels={"value": "Count", "site": "Site", "variable": "Type"},
                            barmode="group",
                            color_discrete_map={"total_injuries": "#667eea", "lti_count": "#f5576c"})
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)

                fig2 = px.bar(df_breakdown, x="site", y=["tifr", "ltifr"],
                             title="TIFR & LTIFR by Site",
                             labels={"value": "Rate", "site": "Site", "variable": "Rate Type"},
                             barmode="group",
                             color_discrete_map={"tifr": "#fa709a", "ltifr": "#4facfe"})
                fig2.update_layout(height=400)
                st.plotly_chart(fig2, use_container_width=True)
            else:
                st.info("No site data matches the current filters.")
        else:
            st.info("No site breakdown data available.")

    with tab3:
        if stats["incidents"]:
            df_types = pd.DataFrame(stats["incidents"])
            type_counts = df_types["type"].value_counts().reset_index()
            type_counts.columns = ["type", "count"]

            col_ty1, col_ty2 = st.columns(2)

            with col_ty1:
                fig = px.bar(type_counts, x="type", y="count",
                            title="Incidents by Type",
                            labels={"type": "Incident Type", "count": "Count"},
                            color="type",
                            color_discrete_sequence=px.colors.qualitative.Set3)
                fig.update_layout(height=400, showlegend=False)
                st.plotly_chart(fig, use_container_width=True)

            with col_ty2:
                body_part_counts = df_types["body_part"].value_counts().reset_index()
                body_part_counts.columns = ["body_part", "count"]

                fig = px.bar(body_part_counts, x="body_part", y="count",
                            title="Injuries by Body Part",
                            labels={"body_part": "Body Part", "count": "Count"},
                            color="body_part",
                            color_discrete_sequence=px.colors.qualitative.Pastel)
                fig.update_layout(height=400, showlegend=False)
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No incident type data available.")

    with tab4:
        all_years_data = []
        for yr in all_years:
            yr_stats = calculate_stats(incidents, man_hours, year_filter=yr, contractor_filter=contractor_view)
            all_years_data.append({
                "year": yr,
                "total_incidents": yr_stats["total_injuries"],
                "ltis": yr_stats["lti_count"],
                "days_lost": yr_stats["total_days_lost"],
                "tifr": yr_stats["tifr"],
                "ltifr": yr_stats["ltifr"],
                "hours": yr_stats["total_hours"]
            })

        if all_years_data:
            df_years = pd.DataFrame(all_years_data)

            col_y1, col_y2 = st.columns(2)

            with col_y1:
                fig = px.line(df_years, x="year", y=["total_incidents", "ltis"],
                             title="Incidents by Year",
                             labels={"year": "Year", "value": "Count", "variable": "Type"},
                             markers=True)
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)

            with col_y2:
                fig = px.line(df_years, x="year", y=["tifr", "ltifr"],
                             title="TIFR & LTIFR by Year",
                             labels={"year": "Year", "value": "Rate", "variable": "Rate Type"},
                             markers=True)
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)

            st.dataframe(df_years, use_container_width=True, hide_index=True)
        else:
            st.info("No multi-year data available for comparison.")

# ─── INCIDENT REGISTER ───
elif page == "Incident Register":
    st.markdown('<div class="main-header">Incident Register</div>', unsafe_allow_html=True)

    # Filters
    st.markdown('<div class="filter-section">', unsafe_allow_html=True)

    col_if1, col_if2, col_if3, col_if4 = st.columns(4)

    with col_if1:
        reg_year_filter = st.selectbox("Year", ["All"] + [str(y) for y in get_all_years()], index=0)

    with col_if2:
        reg_type_filter = st.selectbox("Type", ["All", "LTI", "MTC", "First Aid Case"], index=0)

    with col_if3:
        reg_status_filter = st.selectbox("Status", ["All", "Open", "Closed"], index=0)

    with col_if4:
        all_sites_list = ["All Sites"] + get_all_sites()
        reg_site_filter = st.selectbox("Site", all_sites_list, index=0)

    st.markdown('</div>', unsafe_allow_html=True)

    # Apply filters
    all_incidents = st.session_state.ehs_data.get("incidents", [])
    filtered = list(all_incidents)

    if reg_year_filter != "All":
        filtered = [i for i in filtered if str(i.get("year", "")) == reg_year_filter]

    if reg_type_filter != "All":
        filtered = [i for i in filtered if i.get("type") == reg_type_filter]

    if reg_status_filter != "All":
        filtered = [i for i in filtered if i.get("status") == reg_status_filter]

    if reg_site_filter != "All Sites":
        filtered = [i for i in filtered if i.get("site") == reg_site_filter]

    # Display
    if filtered:
        df_reg = pd.DataFrame(filtered)

        display_cols = ["date", "employee_name", "id", "site", "employment_type", "division", 
                       "description", "preventative_action", "body_part", "cause", "type", "days_lost"]
        available_cols = [c for c in display_cols if c in df_reg.columns]
        df_display = df_reg[available_cols]

        st.dataframe(df_display, use_container_width=True, hide_index=True)

        st.markdown("**Showing %d of %d total incidents**" % (len(filtered), len(all_incidents)))

        # Export option
        csv = df_display.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download as CSV",
            data=csv,
            file_name="incident_register_%s.csv" % datetime.now().strftime('%Y%m%d'),
            mime="text/csv"
        )
    else:
        st.info("No incidents match the selected filters.")

# ─── ADD INCIDENT ───
elif page == "Add Incident":
    st.markdown('<div class="main-header">Report New Incident</div>', unsafe_allow_html=True)

    with st.form("incident_form"):
        # Row 1
        col1, col2, col3 = st.columns(3)

        with col1:
            incident_date = st.date_input("Incident Date", value=date.today())

        with col2:
            current_year = datetime.now().year
            existing = [i for i in st.session_state.ehs_data.get("incidents", []) if i.get("year") == current_year]
            next_num = len(existing) + 1
            incident_id = "INC-%d-%03d" % (current_year, next_num)
            st.text_input("Incident ID", value=incident_id, disabled=True)

        with col3:
            site = st.selectbox("Site", get_all_sites())

        # Row 2 - Employee Info
        st.subheader("Employee Information")
        col_e1, col_e2, col_e3 = st.columns(3)

        with col_e1:
            employee_name = st.text_input("Employee Name & Surname")

        with col_e2:
            employment_type = st.selectbox("Employment Type", ["Permanent", "LDC", "Subcontractor"])

        with col_e3:
            division = st.selectbox("Division", ["Construction", "Engineering", "Maintenance", "Administration", "Safety", "Operations"])

        # Row 3 - Incident Details
        st.subheader("Incident Details")
        col_d1, col_d2, col_d3 = st.columns(3)

        with col_d1:
            incident_type = st.selectbox("Injury Type", ["LTI", "MTC", "First Aid Case"])

        with col_d2:
            cause = st.selectbox("Cause", [
                "Struck By", "Caught Between", "Snake & Insect Bites", "MVA",
                "Slip Trips", "Cuts and Wounds", "Dog Bites", "Sprains and Strains",
                "Chemical Burns", "Struck Against", "Criminal"
            ])

        with col_d3:
            body_part = st.selectbox("Body Part Affected", 
                                    ["Head", "Eye", "Arm", "Hand", "Finger", "Back", "Leg", "Knee", "Ankle", "Foot", "Multiple", "Other"])

        # Row 4 - Description & Actions
        col_a1, col_a2 = st.columns(2)

        with col_a1:
            description = st.text_area("Description of Incident", height=100)

        with col_a2:
            preventative_action = st.text_area("Preventative Action", height=100)

        # Row 5 - Days & Status
        col_s1, col_s2, col_s3 = st.columns(3)

        with col_s1:
            days_lost = st.number_input("Days Away (Number)", min_value=0, value=0)

        with col_s2:
            severity = st.selectbox("Severity", ["Low", "Medium", "High", "Critical"])

        with col_s3:
            reported_by = st.text_input("Reported By")

        submitted = st.form_submit_button("Submit Incident", use_container_width=True)

        if submitted:
            if not description:
                st.error("Please provide a description of the incident.")
            elif not employee_name:
                st.error("Please provide the employee name.")
            else:
                new_incident = {
                    "id": incident_id,
                    "date": incident_date.strftime("%Y-%m-%d"),
                    "site": site,
                    "type": incident_type,
                    "severity": severity,
                    "body_part": body_part,
                    "contractor": "Amandla" if employment_type != "Subcontractor" else "Subcontractor",
                    "division": division,
                    "days_lost": days_lost,
                    "reported_by": reported_by,
                    "description": description,
                    "preventative_action": preventative_action,
                    "status": "Open",
                    "year": current_year,
                    "employee_name": employee_name,
                    "employment_type": employment_type,
                    "cause": cause
                }

                st.session_state.ehs_data["incidents"].append(new_incident)
                save_data()

                st.success("Incident %s recorded successfully!" % incident_id)
                st.balloons()

# ─── SITE MANAGEMENT ───
elif page == "Site Management":
    st.markdown('<div class="main-header">Site Management</div>', unsafe_allow_html=True)

    tab_sites, tab_add_site = st.tabs(["Manage Sites", "Add New Site"])

    with tab_sites:
        sites = st.session_state.ehs_data.get("sites", [])

        if sites:
            df_sites = pd.DataFrame(sites)

            status_filter = st.selectbox("Filter by Status", ["All", "Active", "Completed"], index=0)
            if status_filter != "All":
                df_sites = df_sites[df_sites["status"] == status_filter]

            st.dataframe(df_sites, use_container_width=True, hide_index=True)

            st.subheader("Update Site Status")
            col_site1, col_site2 = st.columns(2)

            with col_site1:
                site_to_update = st.selectbox("Select Site", [s["name"] for s in sites])

            with col_site2:
                new_status = st.selectbox("New Status", ["Active", "Completed"])

            if st.button("Update Status", use_container_width=True):
                for s in sites:
                    if s["name"] == site_to_update:
                        s["status"] = new_status
                        if new_status == "Completed":
                            s["end_date"] = date.today().strftime("%Y-%m-%d")
                        break
                save_data()
                st.success("%s status updated to %s" % (site_to_update, new_status))
        else:
            st.info("No sites registered yet.")

    with tab_add_site:
        with st.form("site_form"):
            site_name = st.text_input("Site Name")
            site_location = st.text_input("Location")
            site_division = st.selectbox("Division", ["Amandla", "Subcontractor"])
            site_start = st.date_input("Start Date", value=date.today())

            submitted = st.form_submit_button("Add Site", use_container_width=True)

            if submitted:
                if not site_name or not site_location:
                    st.error("Please fill in all required fields.")
                else:
                    new_site = {
                        "name": site_name,
                        "location": site_location,
                        "status": "Active",
                        "start_date": site_start.strftime("%Y-%m-%d"),
                        "end_date": None,
                        "division": site_division
                    }
                    st.session_state.ehs_data["sites"].append(new_site)
                    save_data()
                    st.success("Site '%s' added successfully!" % site_name)

# ─── IMPORT DATA ───
elif page == "Import Data":
    st.markdown('<div class="main-header">Import Data</div>', unsafe_allow_html=True)

    tab_hours, tab_incidents = st.tabs(["Import Man Hours", "Bulk Import Incidents"])

    with tab_hours:
        st.markdown("""
        <div class="highlight-box">
        <strong>Expected CSV Format:</strong><br>
        site, year, month, amandla_hours, subcontractor_hours<br><br>
        <em>Example:</em><br>
        Site A, 2024, 1, 8000, 3000
        </div>
        """, unsafe_allow_html=True)

        uploaded_hours = st.file_uploader("Upload Man Hours CSV", type=["csv"])

        if uploaded_hours:
            df_hours = pd.read_csv(uploaded_hours)
            st.write("Preview:")
            st.dataframe(df_hours.head(), use_container_width=True)

            if st.button("Import Man Hours", use_container_width=True):
                records = df_hours.to_dict('records')
                st.session_state.ehs_data["man_hours"].extend(records)
                save_data()
                st.success("Imported %d man hour records!" % len(records))

    with tab_incidents:
        st.markdown("""
        <div class="highlight-box">
        <strong>Expected CSV Format:</strong><br>
        id, date, site, type, severity, body_part, contractor, days_lost, description, status<br><br>
        <em>Example:</em><br>
        INC-2024-001, 2024-01-15, Site A, First Aid, Low, Hand, Amandla, 0, Cut on hand, Closed
        </div>
        """, unsafe_allow_html=True)

        uploaded_incidents = st.file_uploader("Upload Incidents CSV", type=["csv"])

        if uploaded_incidents:
            df_inc = pd.read_csv(uploaded_incidents)
            st.write("Preview:")
            st.dataframe(df_inc.head(), use_container_width=True)

            if st.button("Import Incidents", use_container_width=True):
                records = df_inc.to_dict('records')
                for r in records:
                    r["year"] = pd.to_datetime(r["date"]).year
                    r["division"] = "Amandla" if r.get("contractor") == "Amandla" else "Subcontractor"
                st.session_state.ehs_data["incidents"].extend(records)
                save_data()
                st.success("Imported %d incident records!" % len(records))

# ─── SETTINGS ───
elif page == "Settings":
    st.markdown('<div class="main-header">System Settings</div>', unsafe_allow_html=True)

    col_set1, col_set2 = st.columns(2)

    with col_set1:
        st.subheader("Data Management")

        if st.button("Backup Data to JSON", use_container_width=True):
            save_data()
            st.success("Data backed up successfully!")

        if st.button("Reload Sample Data", use_container_width=True):
            load_sample_data()
            st.success("Sample data reloaded!")

        if st.button("Clear All Data", use_container_width=True):
            st.session_state.ehs_data = {"incidents": [], "sites": [], "employees": [], "man_hours": []}
            save_data()
            st.warning("All data cleared!")

    with col_set2:
        st.subheader("Statistics Summary")

        total_incidents = len(st.session_state.ehs_data.get("incidents", []))
        total_sites = len(st.session_state.ehs_data.get("sites", []))
        total_hours = len(st.session_state.ehs_data.get("man_hours", []))

        st.metric("Total Incidents", total_incidents)
        st.metric("Total Sites", total_sites)
        st.metric("Man Hour Records", total_hours)

        st.markdown("---")
        st.caption("Last updated: %s" % datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

# ─── FOOTER ───
st.sidebar.markdown("---")
st.sidebar.caption("Amandla EHS v2.0")
st.sidebar.caption("Built with Streamlit")
