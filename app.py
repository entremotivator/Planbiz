import streamlit as st
import pandas as pd
import requests
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import re
from datetime import datetime
import numpy as np
from collections import Counter
import io
import base64

# -------------------------------
# Page Configuration
# -------------------------------
st.set_page_config(
    page_title="Business Plan Analytics Dashboard",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced CSS with modern design
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
    
    .main {
        font-family: 'Poppins', sans-serif;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
    }
    
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    .business-card {
        background: linear-gradient(145deg, #ffffff 0%, #f8f9ff 100%);
        padding: 25px;
        border-radius: 20px;
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.15);
        margin: 20px 0;
        border-left: 6px solid #667eea;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        position: relative;
        overflow: hidden;
        color: #000000 !important;
    }
    
    .business-card * {
        color: #000000 !important;
    }
    
    .business-card h1,
    .business-card h2,
    .business-card h3,
    .business-card h4,
    .business-card h5,
    .business-card h6 {
        color: #667eea !important;
    }
    
    .business-card p,
    .business-card div,
    .business-card span,
    .business-card li {
        color: #000000 !important;
    }
    
    .business-card::before {
        content: '';
        position: absolute;
        top: 0;
        right: 0;
        width: 100px;
        height: 100px;
        background: linear-gradient(45deg, rgba(102, 126, 234, 0.1), rgba(118, 75, 162, 0.1));
        border-radius: 0 20px 0 100px;
    }
    
    .business-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px rgba(102, 126, 234, 0.25);
    }
    
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        margin: 10px;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
        transition: transform 0.3s ease;
    }
    
    .metric-card:hover {
        transform: scale(1.05);
    }
    
    .metric-number {
        font-size: 2.5em;
        font-weight: 700;
        margin-bottom: 5px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .metric-label {
        font-size: 1em;
        opacity: 0.9;
        font-weight: 300;
    }
    
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #f8f9ff 0%, #e8ecff 100%);
    }
    
    .main-header {
        text-align: center;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3em;
        font-weight: 700;
        margin-bottom: 10px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    .sub-header {
        text-align: center;
        color: #6c757d;
        font-size: 1.2em;
        margin-bottom: 40px;
        font-weight: 300;
    }
    
    .section-header {
        color: #495057;
        font-weight: 600;
        margin: 30px 0 20px 0;
        padding-bottom: 10px;
        border-bottom: 3px solid #667eea;
        display: inline-block;
    }
    
    .goal-timeline {
        background: #f8f9ff;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        border-left: 4px solid #667eea;
        color: #000000 !important;
    }
    
    .goal-timeline * {
        color: #000000 !important;
    }
    
    .goal-timeline h4 {
        color: #667eea !important;
    }
    
    .filter-container {
        background: white;
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        margin: 20px 0;
    }
    
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 20px;
        margin: 20px 0;
    }
    
    .welcome-container {
        background: white;
        padding: 50px;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        text-align: center;
        margin: 40px auto;
        max-width: 800px;
    }
    
    .feature-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 20px;
        margin: 30px 0;
    }
    
    .feature-card {
        background: #f8f9ff;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        border: 2px solid #e8ecff;
        transition: all 0.3s ease;
    }
    
    .feature-card:hover {
        border-color: #667eea;
        transform: translateY(-5px);
    }
    
    .export-button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    /* Force all text in Streamlit content to be black */
    .stMarkdown p,
    .stMarkdown div,
    .stMarkdown span,
    .stWrite p,
    .stWrite div,
    .stWrite span {
        color: #000000 !important;
    }
    
    /* Keep section headers with accent color */
    .stMarkdown h3,
    .stMarkdown h4 {
        color: #667eea !important;
    }
    
    /* Ensure tab content text is black */
    .stTabs [data-baseweb="tab-panel"] p,
    .stTabs [data-baseweb="tab-panel"] div {
        color: #000000 !important;
    }
</style>
""", unsafe_allow_html=True)

# -------------------------------
# Enhanced Helper Functions
# -------------------------------

@st.cache_data(ttl=300)
def fetch_public_sheet_data(sheet_id):
    """Fetch data from public Google Sheet using CSV export - pulls all sheets"""
    try:
        # Try multiple approaches to get the data
        urls_to_try = [
            f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv",  # Default sheet
            f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid=0",  # First sheet explicitly
            f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv",  # Alternative export method
        ]
        
        for url in urls_to_try:
            try:
                response = requests.get(url, timeout=10)
                response.raise_for_status()
                
                # Read CSV data
                df = pd.read_csv(io.StringIO(response.text))
                
                # Clean column names (remove extra spaces)
                df.columns = df.columns.str.strip()
                
                # Check if we got valid data
                if len(df) > 0 and len(df.columns) > 1:
                    return df
                    
            except Exception as e:
                continue  # Try next URL
        
        # If all URLs fail, raise an error
        raise Exception("Unable to fetch data from any of the attempted URLs")
        
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        st.info("💡 Tip: Make sure the Google Sheet is publicly accessible (Anyone with the link can view)")
        return pd.DataFrame()

def extract_numeric_value(text):
    """Enhanced numeric extraction with better handling"""
    if pd.isna(text) or text == "" or str(text).lower() in ['na', 'n/a', 'none', 'tbd']:
        return 0
    
    # Remove currency symbols and clean text
    clean_text = str(text).replace('$', '').replace(',', '').replace(' ', '')
    
    # Extract all numbers
    numbers = re.findall(r'\d+\.?\d*', clean_text)
    if numbers:
        try:
            return float(numbers[0])
        except ValueError:
            return 0
    return 0

def analyze_text_complexity(text):
    """Analyze text complexity and return metrics"""
    if pd.isna(text) or not text:
        return {"words": 0, "sentences": 0, "avg_word_length": 0}
    
    words = str(text).split()
    sentences = len(re.findall(r'[.!?]+', str(text)))
    avg_word_length = np.mean([len(word) for word in words]) if words else 0
    
    return {
        "words": len(words),
        "sentences": max(1, sentences),
        "avg_word_length": avg_word_length
    }

def extract_keywords(text, top_n=5):
    """Extract top keywords from text"""
    if pd.isna(text) or not text:
        return []
    
    # Simple keyword extraction
    words = re.findall(r'\b[a-zA-Z]{4,}\b', str(text).lower())
    # Remove common stop words
    stop_words = {'that', 'this', 'with', 'from', 'they', 'have', 'will', 'been', 'their', 'said', 'each', 'which'}
    words = [w for w in words if w not in stop_words]
    
    word_counts = Counter(words)
    return [word for word, count in word_counts.most_common(top_n)]

def create_enhanced_business_card(row, index):
    """Create an enhanced business card with more interactive elements"""
    
    # Calculate metrics
    idea_metrics = analyze_text_complexity(row.get('Business Idea', ''))
    startup_cost = extract_numeric_value(row.get('Startup Costs', 0))
    keywords = extract_keywords(row.get('Business Idea', ''))
    
    with st.container():
        st.markdown(f"""
        <div class="business-card">
            <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 20px;">
                <div style="flex: 1;">
                    <h2 style="color: #667eea !important; margin-bottom: 5px; font-weight: 700;">🚀 {row.get('Business Name', 'N/A')}</h2>
                    <p style="color: #000000 !important; font-size: 1.1em;"><strong>👤 Founder:</strong> {row.get('Name', 'N/A')}</p>
                    <p style="color: #000000 !important; font-size: 1.1em;"><strong>📧 Contact:</strong> {row.get('Email', 'N/A')}</p>
                </div>
                <div style="background: linear-gradient(135deg, #667eea, #764ba2); color: white; padding: 10px 15px; border-radius: 20px; font-weight: 600;">
                    #{index + 1}
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Create tabs for better organization
        tab1, tab2, tab3, tab4 = st.tabs(["💡 Business Overview", "🎯 Goals & Strategy", "💰 Financial & Market", "📊 Analytics"])
        
        with tab1:
            col1, col2 = st.columns([2, 1])
            with col1:
                st.markdown("### 💡 Business Concept")
                st.write(row.get('Business Idea', 'Not specified'))
                
                st.markdown("### 🛍️ Product/Service Description")
                st.write(row.get('Product or Service Description', 'Not specified'))
                
                st.markdown("### 🎯 Mission Statement")
                st.write(row.get('Mission Statement', 'Not specified'))
            
            with col2:
                st.markdown("### 📊 Quick Stats")
                st.metric("Idea Complexity", f"{idea_metrics['words']} words")
                st.metric("Startup Cost", f"${startup_cost:,.0f}")
                
                if keywords:
                    st.markdown("### 🔑 Key Themes")
                    for keyword in keywords[:3]:
                        st.code(keyword.title(), language=None)
        
        with tab2:
            st.markdown("### 🎯 Business Goals Timeline")
            
            goals_data = [
                ("3 Months", row.get('Business Goals (3 months)', 'Not specified')),
                ("6 Months", row.get('Business Goals (6 months)', 'Not specified')),
                ("12 Months", row.get('Business Goals (12 months)', 'Not specified'))
            ]
            
            for period, goal in goals_data:
                st.markdown(f"""
                <div class="goal-timeline">
                    <h4 style="color: #667eea !important; margin-bottom: 10px;">📅 {period}</h4>
                    <p style="margin: 0; color: #000000 !important;">{goal}</p>
                </div>
                """, unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("### 📢 Marketing Strategy")
                st.write(row.get('Marketing Plan', 'Not specified'))
            
            with col2:
                st.markdown("### 👥 Target Audience")
                st.write(row.get('Target Audience', 'Not specified'))
        
        with tab3:
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("### 💵 Pricing & Revenue")
                st.write(row.get('Pricing and Revenue Plan', 'Not specified'))
                
                st.markdown("### 💰 Startup Investment")
                st.write(row.get('Startup Costs', 'Not specified'))
            
            with col2:
                st.markdown("### 🏆 Competitive Edge")
                st.write(row.get('Competitors and Differentiation', 'Not specified'))
        
        with tab4:
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Business Idea", f"{idea_metrics['words']} words", f"{idea_metrics['sentences']} sentences")
            with col2:
                st.metric("Avg Word Length", f"{idea_metrics['avg_word_length']:.1f} chars")
            with col3:
                completeness = sum([1 for key in row.keys() if pd.notna(row[key]) and str(row[key]).strip() != ''])
                total_fields = len(row)
                st.metric("Completeness", f"{completeness}/{total_fields}", f"{(completeness/total_fields)*100:.1f}%")
            
            if row.get('Additional Notes or Support'):
                st.markdown("### 📝 Additional Notes")
                st.info(row.get('Additional Notes or Support'))
            
            if row.get('Plan Summary or Revision Preference'):
                st.markdown("### 📋 Plan Summary/Preferences")
                st.success(row.get('Plan Summary or Revision Preference'))
        
        st.markdown("</div>", unsafe_allow_html=True)

def create_analytics_dashboard(df):
    """Create comprehensive analytics dashboard"""
    
    st.markdown('<h2 class="section-header">📊 Advanced Analytics Dashboard</h2>', unsafe_allow_html=True)
    
    # Key Metrics Row
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-number">{len(df)}</div>
            <div class="metric-label">Total Plans</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        unique_founders = df['Name'].nunique()
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-number">{unique_founders}</div>
            <div class="metric-label">Unique Founders</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        df['startup_costs_numeric'] = df['Startup Costs'].apply(extract_numeric_value)
        avg_costs = df['startup_costs_numeric'].mean()
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-number">${avg_costs:,.0f}</div>
            <div class="metric-label">Avg Investment</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        complete_plans = df.apply(lambda row: sum([1 for val in row if pd.notna(val) and str(val).strip() != '']), axis=1)
        avg_completeness = (complete_plans / len(df.columns)).mean() * 100
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-number">{avg_completeness:.1f}%</div>
            <div class="metric-label">Avg Completeness</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col5:
        total_investment = df['startup_costs_numeric'].sum()
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-number">${total_investment:,.0f}</div>
            <div class="metric-label">Total Investment</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Charts Row 1
    col1, col2 = st.columns(2)
    
    with col1:
        # Investment Distribution
        if df['startup_costs_numeric'].sum() > 0:
            fig_dist = px.histogram(
                df[df['startup_costs_numeric'] > 0], 
                x='startup_costs_numeric',
                title="💰 Investment Distribution",
                labels={'startup_costs_numeric': 'Investment Amount ($)', 'count': 'Number of Businesses'},
                color_discrete_sequence=['#667eea'],
                nbins=20
            )
            fig_dist.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                title_font_size=16,
                title_font_color='#495057'
            )
            st.plotly_chart(fig_dist, use_container_width=True)
    
    with col2:
        # Top Investments
        top_investments = df.nlargest(10, 'startup_costs_numeric')
        if len(top_investments) > 0:
            fig_top = px.bar(
                top_investments,
                x='startup_costs_numeric',
                y='Business Name',
                orientation='h',
                title="🏆 Highest Investment Plans",
                labels={'startup_costs_numeric': 'Investment ($)', 'Business Name': 'Business'},
                color='startup_costs_numeric',
                color_continuous_scale='viridis'
            )
            fig_top.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                title_font_size=16,
                title_font_color='#495057'
            )
            st.plotly_chart(fig_top, use_container_width=True)
    
    # Charts Row 2
    col1, col2 = st.columns(2)
    
    with col1:
        # Business Plan Completeness
        completeness_scores = df.apply(lambda row: (sum([1 for val in row if pd.notna(val) and str(val).strip() != '']) / len(row)) * 100, axis=1)
        df['completeness'] = completeness_scores
        
        fig_complete = px.histogram(
            df,
            x='completeness',
            title="📋 Plan Completeness Distribution",
            labels={'completeness': 'Completeness (%)', 'count': 'Number of Plans'},
            color_discrete_sequence=['#764ba2'],
            nbins=15
        )
        fig_complete.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            title_font_size=16,
            title_font_color='#495057'
        )
        st.plotly_chart(fig_complete, use_container_width=True)
    
    with col2:
        # Word Count Analysis for Business Ideas
        df['idea_word_count'] = df['Business Idea'].apply(lambda x: len(str(x).split()) if pd.notna(x) else 0)
        
        fig_words = px.scatter(
            df,
            x='idea_word_count',
            y='startup_costs_numeric',
            title="💡 Idea Complexity vs Investment",
            labels={'idea_word_count': 'Words in Business Idea', 'startup_costs_numeric': 'Investment ($)'},
            color='completeness',
            color_continuous_scale='plasma',
            hover_data=['Business Name', 'Name']
        )
        fig_words.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            title_font_size=16,
            title_font_color='#495057'
        )
        st.plotly_chart(fig_words, use_container_width=True)

def export_data_to_csv(df):
    """Export filtered data to CSV"""
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="business_plans_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv" class="export-button">📥 Download CSV Report</a>'
    return href

def generate_business_insights(df):
    """Generate AI-powered business insights"""
    insights = []
    
    # Investment insights
    avg_investment = df['startup_costs_numeric'].mean()
    median_investment = df['startup_costs_numeric'].median()
    
    if avg_investment > median_investment * 1.5:
        insights.append("💡 There are some high-investment outliers that may represent scalable business models")
    
    # Completeness insights
    completeness_scores = df.apply(lambda row: (sum([1 for val in row if pd.notna(val) and str(val).strip() != '']) / len(row)) * 100, axis=1)
    avg_completeness = completeness_scores.mean()
    
    if avg_completeness < 70:
        insights.append("📝 Many business plans could benefit from more detailed information")
    
    # Word count insights
    df['idea_word_count'] = df['Business Idea'].apply(lambda x: len(str(x).split()) if pd.notna(x) else 0)
    avg_words = df['idea_word_count'].mean()
    
    if avg_words < 20:
        insights.append("💭 Business ideas could be more detailed - aim for 30+ words for clarity")
    
    return insights

def create_comparison_view(df, selected_plans):
    """Create side-by-side comparison of selected business plans"""
    if len(selected_plans) < 2:
        return
    
    st.markdown("### 🔄 Business Plan Comparison")
    
    cols = st.columns(len(selected_plans))
    
    for i, plan_idx in enumerate(selected_plans):
        with cols[i]:
            row = df.iloc[plan_idx]
            st.markdown(f"""
            <div style="border: 2px solid #667eea; border-radius: 10px; padding: 15px; margin: 5px;">
                <h4 style="color: #667eea;">{row['Business Name']}</h4>
                <p><strong>Founder:</strong> {row['Name']}</p>
                <p><strong>Investment:</strong> ${extract_numeric_value(row['Startup Costs']):,.0f}</p>
                <p><strong>Target:</strong> {row['Target Audience'][:100]}...</p>
            </div>
            """, unsafe_allow_html=True)

def log_usage_analytics():
    """Log basic usage analytics (privacy-friendly)"""
    if 'page_views' not in st.session_state:
        st.session_state.page_views = 0
    st.session_state.page_views += 1

# -------------------------------
# Main Application
# -------------------------------

st.markdown('<h1 class="main-header">🚀 Business Plan Analytics Hub</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Comprehensive Analysis & Insights for Entrepreneurial Success</p>', unsafe_allow_html=True)

# Initialize session state
log_usage_analytics()

# Sidebar Configuration
st.sidebar.markdown("## 📊 Data Source")
st.sidebar.success("✅ Connected to Default Business Plans Sheet")
st.sidebar.info("Using hardcoded Google Sheet with sample business plans")

# Hard-coded sheet configuration
sheet_id = "1WNFuryFtCQ9j8Wp1DTR0WhGkkxpkqU2ZgQ6SQ6wk3d4"

# Always fetch data with the hardcoded sheet (no GID needed)
if True:
    with st.spinner("🔄 Loading business plan data..."):
        df = fetch_public_sheet_data(sheet_id)
    
    if not df.empty:
        # Ensure all required columns exist
        required_columns = [
            'Name', 'Email', 'Business Idea', 'Business Name', 'Startup Costs',
            'Business Goals (3 months)', 'Business Goals (6 months)', 'Business Goals (12 months)',
            'Marketing Plan', 'Target Audience', 'Mission Statement', 'Pricing and Revenue Plan',
            'Product or Service Description', 'Competitors and Differentiation',
            'Additional Notes or Support', 'Plan Summary or Revision Preference'
        ]
        
        # Add missing columns with empty values
        for col in required_columns:
            if col not in df.columns:
                df[col] = ''
        
        # Create analytics dashboard
        create_analytics_dashboard(df)
        
        # Generate insights
        insights = generate_business_insights(df)
        if insights:
            st.markdown("### 🧠 Smart Insights")
            for insight in insights:
                st.info(insight)
        
        # Advanced Filters Section
        st.markdown('<div class="filter-container">', unsafe_allow_html=True)
        st.markdown('<h2 class="section-header">🔍 Advanced Search & Filtering</h2>', unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            search_term = st.text_input("🔍 Search businesses:", placeholder="Enter business name or founder...")
        
        with col2:
            # Calculate cost range for slider
            df['startup_costs_numeric'] = df['Startup Costs'].apply(extract_numeric_value)
            max_cost = max(df['startup_costs_numeric'].max(), 1000)
            cost_range = st.slider(
                "💰 Investment Range ($)",
                min_value=0,
                max_value=int(max_cost),
                value=(0, int(max_cost)),
                step=100
            )
        
        with col3:
            # Completeness filter
            completeness_threshold = st.slider(
                "📋 Min Completeness (%)",
                min_value=0,
                max_value=100,
                value=0,
                step=5
            )
        
        with col4:
            sort_options = {
                "Business Name": "Business Name",
                "Founder Name": "Name", 
                "Investment (High-Low)": "startup_costs_numeric_desc",
                "Investment (Low-High)": "startup_costs_numeric_asc",
                "Completeness": "completeness_desc"
            }
            sort_by = st.selectbox("📊 Sort by:", list(sort_options.keys()))
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Apply filters
        df_filtered = df.copy()
        
        # Text search
        if search_term:
            mask = (
                df_filtered['Name'].str.contains(search_term, case=False, na=False) |
                df_filtered['Business Name'].str.contains(search_term, case=False, na=False) |
                df_filtered['Business Idea'].str.contains(search_term, case=False, na=False)
            )
            df_filtered = df_filtered[mask]
        
        # Cost filter
        df_filtered = df_filtered[
            (df_filtered['startup_costs_numeric'] >= cost_range[0]) &
            (df_filtered['startup_costs_numeric'] <= cost_range[1])
        ]
        
        # Completeness filter
        if completeness_threshold > 0:
            completeness_scores = df_filtered.apply(
                lambda row: (sum([1 for val in row if pd.notna(val) and str(val).strip() != '']) / len(row)) * 100, 
                axis=1
            )
            df_filtered = df_filtered[completeness_scores >= completeness_threshold]
        
        # Sorting
        if sort_by == "Investment (High-Low)":
            df_filtered = df_filtered.sort_values('startup_costs_numeric', ascending=False)
        elif sort_by == "Investment (Low-High)":
            df_filtered = df_filtered.sort_values('startup_costs_numeric', ascending=True)
        elif sort_by == "Completeness":
            completeness_scores = df_filtered.apply(
                lambda row: (sum([1 for val in row if pd.notna(val) and str(val).strip() != '']) / len(row)) * 100, 
                axis=1
            )
            df_filtered = df_filtered.iloc[completeness_scores.sort_values(ascending=False).index]
        else:
            df_filtered = df_filtered.sort_values(sort_options[sort_by], na_position='last')
        
        # Export functionality
        if len(df_filtered) > 0:
            col1, col2, col3 = st.columns([1, 1, 2])
            with col1:
                st.markdown(export_data_to_csv(df_filtered), unsafe_allow_html=True)
            with col2:
                st.info(f"📊 Showing {len(df_filtered)} of {len(df)} plans")
        
        st.markdown("---")
        
        # Business Plans Display
        if len(df_filtered) > 0:
            st.markdown('<h2 class="section-header">📋 Business Plan Showcase</h2>', unsafe_allow_html=True)
            
            # Pagination
            col1, col2 = st.columns([1, 3])
            with col1:
                items_per_page = st.selectbox("📄 Plans per page:", [5, 10, 20], index=1)
            
            total_pages = (len(df_filtered) - 1) // items_per_page + 1
            
            if total_pages > 1:
                with col2:
                    page = st.selectbox("📖 Page:", range(1, total_pages + 1))
                start_idx = (page - 1) * items_per_page
                end_idx = start_idx + items_per_page
                df_page = df_filtered.iloc[start_idx:end_idx]
            else:
                df_page = df_filtered
                start_idx = 0
            
            # Display enhanced business cards
            for index, row in df_page.iterrows():
                create_enhanced_business_card(row, start_idx + df_page.index.get_loc(index) if total_pages > 1 else index)
        
        else:
            st.markdown("""
            <div class="welcome-container">
                <h2 style="color: #667eea;">🔍 No Results Found</h2>
                <p>Try adjusting your filters to see more business plans.</p>
            </div>
            """, unsafe_allow_html=True)
    
    else:
        st.error("❌ Unable to fetch data from the Google Sheet.")
        st.markdown("""
        ### 🔧 Troubleshooting Steps:
        1. **Check Sheet Access**: Ensure the Google Sheet is publicly accessible
        2. **Verify Link**: The sheet link should work when opened in a browser
        3. **Sheet Format**: Make sure the sheet contains the expected columns
        4. **Try Refresh**: Sometimes a simple page refresh resolves connectivity issues
        
        ### 📊 Expected Data Format:
        The sheet should contain business plan data with columns like:
        - Name, Email, Business Name, Business Idea, Startup Costs, etc.
        
        ### 🔗 Current Sheet: 
        [https://docs.google.com/spreadsheets/d/1WNFuryFtCQ9j8Wp1DTR0WhGkkxpkqU2ZgQ6SQ6wk3d4/](https://docs.google.com/spreadsheets/d/1WNFuryFtCQ9j8Wp1DTR0WhGkkxpkqU2ZgQ6SQ6wk3d4/)
        """, unsafe_allow_html=True)

else:
    # Enhanced welcome screen
    st.markdown("""
    <div class="welcome-container">
        <h2 style="color: #667eea; margin-bottom: 20px;">Welcome to the Business Plan Analytics Hub! 🎯</h2>
        <p style="font-size: 1.2em; color: #6c757d; margin-bottom: 30px;">
            Unlock powerful insights from entrepreneurial business plans with advanced analytics and interactive visualizations.
        </p>
        
        <div class="feature-grid">
            <div class="feature-card">
                <h3 style="color: #667eea;">📊 Advanced Analytics</h3>
                <p>Comprehensive metrics, distributions, and trend analysis</p>
            </div>
            <div class="feature-card">
                <h3 style="color: #667eea;">🔍 Smart Filtering</h3>
                <p>Multi-dimensional search and filtering capabilities</p>
            </div>
            <div class="feature-card">
                <h3 style="color: #667eea;">📈 Interactive Visualizations</h3>
                <p>Dynamic charts and graphs for data exploration</p>
            </div>
            <div class="feature-card">
                <h3 style="color: #667eea;">📋 Detailed Plan Views</h3>
                <p>Comprehensive business plan analysis with tabs</p>
            </div>
            <div class="feature-card">
                <h3 style="color: #667eea;">📥 Export Capabilities</h3>
                <p>Download filtered data as CSV reports</p>
            </div>
            <div class="feature-card">
                <h3 style="color: #667eea;">🚀 Real-time Updates</h3>
                <p>Live data fetching from Google Sheets</p>
            </div>
        </div>
        
        <div style="margin-top: 40px; padding: 30px; background: #f8f9ff; border-radius: 15px; border-left: 5px solid #667eea;">
            <h3 style="color: #495057; margin-bottom: 20px;">🚀 Ready to Explore!</h3>
            <div style="text-align: left; max-width: 600px; margin: 0 auto;">
                <p style="margin-bottom: 15px;"><strong>📊</strong> Real business plan data is automatically loaded</p>
                <p style="margin-bottom: 15px;"><strong>🔍</strong> Use the search and filtering tools to find specific plans</p>
                <p style="margin-bottom: 15px;"><strong>📈</strong> Explore the interactive analytics dashboard above</p>
                <p style="margin-bottom: 15px;"><strong>📋</strong> Click through detailed business plan cards below</p>
                <p style="margin-bottom: 0;"><strong>📥</strong> Export filtered results as CSV reports</p>
            </div>
        </div>
        
        <div style="margin-top: 30px;">
            <p style="color: #6c757d; font-style: italic;">
                💡 Data Source: <a href="https://docs.google.com/spreadsheets/d/1WNFuryFtCQ9j8Wp1DTR0WhGkkxpkqU2ZgQ6SQ6wk3d4/edit?usp=drivesdk" target="_blank">View Original Google Sheet</a>
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Enhanced sidebar information
st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 Data Information")
st.sidebar.info("Connected to hardcoded business plans dataset with real entrepreneurial data.")

st.sidebar.markdown("### 🔗 Source Sheet")
st.sidebar.markdown("""
**Direct Link:**  
[View Google Sheet](https://docs.google.com/spreadsheets/d/1WNFuryFtCQ9j8Wp1DTR0WhGkkxpkqU2ZgQ6SQ6wk3d4/edit?usp=drivesdk)

**Sheet ID:** `1WNFuryFtCQ9j8Wp1DTR0WhGkkxpkqU2ZgQ6SQ6wk3d4`

**Data Loading:** Multiple URL attempts for maximum compatibility
""", unsafe_allow_html=True)

st.sidebar.markdown("### 📋 Data Columns")
with st.sidebar.expander("View All 16 Columns"):
    required_cols = [
        "Name", "Email", "Business Idea", "Business Name", "Startup Costs",
        "Business Goals (3 months)", "Business Goals (6 months)", "Business Goals (12 months)",
        "Marketing Plan", "Target Audience", "Mission Statement", "Pricing and Revenue Plan",
        "Product or Service Description", "Competitors and Differentiation",
        "Additional Notes or Support", "Plan Summary or Revision Preference"
    ]
    for col in required_cols:
        st.sidebar.write(f"• {col}")

st.sidebar.markdown("### 🎯 Features")
features = [
    "📊 Real-time analytics dashboard",
    "🔍 Advanced search & filtering",
    "📈 Interactive visualizations", 
    "📋 Detailed business plan cards",
    "📥 CSV export functionality",
    "📱 Responsive design",
    "🚀 Fast data loading with caching",
    "🧠 Smart business insights",
    "🎨 Modern UI/UX design"
]

for feature in features:
    st.sidebar.write(feature)

# Usage statistics in sidebar
if 'page_views' in st.session_state:
    st.sidebar.markdown("---")
    st.sidebar.metric("Session Views", st.session_state.page_views)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 30px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 15px; margin-top: 40px;">
    <h3 style="color: white; margin-bottom: 15px;">🚀 Business Plan Analytics Hub</h3>
    <p style="color: rgba(255,255,255,0.9); margin-bottom: 10px;">Empowering entrepreneurs with data-driven insights</p>
    <p style="color: rgba(255,255,255,0.7); font-size: 0.9em;">Built with Streamlit, Plotly & Python | Enhanced for Public Google Sheets</p>
    <p style="color: rgba(255,255,255,0.6); font-size: 0.8em; margin-top: 15px;">© 2025 | Version 2.0 | Supports all 16 required business plan columns</p>
</div>
""", unsafe_allow_html=True)
