"""
UI Components Module

Reusable Streamlit components for consistent, professional interface design.
Includes cards, charts, tables, and input components.
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from typing import List, Dict, Optional, Tuple


# ============================================================================
# CARD COMPONENTS
# ============================================================================

def metric_card(label: str, value: str, delta: Optional[str] = None) -> None:
    """
    Display a metric in a styled card.
    
    Args:
        label: Metric label
        value: Metric value
        delta: Optional change indicator
    """
    st.metric(label=label, value=value, delta=delta)


def stat_cards(statistics: Dict) -> None:
    """
    Display dashboard statistics as cards.
    
    Args:
        statistics: Dictionary with stat values
    """
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "🌐 Total Scanned",
            statistics.get("total_scanned", 0)
        )
    
    with col2:
        st.metric(
            "🟢 Online",
            statistics.get("online_count", 0)
        )
    
    with col3:
        st.metric(
            "🔴 Offline",
            statistics.get("offline_count", 0)
        )
    
    with col4:
        st.metric(
            "⏱️ Avg Response",
            statistics.get("avg_response_time", "N/A")
        )


def health_status_card(health: str) -> None:
    """
    Display network health status card.
    
    Args:
        health: Health status string
    """
    # Color mapping for health status
    health_colors = {
        "Excellent": "#00C853",
        "Good": "#7CB342",
        "Average": "#FDD835",
        "Poor": "#E53935"
    }
    
    health_emojis = {
        "Excellent": "🟢",
        "Good": "🟢",
        "Average": "🟡",
        "Poor": "🔴"
    }
    
    color = health_colors.get(health, "#9E9E9E")
    emoji = health_emojis.get(health, "⚪")
    
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, {color}20 0%, {color}10 100%);
        border-left: 4px solid {color};
        padding: 20px;
        border-radius: 8px;
        margin: 10px 0;
    ">
        <h3 style="margin: 0; color: {color};">
            {emoji} Network Health
        </h3>
        <p style="margin: 10px 0 0 0; font-size: 24px; font-weight: bold; color: {color};">
            {health}
        </p>
    </div>
    """, unsafe_allow_html=True)


# ============================================================================
# TABLE COMPONENTS
# ============================================================================

def results_table(
    results_df: pd.DataFrame,
    searchable: bool = True,
    sortable: bool = True
) -> pd.DataFrame:
    """
    Display scan results in a professional table.
    
    Args:
        results_df: DataFrame with scan results
        searchable: Enable search functionality
        sortable: Enable sorting
        
    Returns:
        Filtered/sorted DataFrame if search applied, original otherwise
    """
    # Create columns for controls
    col1, col2, col3 = st.columns([1, 1, 2])
    
    with col1:
        status_filter = st.selectbox(
            "Filter by Status",
            options=["All", "Online", "Offline"],
            key="status_filter"
        )
    
    with col2:
        search_term = st.text_input(
            "Search",
            placeholder="IP or Hostname",
            key="search_term"
        )
    
    # Apply filters
    filtered_df = results_df.copy()
    
    if status_filter != "All":
        filtered_df = filtered_df[filtered_df["Status"] == status_filter]
    
    if search_term:
        mask = (
            filtered_df["IP"].str.contains(search_term, case=False, na=False) |
            filtered_df["Hostname"].str.contains(search_term, case=False, na=False)
        )
        filtered_df = filtered_df[mask]
    
    # Display table
    st.dataframe(
        filtered_df,
        use_container_width=True,
        height=400,
        column_config={
            "IP": st.column_config.TextColumn(width="medium"),
            "Status": st.column_config.TextColumn(width="small"),
            "Hostname": st.column_config.TextColumn(width="medium"),
            "Response Time": st.column_config.TextColumn(width="small")
        }
    )
    
    # Show result count
    st.caption(f"Showing {len(filtered_df)} of {len(results_df)} devices")
    
    return filtered_df


# ============================================================================
# CHART COMPONENTS
# ============================================================================

def online_offline_chart(online_count: int, offline_count: int) -> None:
    """
    Display online/offline device distribution pie chart.
    
    Args:
        online_count: Number of online devices
        offline_count: Number of offline devices
    """
    fig = go.Figure(data=[go.Pie(
        labels=["Online", "Offline"],
        values=[online_count, offline_count],
        hole=0.4,
        marker=dict(colors=["#00C853", "#E53935"]),
        textposition="inside",
        textinfo="label+percent"
    )])
    
    fig.update_layout(
        title="Device Status Distribution",
        showlegend=True,
        height=400,
        margin=dict(t=50, b=50, l=50, r=50)
    )
    
    st.plotly_chart(fig, use_container_width=True)


def response_time_chart(results: List[Dict]) -> None:
    """
    Display response time distribution bar chart.
    
    Args:
        results: List of scan results
    """
    # Extract response times from online devices
    online_devices = [r for r in results if r["Status"] == "Online"]
    
    if not online_devices:
        st.info("No online devices to display")
        return
    
    # Prepare data (limit to top 20 fastest devices)
    ips = []
    times = []
    
    for device in online_devices[:20]:
        rt = device.get("Response Time", "N/A")
        if rt and rt != "N/A" and "ms" in str(rt):
            try:
                time_val = float(str(rt).replace("ms", ""))
                ips.append(device["IP"])
                times.append(time_val)
            except ValueError:
                pass
    
    if not times:
        st.info("No response time data available")
        return
    
    # Create chart
    fig = go.Figure(data=[
        go.Bar(
            x=ips,
            y=times,
            marker=dict(color=times, colorscale="Viridis"),
            hovertemplate="<b>%{x}</b><br>Response: %{y:.1f}ms<extra></extra>"
        )
    ])
    
    fig.update_layout(
        title="Response Time by Device (Top 20)",
        xaxis_title="IP Address",
        yaxis_title="Response Time (ms)",
        height=400,
        showlegend=False,
        margin=dict(t=50, b=100, l=50, r=50),
        xaxis=dict(tickangle=-45)
    )
    
    st.plotly_chart(fig, use_container_width=True)


# ============================================================================
# INPUT COMPONENTS
# ============================================================================

def network_input() -> Tuple[str, bool]:
    """
    Get network range input from user.
    
    Returns:
        Tuple of (network_range, scan_button_pressed)
    """
    col1, col2 = st.columns([3, 1])
    
    with col1:
        network_range = st.text_input(
            "Network Range",
            placeholder="e.g., 192.168.1.0/24",
            help="Enter CIDR notation (IP/prefix)",
            key="network_input"
        )
    
    with col2:
        scan_button = st.button(
            "🔍 Scan",
            use_container_width=True,
            type="primary"
        )
    
    return network_range, scan_button


def auto_detect_network() -> Optional[str]:
    """
    Auto-detect local network range.
    
    Returns:
        Detected network range or None
    """
    try:
        import socket
        
        # Get local IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        
        # Construct network range (/24)
        parts = local_ip.split(".")
        network = f"{parts[0]}.{parts[1]}.{parts[2]}.0/24"
        
        return network
    except Exception:
        return None


def settings_panel() -> Dict:
    """
    Display settings configuration panel.
    
    Returns:
        Dictionary with updated settings
    """
    st.subheader("⚙️ Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        timeout = st.slider(
            "Ping Timeout (seconds)",
            min_value=1,
            max_value=5,
            value=2,
            help="How long to wait for each ping"
        )
        
        max_threads = st.slider(
            "Max Concurrent Threads",
            min_value=5,
            max_value=50,
            value=20,
            help="Number of parallel scans"
        )
    
    with col2:
        groq_key = st.text_input(
            "Groq API Key",
            type="password",
            help="Get from https://console.groq.com",
            key="groq_key_input"
        )
        
        theme = st.selectbox(
            "Theme",
            options=["Light", "Dark"],
            help="Display theme preference"
        )
    
    return {
        "timeout": timeout,
        "max_threads": max_threads,
        "groq_api_key": groq_key,
        "theme": theme
    }


# ============================================================================
# INFORMATION PANELS
# ============================================================================

def ai_analysis_panel(analysis: Optional[Dict]) -> None:
    """
    Display AI analysis results in organized panels.
    
    Args:
        analysis: Dictionary with AI analysis results
    """
    if analysis is None:
        st.warning("AI analysis unavailable - API key not configured")
        return
    
    # Summary section
    with st.expander("📊 Network Summary", expanded=True):
        summary = analysis.get("summary", "No summary available")
        st.write(summary)
    
    # Recommendations section
    with st.expander("💡 Recommendations", expanded=True):
        recommendations = analysis.get("recommendations", "No recommendations available")
        st.write(recommendations)
    
    # Health status
    with st.expander("❤️ Network Health", expanded=False):
        health = analysis.get("health", "Unknown")
        health_status_card(health)


def about_panel() -> None:
    """Display project information panel."""
    st.subheader("ℹ️ About This Project")
    
    st.markdown("""
    ### AI-Powered Network Scanner
    
    A fast, intelligent network scanning tool for discovering and analyzing 
    devices on your network.
    
    **Features:**
    - 🔍 Fast concurrent network scanning
    - 🤖 AI-powered analysis (Groq)
    - 📊 Real-time statistics and charts
    - 💾 Export to CSV/JSON
    - 🎨 Modern, responsive UI
    
    **Technology Stack:**
    - Python & Streamlit
    - ThreadPoolExecutor (concurrent scanning)
    - Groq API (AI analysis)
    - Plotly (data visualization)
    
    **Learning Outcomes:**
    - Network fundamentals & CIDR notation
    - Concurrent programming in Python
    - API integration patterns
    - UI/UX with Streamlit
    - Clean code practices
    
    **Portfolio Ready:** This project demonstrates professional Python development,
    networking knowledge, and modern web UI skills.
    """)


# ============================================================================
# PROGRESS & STATUS COMPONENTS
# ============================================================================

def progress_tracker(total: int):
    """
    Context manager for scan progress tracking.
    
    Usage:
        with progress_tracker(total_ips) as progress:
            for ip in ips:
                progress.update()
    
    Args:
        total: Total items to process
    """
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    class ProgressTracker:
        def __init__(self):
            self.current = 0
        
        def update(self, message: str = "Scanning..."):
            self.current += 1
            progress = self.current / total
            progress_bar.progress(progress)
            status_text.text(f"{message} ({self.current}/{total})")
        
        def finish(self):
            progress_bar.progress(1.0)
            status_text.text("✅ Complete!")
    
    tracker = ProgressTracker()
    try:
        yield tracker
    finally:
        pass


# ============================================================================
# SIDEBAR COMPONENTS
# ============================================================================

def render_sidebar_nav() -> str:
    """
    Render sidebar navigation.
    
    Returns:
        Selected page name
    """
    with st.sidebar:
        st.title("📡 Network Scanner")
        st.divider()
        
        page = st.radio(
            "Navigation",
            options=["Dashboard", "Settings", "About"],
            label_visibility="collapsed"
        )
        
        return page


def render_sidebar_info() -> None:
    """Render sidebar information panel."""
    with st.sidebar:
        st.divider()
        st.subheader("💡 Quick Tips")
        
        st.markdown("""
        **Common Network Ranges:**
        - Home: `192.168.1.0/24`
        - Office: `10.0.0.0/24`
        - Small: `172.16.0.0/25`
        
        **Tips:**
        - Run with admin/sudo for best results
        - Smaller subnets scan faster
        - Keep API key private
        
        **Documentation:**
        - Check README.md for help
        """)
