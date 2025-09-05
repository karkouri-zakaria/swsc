import streamlit as st
import requests
import json
import os
import time
from datetime import datetime
from pathlib import Path
from typing import List, Tuple, Dict
import concurrent.futures
from dataclasses import dataclass

# Configuration
DATA_FILE = Path("websites.json")
DEFAULT_WEBSITES = [
    "https://agimobadrimmobilier.com",
    "https://agimobadrimmobilier.ma",
    "https://ceg.ma",
    "https://elysiumdinnershow.ma",
    "https://hrk.ma",
    "https://kapture.ma",
    "https://la-villa.ma",
    "https://manaosavis.ma",
    "https://startjobs.ma",
    "https://topanimation.ma"
]

@dataclass
class WebsiteStatus:
    url: str
    status: str
    color: str
    response_time: float
    status_code: int = None

class WebsiteManager:
    """Modern class-based approach for managing websites"""
    
    def __init__(self):
        self.websites = self.load_websites()
    
    def load_websites(self) -> List[str]:
        """Load websites from JSON file or return defaults"""
        if DATA_FILE.exists():
            try:
                with open(DATA_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                return DEFAULT_WEBSITES.copy()
        return DEFAULT_WEBSITES.copy()
    
    def save_websites(self, websites: List[str]) -> bool:
        """Save websites to JSON file"""
        try:
            with open(DATA_FILE, "w", encoding="utf-8") as f:
                json.dump(websites, f, indent=2, ensure_ascii=False)
            self.websites = websites
            return True
        except Exception as e:
            st.error(f"Error saving websites: {e}")
            return False
    
    def check_website(self, url: str, timeout: int = 10) -> WebsiteStatus:
        """Check a single website status with improved error handling"""
        start_time = time.time()
        
        try:
            # Ensure URL has a scheme
            if not url.startswith(('http://', 'https://')):
                url = f"https://{url}"
            
            response = requests.get(
                url, 
                timeout=timeout,
                headers={'User-Agent': 'Website Status Checker 1.0'},
                allow_redirects=True,  # Follow redirects
                verify=False
            )
            response_time = round((time.time() - start_time) * 1000, 2)
            
            # More comprehensive status checking
            if 200 <= response.status_code < 300:
                return WebsiteStatus(
                    url=url,
                    status="🟢 Online",
                    color="#28a745",
                    response_time=response_time,
                    status_code=response.status_code
                )
            elif 300 <= response.status_code < 400:
                return WebsiteStatus(
                    url=url,
                    status=f"🟡 Redirect ({response.status_code})",
                    color="#ffc107",
                    response_time=response_time,
                    status_code=response.status_code
                )
            elif 400 <= response.status_code < 500:
                return WebsiteStatus(
                    url=url,
                    status=f"🔴 Client Error ({response.status_code})",
                    color="#dc3545",
                    response_time=response_time,
                    status_code=response.status_code
                )
            elif 500 <= response.status_code < 600:
                return WebsiteStatus(
                    url=url,
                    status=f"🔴 Server Error ({response.status_code})",
                    color="#dc3545",
                    response_time=response_time,
                    status_code=response.status_code
                )
            else:
                return WebsiteStatus(
                    url=url,
                    status=f"🟡 Unknown ({response.status_code})",
                    color="#ffc107",
                    response_time=response_time,
                    status_code=response.status_code
                )
                
        except requests.exceptions.SSLError:
            return WebsiteStatus(
                url=url,
                status="🔴 SSL Error",
                color="#dc3545",
                response_time=(time.time() - start_time) * 1000
            )
        except requests.exceptions.Timeout:
            return WebsiteStatus(
                url=url,
                status="🔴 Timeout",
                color="#dc3545",
                response_time=timeout * 1000
            )
        except requests.exceptions.ConnectionError:
            return WebsiteStatus(
                url=url,
                status="🔴 Connection Failed",
                color="#dc3545",
                response_time=(time.time() - start_time) * 1000
            )
        except Exception as e:
            return WebsiteStatus(
                url=url,
                status=f"🔴 Error: {str(e)[:50]}",
                color="#dc3545",
                response_time=(time.time() - start_time) * 1000
            )
    
    def check_all_websites(self, websites: List[str], max_workers: int = 5) -> Dict[str, WebsiteStatus]:
        """Check all websites concurrently for better performance"""
        results = {}
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_url = {
                executor.submit(self.check_website, url): url 
                for url in websites
            }
            
            for future in concurrent.futures.as_completed(future_to_url):
                url = future_to_url[future]
                try:
                    result = future.result()
                    results[url] = result
                except Exception as e:
                    results[url] = WebsiteStatus(
                        url=url,
                        status=f"🔴 Error: {str(e)}",
                        color="#dc3545",
                        response_time=0
                    )
        
        return results

# Initialize the website manager
website_manager = WebsiteManager()

# Modern Streamlit configuration
st.set_page_config(
    page_title="SWSC",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Modern CSS styling
st.markdown("""
<style>
    /* Main container styling */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: .5rem;
        border-radius: 20px;
        margin-bottom: 1rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    
    .main-title {
        color: white;
        text-align: center;
        font-size: .5rem;
        font-weight: 700;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .subtitle {
        color: rgba(255,255,255,0.9);
        text-align: center;
        font-size: 1.2rem;
        margin-top: 0.5rem;
    }
    
    /* Card styling */
    .status-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
        border-left: 4px solid #667eea;
        transition: all 0.3s ease;
    }
    
    .status-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }
    
    /* Status styling */
    .status-item {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: .5rem;
        background: #f8f9fa;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 4px solid;
        transition: all 0.3s ease;
    }
    
    .status-item:hover {
        background: #e9ecef;
    }
    
    .url-text {
        font-weight: 600;
        color: #343a40;
        flex: 1;
        word-break: break-all;
    }
    
    .url-text a {
        color: #007bff;
        text-decoration: none;
        font-weight: 600;
        transition: all 0.3s ease;
        border-radius: 4px;
        padding: 2px 4px;
    }
    
    .url-text a:hover {
        color: #0056b3;
        background-color: rgba(0, 123, 255, 0.1);
        text-decoration: underline;
        transform: translateX(2px);
    }
    
    .url-text a:visited {
        color: #6f42c1;
    }
    
    .status-badge {
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.9rem;
    }
    
    .response-time {
        font-size: 0.8rem;
        color: #6c757d;
        margin-left: 0.5rem;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
    }
    
    .form-label {
        color: #495057;
        font-weight: 600;
        font-size: 0.95rem;
        margin-bottom: 0.5rem;
        display: block;
    }
    
    .stTextArea > div > div > textarea {
        border-radius: 12px;
        border: 2px solid #e9ecef;
        padding: 1rem;
        font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
        font-size: 0.9rem;
        transition: all 0.3s ease;
    }
    
    .stTextArea > div > div > textarea:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    /* Action buttons styling */
    .action-buttons {
        display: flex;
        gap: 1rem;
        margin-top: 1.5rem;
    }
    
    .save-button {
        background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
        box-shadow: 0 4px 15px rgba(40, 167, 69, 0.4);
    }
    
    .save-button:hover {
        box-shadow: 0 6px 20px rgba(40, 167, 69, 0.6);
        transform: translateY(-2px);
    }
    
    .reset-button {
        background: linear-gradient(135deg, #ffc107 0%, #fd7e14 100%);
        box-shadow: 0 4px 15px rgba(255, 193, 7, 0.4);
        color: #212529 !important;
    }
    
    .reset-button:hover {
        box-shadow: 0 6px 20px rgba(255, 193, 7, 0.6);
        transform: translateY(-2px);
    }
    
    /* Website count indicator */
    .website-counter {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        margin-top: 1rem;
        text-align: center;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    /* Validation indicators */
    .url-validation {
        display: flex;
        align-items: center;
        margin-top: 0.5rem;
        font-size: 0.85rem;
    }
    
    .valid-url {
        color: #28a745;
    }
    
    .invalid-url {
        color: #dc3545;
    }
    
    /* Help text styling */
    .help-text {
        background: #e7f3ff;
        border-left: 4px solid #0066cc;
        padding: 1rem;
        border-radius: 8px;
        margin-top: 1rem;
        font-size: 0.9rem;
        color: #004085;
    }
    
    .help-text h4 {
        margin: 0 0 0.5rem 0;
        color: #0066cc;
        font-size: 1rem;
    }
    
    .help-text ul {
        margin: 0.5rem 0 0 1rem;
        padding: 0;
    }
    
    .help-text li {
        margin-bottom: 0.25rem;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    /* Enhanced form button styling */
    .stForm button[type="submit"] {
        border-radius: 12px;
        font-weight: 600;
        transition: all 0.3s ease;
        border: none;
        padding: 0.75rem 1.5rem;
    }
    
    /* Save button specific styling */
    .stForm button[type="submit"]:first-of-type {
        background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
        color: white;
        box-shadow: 0 4px 15px rgba(40, 167, 69, 0.4);
    }
    
    .stForm button[type="submit"]:first-of-type:hover {
        box-shadow: 0 6px 20px rgba(40, 167, 69, 0.6);
        transform: translateY(-2px);
    }
    
    /* Reset button specific styling */
    .stForm button[type="submit"]:last-of-type {
        background: linear-gradient(135deg, #ffc107 0%, #fd7e14 100%);
        color: #212529;
        box-shadow: 0 4px 15px rgba(255, 193, 7, 0.4);
    }
    
    .stForm button[type="submit"]:last-of-type:hover {
        box-shadow: 0 6px 20px rgba(255, 193, 7, 0.6);
        transform: translateY(-2px);
    }
    
    /* Success and error message styling */
    .stAlert {
        border-radius: 12px;
        border: none;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
    
    /* Success message */
    .stAlert[data-baseweb="notification"] [data-testid="stNotification"] {
        background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
        border-left: 4px solid #28a745;
    }
    
    /* Error message */
    .stAlert[data-baseweb="notification"] [data-testid="stNotification"][data-testid*="error"] {
        background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%);
        border-left: 4px solid #dc3545;
    }
    
    /* Progress bar */
    .progress-container {
        background: #e9ecef;
        border-radius: 10px;
        overflow: hidden;
        margin: 1rem 0;
    }
    
    .progress-bar {
        height: 8px;
        background: linear-gradient(90deg, #667eea, #764ba2);
        transition: width 0.3s ease;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h4 class="main-title">Startjobs Websites Status Checker</h4>
    <p class="subtitle">Real-time monitoring dashboard for Startjobs websites</p>
</div>
""", unsafe_allow_html=True)

# Sidebar for configuration
with st.sidebar:
    st.markdown("### ⚙️ Configuration")
    
    timeout_setting = st.slider(
        "Request Timeout (seconds)",
        min_value=5,
        max_value=30,
        value=10,
        help="Maximum time to wait for each website response"
    )
    
    max_workers = st.slider(
        "Concurrent Checks",
        min_value=1,
        max_value=10,
        value=5,
        help="Number of websites to check simultaneously"
    )
    
    auto_refresh = st.checkbox(
        "Auto Refresh",
        help="Automatically refresh status every 30 seconds"
    )
    
    if auto_refresh:
        refresh_interval = st.number_input(
            "Refresh Interval (seconds)",
            min_value=10,
            max_value=300,
            value=30
        )

# Main content area
col1, col2 = st.columns([1, 2])

with col1:
    # Website Management Panel with modern styling
    st.markdown("""
    <div class="website-management">
        <div class="management-header">
            <h5 class="management-title">📝 Manage Websites</h5>
        </div>
    """, unsafe_allow_html=True)
    
    # Website management form with enhanced styling
    with st.form("website_form"):
        st.markdown('<div class="website-form-container">', unsafe_allow_html=True)
        
        # Form label
        st.markdown('<label class="form-label">🌐 Website URLs (one per line):</label>', unsafe_allow_html=True)
        
        websites_text = st.text_area(
            "",
            value="\n".join(website_manager.websites),
            height=250,
            label_visibility="collapsed",
            placeholder="https://example.com\nhttps://another-site.com\n..."
        )
        
        # URL validation and count
        current_urls = [line.strip() for line in websites_text.split("\n") if line.strip()]
        
        # URL validation feedback with preview
        if current_urls:
            valid_urls = []
            invalid_urls = []
            
            for url in current_urls:
                if url.startswith(('http://', 'https://')) and '.' in url:
                    valid_urls.append(url)
                else:
                    invalid_urls.append(url)
            
            if valid_urls or invalid_urls:
                st.markdown('<div class="url-validation">', unsafe_allow_html=True)
                if valid_urls:
                    st.markdown(f'<span class="valid-url">✅ {len(valid_urls)} valid URL(s)</span>', unsafe_allow_html=True)
                if invalid_urls:
                    st.markdown(f'<span class="invalid-url">⚠️ {len(invalid_urls)} URL(s) may need http:// or https://</span>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            # Website preview section
            if len(current_urls) != len(website_manager.websites) or set(current_urls) != set(website_manager.websites):
                st.markdown("""
                <div style="background: #fff3cd; border-left: 4px solid #ffc107; padding: 1rem; border-radius: 8px; margin: 1rem 0;">
                    <strong>📝 Unsaved Changes Detected</strong><br>
                    <small>Click "Save Changes" to apply your modifications</small>
                </div>
                """, unsafe_allow_html=True)
        
        # Quick preview of websites
        if current_urls:
            with st.popover("👀 Preview Website List"):
                for i, url in enumerate(current_urls[:10], 1):  # Show first 10
                    status_icon = "✅" if url.startswith(('http://', 'https://')) else "⚠️"
                    st.markdown(f"{i}. {status_icon} `{url}`")
                
                if len(current_urls) > 10:
                    st.markdown(f"... and {len(current_urls) - 10} more websites")
        
        # Action buttons with enhanced styling
        col_save, col_reset = st.columns(2)
        
        with col_save:
            save_button = st.form_submit_button(
                "💾 Save Changes", 
                use_container_width=True,
                help="Save the current list of websites"
            )
        
        with col_reset:
            reset_button = st.form_submit_button(
                "🔄 Reset to Default", 
                use_container_width=True,
                help="Reset to the original default website list"
            )
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)  # Close website-management div
    
    # Form submission handling with enhanced feedback
    if save_button:
        new_websites = [
            line.strip() for line in websites_text.split("\n") 
            if line.strip()
        ]
        
        if not new_websites:
            st.error("❌ Cannot save empty website list. Please add at least one URL.")
        else:
            if website_manager.save_websites(new_websites):
                st.success(f"✅ Successfully saved {len(new_websites)} website(s)!")
                st.balloons()  # Fun visual feedback
                st.rerun()
            else:
                st.error("❌ Failed to save websites. Please try again.")
    
    if reset_button:
        if website_manager.save_websites(DEFAULT_WEBSITES):
            st.success(f"🔄 Successfully reset to {len(DEFAULT_WEBSITES)} default websites!")
            st.balloons()  # Fun visual feedback
            st.rerun()
        else:
            st.error("❌ Failed to reset websites. Please try again.")

with col2:
    st.markdown("##### 🔍 Status Dashboard")
    
    # Control buttons
    col_check, col_export = st.columns(2)
    
    with col_check:
        check_button = st.button("🚀 Start Check ", use_container_width=True)
    
    with col_export:
        export_button = st.button("📊 Export Report", use_container_width=True)
    
    # Status checking
    if check_button or auto_refresh:
        if not website_manager.websites:
            st.warning("⚠️ No websites configured. Please add some URLs first.")
        else:
            # Progress indicator
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Check websites
            with st.spinner("Checking website status..."):
                results = {}
                
                for i, url in enumerate(website_manager.websites):
                    status_text.text(f"Checking: {url}")
                    result = website_manager.check_website(url, timeout_setting)
                    results[url] = result
                    progress_bar.progress((i + 1) / len(website_manager.websites))
                    time.sleep(0.1)  # Small delay for visual effect
                
                status_text.empty()
                progress_bar.empty()
            
            # Display results
            st.markdown("##### 📊 Results")
            
            # Summary statistics
            total_sites = len(results)
            online_sites = sum(1 for r in results.values() if "🟢" in r.status)
            warning_sites = sum(1 for r in results.values() if "🟡" in r.status)
            offline_sites = sum(1 for r in results.values() if "🔴" in r.status)
            
            col_stats1, col_stats2, col_stats3, col_stats4 = st.columns(4)
            
            with col_stats1:
                st.metric("Total Sites", total_sites)
            
            with col_stats2:
                st.metric("Online", online_sites, delta=online_sites-offline_sites)
            
            with col_stats3:
                st.metric("Warnings", warning_sites)
            
            with col_stats4:
                st.metric("Offline", offline_sites, delta=-offline_sites if offline_sites > 0 else 0)
            
            for url, result in results.items():
                # Create status display with clickable URL
                status_html = f"""
                <div class="status-item" style="border-left-color: {result.color}; flex-direction: column; align-items: flex-start;">
                    <div class="url-text" style="margin-bottom: 0.5rem;">
                        <a href="{result.url}" target="_blank" style="color: #007bff; text-decoration: none; font-weight: 600;">
                            {result.url}
                        </a>
                    </div>
                    <div style="display: flex; align-items: center; width: 100%;">
                        <span class="status-badge" style="background-color: {result.color}; color: white;">
                            {result.status}
                        </span>
                        <span class="response-time">{int(result.response_time)}ms</span>
                    </div>
                </div>
                """
                st.markdown(status_html, unsafe_allow_html=True)
            
            # Store results in session state for export
            st.session_state['last_results'] = results
            st.session_state['last_check_time'] = datetime.now()
    
    # Export functionality
    if export_button and 'last_results' in st.session_state:
        report_data = {
            "timestamp": st.session_state['last_check_time'].isoformat(),
            "summary": {
                "total_sites": len(st.session_state['last_results']),
                "online": sum(1 for r in st.session_state['last_results'].values() if "🟢" in r.status),
                "warnings": sum(1 for r in st.session_state['last_results'].values() if "🟡" in r.status),
                "offline": sum(1 for r in st.session_state['last_results'].values() if "🔴" in r.status)
            },
            "details": {
                url: {
                    "status": result.status,
                    "response_time": result.response_time,
                    "status_code": result.status_code
                }
                for url, result in st.session_state['last_results'].items()
            }
        }
        
        st.download_button(
            label="📥 Download JSON Report",
            data=json.dumps(report_data, indent=2),
            file_name=f"website_status_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )

# Auto-refresh functionality
if auto_refresh:
    time.sleep(refresh_interval)
    st.rerun()

# Footer
st.markdown("""
---
<div style="text-align: center; color: #6c757d; padding: 1rem;">
    <p>🚀 Website Status Monitor | Built By Startjobs</p>
    <p>Last updated: {}</p>
</div>
""".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")), unsafe_allow_html=True)
