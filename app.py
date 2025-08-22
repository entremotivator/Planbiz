import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
import json
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import re

# -------------------------------
# Page Configuration
# -------------------------------
st.set_page_config(
    page_title="Business Plan Viewer",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for light blue theme
st.markdown("""
<style>
    .main {
        background-color: #f0f8ff;
    }
    .stApp {
        background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
    }
    .business-card {
        background: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin: 10px 0;
        border-left: 5px solid #2196f3;
    }
    .metric-card {
        background: linear-gradient(135deg, #2196f3 0%, #21cbf3 100%);
        color: white;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        margin: 5px;
    }
    .sidebar .sidebar-content {
        background-color: #e1f5fe;
    }
    .stSelectbox > div > div {
        background-color: white;
    }
    .stTextInput > div > div > input {
        background-color: white;
    }
    h1 {
        color: #1976d2;
        text-align: center;
        margin-bottom: 30px;
    }
    h2 {
        color: #1565c0;
    }
    h3 {
        color: #0d47a1;
    }
</style>
""", unsafe_allow_html=True)

# -------------------------------
# Helper Functions
# -------------------------------

@st.cache_resource(ttl=3600)
def get_gspread_client(service_account_info):
    """Create and cache Google Sheets client"""
    try:
        # Updated scopes to allow read/write access
        scopes = [
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive'
        ]
        creds = Credentials.from_service_account_info(service_account_info, scopes=scopes)
        gc = gspread.authorize(creds)
        return gc
    except Exception as e:
        st.error(f"Error authenticating with Google Sheets: {e}")
        return None

@st.cache_data(ttl=300)
def fetch_data(sheet_id, sheet_name, service_account_info):
    """Fetch data from Google Sheets with caching"""
    try:
        gc = get_gspread_client(service_account_info)
        if gc:
            sh = gc.open_by_key(sheet_id)
            worksheet = sh.worksheet(sheet_name)
            data = worksheet.get_all_records()
            return pd.DataFrame(data)
    except Exception as e:
        st.error(f"Error fetching data: {e}")
    return pd.DataFrame()

def extract_numeric_value(text):
    """Extract numeric value from text (for startup costs)"""
    if pd.isna(text) or text == "":
        return 0
    # Extract numbers from text
    numbers = re.findall(r'[\d,]+', str(text))
    if numbers:
        # Remove commas and convert to int
        return int(numbers[0].replace(',', ''))
    return 0

def create_business_card(row):
    """Create a styled business card for each business plan"""
    with st.container():
        st.markdown(f"""
        <div class="business-card">
            <h3 style="color: #1976d2; margin-bottom: 10px;">🏢 {row['Business Name']}</h3>
            <p style="color: #666; margin-bottom: 15px;"><strong>👤 Founder:</strong> {row['Name']} | <strong>📧 Email:</strong> {row['Email']}</p>
            
            <div style="margin-bottom: 15px;">
                <h4 style="color: #1565c0;">💡 Business Idea</h4>
                <p>{row['Business Idea']}</p>
            </div>
            
            <div style="display: flex; flex-wrap: wrap; gap: 10px; margin-bottom: 15px;">
                <div style="flex: 1; min-width: 200px;">
                    <h4 style="color: #1565c0;">💰 Startup Costs</h4>
                    <p>{row['Startup Costs']}</p>
                </div>
                <div style="flex: 1; min-width: 200px;">
                    <h4 style="color: #1565c0;">🎯 Target Audience</h4>
                    <p>{row['Target Audience']}</p>
                </div>
            </div>
            
            <div style="margin-bottom: 15px;">
                <h4 style="color: #1565c0;">🎯 Business Goals</h4>
                <ul>
                    <li><strong>3 months:</strong> {row['Business Goals (3 months)']}</li>
                    <li><strong>6 months:</strong> {row['Business Goals (6 months)']}</li>
                    <li><strong>12 months:</strong> {row['Business Goals (12 months)']}</li>
                </ul>
            </div>
            
            <div style="margin-bottom: 15px;">
                <h4 style="color: #1565c0;">📈 Marketing Plan</h4>
                <p>{row['Marketing Plan']}</p>
            </div>
            
            <div style="margin-bottom: 15px;">
                <h4 style="color: #1565c0;">🎯 Mission Statement</h4>
                <p>{row['Mission Statement']}</p>
            </div>
            
            <div style="margin-bottom: 15px;">
                <h4 style="color: #1565c0;">💵 Pricing and Revenue Plan</h4>
                <p>{row['Pricing and Revenue Plan']}</p>
            </div>
            
            <div style="margin-bottom: 15px;">
                <h4 style="color: #1565c0;">🛍️ Product/Service Description</h4>
                <p>{row['Product or Service Description']}</p>
            </div>
            
            <div style="margin-bottom: 15px;">
                <h4 style="color: #1565c0;">🏆 Competitive Advantage</h4>
                <p>{row['Competitors and Differentiation']}</p>
            </div>
            
            <div style="margin-bottom: 15px;">
                <h4 style="color: #1565c0;">📝 Additional Notes</h4>
                <p>{row['Additional Notes or Support']}</p>
            </div>
            
            <div>
                <h4 style="color: #1565c0;">📋 Plan Summary/Revision Preference</h4>
                <p>{row['Plan Summary or Revision Preference']}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

# -------------------------------
# Main Application
# -------------------------------

st.title("📊 Business Plan Viewer & Manager")
st.markdown("### Comprehensive Business Plan Analysis and Management System")

# Sidebar for configuration
st.sidebar.header("🔧 Configuration")

# Service Account JSON upload
service_account_file = st.sidebar.file_uploader(
    "📁 Upload Google Service Account JSON", 
    type=["json"],
    help="Upload your Google Service Account JSON file to authenticate with Google Sheets"
)

service_account_info = None
if service_account_file is not None:
    try:
        service_account_info = json.load(service_account_file)
        st.sidebar.success("✅ Service Account JSON uploaded successfully!")
    except json.JSONDecodeError:
        st.sidebar.error("❌ Invalid JSON file. Please upload a valid Service Account JSON.")

# Sheet configuration
st.sidebar.subheader("📊 Sheet Configuration")
sheet_id = st.sidebar.text_input(
    "Google Sheet ID", 
    value="1WNFuryFtCQ9j8Wp1DTR0WhGkkxpkqU2ZgQ6SQ6wk3d4",
    help="Enter the Google Sheet ID from the URL"
)
sheet_name = st.sidebar.text_input(
    "Sheet Name", 
    value="Sheet1",
    help="Enter the name of the worksheet tab"
)

# Connect to Google Sheets
if service_account_info and sheet_id and sheet_name:
    df = fetch_data(sheet_id, sheet_name, service_account_info)
    
    if not df.empty:
        # Main content area
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <h3>{len(df)}</h3>
                <p>Total Business Plans</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            unique_founders = df['Name'].nunique()
            st.markdown(f"""
            <div class="metric-card">
                <h3>{unique_founders}</h3>
                <p>Unique Founders</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            # Calculate average startup costs
            df['startup_costs_numeric'] = df['Startup Costs'].apply(extract_numeric_value)
            avg_costs = df['startup_costs_numeric'].mean()
            st.markdown(f"""
            <div class="metric-card">
                <h3>${avg_costs:,.0f}</h3>
                <p>Avg Startup Costs</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            # Count non-empty business ideas
            valid_ideas = df['Business Idea'].notna().sum()
            st.markdown(f"""
            <div class="metric-card">
                <h3>{valid_ideas}</h3>
                <p>Complete Ideas</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Filters and Search
        st.subheader("🔍 Search & Filter")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            search_term = st.text_input("🔍 Search by Name or Business Name:")
        
        with col2:
            # Cost range filter
            min_cost, max_cost = st.slider(
                "💰 Startup Cost Range",
                min_value=0,
                max_value=int(df['startup_costs_numeric'].max()) if df['startup_costs_numeric'].max() > 0 else 100000,
                value=(0, int(df['startup_costs_numeric'].max()) if df['startup_costs_numeric'].max() > 0 else 100000),
                step=1000
            )
        
        with col3:
            # Sort options
            sort_by = st.selectbox(
                "📊 Sort by:",
                ["Name", "Business Name", "Startup Costs", "Email"]
            )
        
        # Apply filters
        df_filtered = df.copy()
        
        if search_term:
            df_filtered = df_filtered[
                df_filtered['Name'].str.contains(search_term, case=False, na=False) |
                df_filtered['Business Name'].str.contains(search_term, case=False, na=False)
            ]
        
        # Apply cost filter
        df_filtered = df_filtered[
            (df_filtered['startup_costs_numeric'] >= min_cost) &
            (df_filtered['startup_costs_numeric'] <= max_cost)
        ]
        
        # Sort data
        if sort_by == "Startup Costs":
            df_filtered = df_filtered.sort_values('startup_costs_numeric', ascending=False)
        else:
            df_filtered = df_filtered.sort_values(sort_by)
        
        st.markdown("---")
        
        # Data Visualization
        if len(df_filtered) > 0:
            st.subheader("📈 Data Insights")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Startup costs distribution
                if df_filtered['startup_costs_numeric'].sum() > 0:
                    fig_costs = px.histogram(
                        df_filtered, 
                        x='startup_costs_numeric',
                        title="Startup Costs Distribution",
                        labels={'startup_costs_numeric': 'Startup Costs ($)', 'count': 'Number of Businesses'},
                        color_discrete_sequence=['#2196f3']
                    )
                    fig_costs.update_layout(
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)'
                    )
                    st.plotly_chart(fig_costs, use_container_width=True)
            
            with col2:
                # Top business names by startup costs
                top_businesses = df_filtered.nlargest(10, 'startup_costs_numeric')
                if len(top_businesses) > 0:
                    fig_top = px.bar(
                        top_businesses,
                        x='startup_costs_numeric',
                        y='Business Name',
                        orientation='h',
                        title="Top Businesses by Startup Costs",
                        labels={'startup_costs_numeric': 'Startup Costs ($)', 'Business Name': 'Business'},
                        color_discrete_sequence=['#21cbf3']
                    )
                    fig_top.update_layout(
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)'
                    )
                    st.plotly_chart(fig_top, use_container_width=True)
            
            st.markdown("---")
            
            # Business Plans Display
            st.subheader(f"📋 Business Plans ({len(df_filtered)} found)")
            
            # Pagination
            items_per_page = st.selectbox("Items per page:", [5, 10, 20, 50], index=1)
            total_pages = (len(df_filtered) - 1) // items_per_page + 1
            
            if total_pages > 1:
                page = st.selectbox("Page:", range(1, total_pages + 1))
                start_idx = (page - 1) * items_per_page
                end_idx = start_idx + items_per_page
                df_page = df_filtered.iloc[start_idx:end_idx]
            else:
                df_page = df_filtered
            
            # Display business cards
            for index, row in df_page.iterrows():
                create_business_card(row)
                
                # Add edit button for each business plan
                with st.expander(f"✏️ Edit {row['Business Name']}", expanded=False):
                    st.info("Edit functionality will be implemented in the next version.")
                    st.write("This will allow you to modify business plan details directly.")
        
        else:
            st.warning("No business plans match your current filters.")
    
    else:
        st.warning("No data found in the specified sheet or unable to connect.")

else:
    # Welcome screen
    st.markdown("""
    <div style="text-align: center; padding: 50px;">
        <h2 style="color: #1976d2;">Welcome to Business Plan Viewer! 🚀</h2>
        <p style="font-size: 18px; color: #666;">
            To get started, please:
        </p>
        <ol style="text-align: left; display: inline-block; font-size: 16px; color: #666;">
            <li>Upload your Google Service Account JSON file in the sidebar</li>
            <li>Enter your Google Sheet ID and Sheet Name</li>
            <li>Start exploring your business plans with advanced filtering and visualization!</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 20px;">
    <p>📊 Business Plan Viewer & Manager | Built with Streamlit & ❤️</p>
</div>
""", unsafe_allow_html=True)

