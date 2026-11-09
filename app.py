"""
AI-Powered Network Scanner - Main Application
"""

import streamlit as st
import pandas as pd
import logging
import os
from datetime import datetime
import time
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from scanner import NetworkScanner
from ai import GroqAnalyzer
from utils import (
    validate_network_range,
    format_duration,
    calculate_statistics,
    export_to_csv,
    export_to_json,
    get_default_settings
)
from ui import (
    auto_detect_network,
    stat_cards,
    results_table,
    online_offline_chart,
    response_time_chart,
    ai_analysis_panel,
    about_panel,
    render_sidebar_nav,
    render_sidebar_info
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

def configure_page():
    """Configure Streamlit page and session state."""
    st.set_page_config(
        page_title="Network Scanner",
        page_icon="📡",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Initialize session state
    if "scan_results" not in st.session_state:
        st.session_state.scan_results = None
    if "scan_statistics" not in st.session_state:
        st.session_state.scan_statistics = None
    if "ai_analysis" not in st.session_state:
        st.session_state.ai_analysis = None
    if "scan_timestamp" not in st.session_state:
        st.session_state.scan_timestamp = None
    if "settings" not in st.session_state:
        st.session_state.settings = get_default_settings()
    if "network_input_val" not in st.session_state:
        st.session_state.network_input_val = ""


# ============================================================================
# DASHBOARD PAGE
# ============================================================================

def dashboard_page():
    """Main dashboard with scanning interface."""
    
    st.title("🌐 Network Scanner Dashboard")
    st.write("Fast, intelligent network device discovery and analysis")
    st.divider()
    
    st.subheader("🔍 Scan Network")
    
    # Aligned bottom to match text_input height perfectly
    col1, col2 = st.columns([3, 1], vertical_alignment="bottom")
    
    with col1:
        network_range = st.text_input(
            "Network Range",
            value=st.session_state.network_input_val,
            placeholder="e.g., 192.168.1.0/24",
            help="Enter CIDR notation",
            key="network_range_input"
        )
        # Update session state with manual typed value
        st.session_state.network_input_val = network_range
    
    with col2:
        if st.button("🔎 Auto-Detect", use_container_width=True, type="secondary"):
            detected = auto_detect_network()
            if detected:
                st.session_state.network_input_val = detected
                st.rerun()
            else:
                st.error("❌ Could not auto-detect network")
    
    st.write("")  # Spacer
    
    # Action buttons
    col1, col2, col3 = st.columns([1, 1, 2])
    
    with col1:
        scan_button = st.button(
            "🚀 Start Scan",
            use_container_width=True,
            type="primary"
        )
    
    with col2:
        clear_button = st.button(
            "🗑️ Clear Results",
            use_container_width=True,
            type="secondary"
        )
    
    # Handle action buttons
    if clear_button:
        st.session_state.scan_results = None
        st.session_state.ai_analysis = None
        st.session_state.scan_statistics = None
        st.session_state.network_input_val = ""
        st.rerun()
    
    if scan_button:
        handle_scan(st.session_state.network_input_val)
    
    # Display results if available
    if st.session_state.scan_results is not None:
        st.divider()
        display_results()


def handle_scan(network_range: str):
    """Execute network scan."""
    if not network_range:
        st.error("❌ Please enter a network range")
        return
    
    if not validate_network_range(network_range):
        st.error("❌ Invalid network range. Use CIDR notation (e.g., 192.168.1.0/24)")
        return
    
    try:
        progress_placeholder = st.empty()
        status_placeholder = st.empty()
        
        settings = st.session_state.settings
        scanner = NetworkScanner(
            timeout=settings["timeout"],
            max_threads=settings["max_threads"]
        )
        
        with progress_placeholder.container():
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            def progress_callback(progress: float):
                status_text.text(f"🔍 Scanning: {int(progress * 100)}%")
                progress_bar.progress(progress)
            
            status_placeholder.info("⏳ Scanning network... This may take a minute.")
            
            start_time = time.time()
            results = scanner.scan_network(
                network_range,
                progress_callback=progress_callback
            )
            end_time = time.time()
        
        results_df = pd.DataFrame(results)
        statistics = calculate_statistics(results)
        statistics["duration"] = format_duration(end_time - start_time)
        statistics["total_scanned"] = len(results)
        
        st.session_state.scan_results = results_df
        st.session_state.scan_statistics = statistics
        st.session_state.scan_timestamp = datetime.now()
        
        status_placeholder.info("🤖 Generating AI analysis...")
        
        api_key = os.getenv("GROQ_API_KEY") or st.session_state.settings.get("groq_api_key")
        analyzer = GroqAnalyzer(api_key)
        
        if analyzer.is_available():
            ai_analysis = analyzer.analyze_scan_results(results, statistics)
            st.session_state.ai_analysis = ai_analysis
        
        progress_placeholder.empty()
        status_placeholder.success("✅ Scan completed successfully!")
        
        logger.info(f"Scan completed: {statistics['total_scanned']} IPs, {statistics['online_count']} online")
        
        time.sleep(0.5)
        st.rerun()
    
    except Exception as e:
        st.error(f"❌ Scan failed: {str(e)}")
        logger.error(f"Scan error: {e}")


def display_results():
    """Display scan results and analysis."""
    results_df = st.session_state.scan_results
    statistics = st.session_state.scan_statistics
    
    st.subheader("📊 Statistics")
    stat_cards(statistics)
    
    st.divider()
    st.subheader("📈 Visualizations")
    
    col1, col2 = st.columns(2)
    with col1:
        online_offline_chart(
            statistics["online_count"],
            statistics["offline_count"]
        )
    
    with col2:
        response_time_chart(st.session_state.scan_results.to_dict('records'))
    
    st.divider()
    st.subheader("🖥️ Scan Results")
    results_table(results_df)
    
    st.divider()
    if st.session_state.ai_analysis is not None:
        st.subheader("🤖 AI Analysis")
        ai_analysis_panel(st.session_state.ai_analysis)
    
    st.divider()
    st.subheader("💾 Export Results")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        csv_data = export_to_csv(results_df)
        st.download_button(
            label="📥 Download CSV",
            data=csv_data,
            file_name=f"scan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            use_container_width=True
        )
    
    with col2:
        json_data = export_to_json(results_df)
        st.download_button(
            label="📥 Download JSON",
            data=json_data,
            file_name=f"scan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json",
            use_container_width=True
        )
    
    with col3:
        st.info("📝 Export formats: CSV and JSON")


# ============================================================================
# SETTINGS & ABOUT PAGES
# ============================================================================

def settings_page():
    st.title("⚙️ Settings")
    st.write("Configure scanner behavior and API keys")
    st.divider()
    
    settings = st.session_state.settings
    st.subheader("🔧 Scanner Settings")
    
    col1, col2 = st.columns(2)
    with col1:
        timeout = st.slider(
            "Ping Timeout (seconds)",
            min_value=1, max_value=5,
            value=settings.get("timeout", 2),
            key="timeout_slider"
        )
    
    with col2:
        max_threads = st.slider(
            "Max Concurrent Threads",
            min_value=5, max_value=50,
            value=settings.get("max_threads", 20),
            key="threads_slider"
        )
    
    st.divider()
    st.subheader("🤖 AI Analysis Settings")
    
    env_api_key = os.getenv("GROQ_API_KEY")
    if env_api_key:
        st.success("✅ API key loaded from environment (.env file)")
    
    groq_key = st.text_input(
        "Groq API Key",
        value=settings.get("groq_api_key", ""),
        type="password",
        key="groq_key"
    )
    
    if groq_key:
        if st.button("🧪 Test API Key", use_container_width=True):
            try:
                analyzer = GroqAnalyzer(groq_key)
                if analyzer.is_available():
                    st.success("✅ API key is valid!")
                else:
                    st.error("❌ API key is invalid")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
    
    st.divider()
    st.subheader("🎨 Display Settings")
    
    theme = st.selectbox(
        "Theme",
        options=["Light", "Dark"],
        index=0 if settings.get("theme", "light") == "Light" else 1,
        key="theme_select"
    )
    
    st.divider()
    if st.button("💾 Save Settings", use_container_width=True, type="primary"):
        st.session_state.settings = {
            "timeout": timeout,
            "max_threads": max_threads,
            "groq_api_key": groq_key,
            "theme": theme
        }
        st.success("✅ Settings saved!")


def about_page():
    st.title("ℹ️ About")
    st.divider()
    about_panel()


# ============================================================================
# MAIN APPLICATION
# ============================================================================

def main():
    configure_page()
    page = render_sidebar_nav()
    render_sidebar_info()
    
    if page == "Dashboard":
        dashboard_page()
    elif page == "Settings":
        settings_page()
    elif page == "About":
        about_page()


if __name__ == "__main__":
    main()