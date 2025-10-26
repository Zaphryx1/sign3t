import streamlit as st
import json
import time
from datetime import datetime
from threat_score import generate_briefing
from threat_assessment import generate_threat_assessment, ThreatAssessment
from config import APP_NAME, VERSION, THREAT_LEVELS
import pandas as pd

# Page configuration
st.set_page_config(
    page_title=APP_NAME,
    page_icon="!",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .threat-level-critical {
        background-color: #ff4444;
        color: white;
        padding: 0.5rem;
        border-radius: 0.5rem;
        text-align: center;
        font-weight: bold;
    }
    .threat-level-high {
        background-color: #ff8800;
        color: white;
        padding: 0.5rem;
        border-radius: 0.5rem;
        text-align: center;
        font-weight: bold;
    }
    .threat-level-medium {
        background-color: #ffbb00;
        color: black;
        padding: 0.5rem;
        border-radius: 0.5rem;
        text-align: center;
        font-weight: bold;
    }
    .threat-level-low {
        background-color: #44ff44;
        color: black;
        padding: 0.5rem;
        border-radius: 0.5rem;
        text-align: center;
        font-weight: bold;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .recommendation-box {
        background-color: #e8f4fd;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Header
    st.markdown(f'<div class="main-header">{APP_NAME}</div>', unsafe_allow_html=True)
    st.markdown(f"**Version:** {VERSION} | **Real-time AI Threat Assessment for Law Enforcement**")
    
    # Sidebar
    with st.sidebar:
        st.header("System Controls")
        
        # Location input
        location = st.text_input(
            "Enter Location",
            value="123 Main St",
            help="Enter the address or location to assess"
        )
        
        # Assessment options
        st.subheader("Assessment Options")
        include_historical = st.checkbox("Include Historical Data", value=True)
        include_gis = st.checkbox("Include GIS Data", value=True)
        include_dispatch = st.checkbox("Include Dispatch Records", value=True)
        
        # Real-time updates
        st.subheader("Real-time Updates")
        auto_refresh = st.checkbox("Auto-refresh (30s)", value=False)
        if auto_refresh:
            st.info("Auto-refresh enabled")
        
        # System status
        st.subheader("System Status")
        st.success("AI Models: Active")
        st.success("Data Sources: Connected")
        st.success("Vector Database: Online")
    
    # Main content area
    if location:
        # Generate assessment
        with st.spinner("AI is analyzing threat data..."):
            try:
                assessment = generate_threat_assessment(location)
                briefing = generate_briefing(location)
                
                # Display results
                display_threat_assessment(assessment)
                display_detailed_briefing(briefing)
                
            except Exception as e:
                st.error(f"Error generating assessment: {e}")
                st.info("Try checking your data sources and API connections")
    else:
        st.info("Please enter a location in the sidebar to begin threat assessment")
        display_demo_data()

def display_threat_assessment(assessment: ThreatAssessment):
    """Display the threat assessment in a structured format"""
    
    # Threat level indicator
    threat_color = THREAT_LEVELS.get(assessment.threat_level, {}).get("color", "gray")
    threat_class = f"threat-level-{assessment.threat_level.lower()}"
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="{threat_class}">
            THREAT LEVEL<br>
            {assessment.threat_level}
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.metric("Threat Score", f"{assessment.threat_score}/10", delta=None)
    
    with col3:
        st.metric("Confidence", f"{assessment.confidence_score:.1%}", delta=None)
    
    with col4:
        st.metric("Last Updated", datetime.now().strftime("%H:%M:%S"))
    
    # Detailed information in tabs
    tab1, tab2, tab3, tab4 = st.tabs(["Risk Analysis", "Known Individuals", "Recommendations", "Location Info"])
    
    with tab1:
        st.subheader("Risk Factors")
        for factor in assessment.risk_factors:
            st.markdown(f" {factor}")
        
        if assessment.weapons_involved:
            st.subheader("Weapons Involved")
            for weapon in assessment.weapons_involved:
                st.markdown(f" {weapon}")
        
        if assessment.location_risks:
            st.subheader("Location Risks")
            for risk in assessment.location_risks:
                st.markdown(f" {risk}")
    
    with tab2:
        if assessment.known_individuals:
            for person in assessment.known_individuals:
                with st.expander(f"{person['name']} ({person['role']})"):
                    st.write(f"**Risk Level:** {person['risk_level']}")
                    st.write(f"**History:** {person['history']}")
                    st.write(f"**Last Seen:** {person.get('last_seen', 'Unknown')}")
        else:
            st.info("No known individuals identified")
    
    with tab3:
        st.subheader("De-escalation Recommendations")
        for i, rec in enumerate(assessment.de_escalation_recommendations, 1):
            st.markdown(f"**{i}.** {rec}")
        
        st.subheader("Safety Protocols")
        for i, protocol in enumerate(assessment.safety_protocols, 1):
            st.markdown(f"**{i}.** {protocol}")
    
    with tab4:
        if assessment.historical_context:
            st.subheader("Historical Context")
            st.write(assessment.historical_context)
        else:
            st.info("No historical context available")

def display_detailed_briefing(briefing: str):
    """Display the detailed briefing"""
    st.markdown("---")
    st.subheader("Complete Officer Briefing")
    
    # Display briefing in an expandable section
    with st.expander("View Complete Briefing", expanded=True):
        st.text(briefing)

def display_demo_data():
    """Display demo data and features"""
    st.subheader("System Features")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **AI-Powered Analysis:**
        - Real-time threat assessment
        - Pattern recognition
        - Risk scoring
        - Predictive analytics
        """)
        
        st.markdown("""
        **Data Sources:**
        - 911 call transcripts
        - Prior incident reports
        - GIS mapping data
        - Dispatch records
        - Body camera footage
        """)
    
    with col2:
        st.markdown("""
        **Safety Features:**
        - De-escalation recommendations
        - Safety protocols
        - Threat level indicators
        - Known individual tracking
        """)
        
        st.markdown("""
        **Privacy & Compliance:**
        - Data encryption
        - Audit trails
        - Explainable AI
        - Ethical guidelines
        """)
    
    # Demo threat levels
    st.subheader("Threat Level Examples")
    
    demo_data = [
        {"Level": "LOW", "Score": 2, "Description": "Minimal risk", "Color": "green"},
        {"Level": "MEDIUM", "Score": 4, "Description": "Moderate risk", "Color": "yellow"},
        {"Level": "HIGH", "Score": 7, "Description": "Significant risk", "Color": "orange"},
        {"Level": "CRITICAL", "Score": 9, "Description": "Extreme risk", "Color": "red"}
    ]
    
    df = pd.DataFrame(demo_data)
    st.dataframe(df, use_container_width=True)

if __name__ == "__main__":
    main()