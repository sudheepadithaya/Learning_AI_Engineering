"""
Interactive Bikeshare Data Explorer Web Application
=================================================
A comprehensive, visual web application for exploring bikeshare data with
interactive charts, maps, and advanced analytics.

Run with: streamlit run bikeshare_webapp.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import folium
from streamlit_folium import folium_static
from datetime import datetime, timedelta
import warnings
from pathlib import Path
import time
from typing import Dict, Optional, Tuple

# Configure page
st.set_page_config(
    page_title="🚴 Bikeshare Explorer",
    page_icon="🚴",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Suppress warnings
warnings.filterwarnings('ignore')

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        background: linear-gradient(90deg, #ff6b6b, #4ecdc4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #4ecdc4;
    }
    .stMetric {
        background-color: #ffffff;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)


class BikeshareWebApp:
    """Interactive Bikeshare Web Application"""
    
    CITY_DATA = {
        'Chicago': 'chicago.csv',
        'New York City': 'new_york_city.csv',
        'Washington': 'washington.csv'
    }
    
    # Sample coordinates for cities (for map visualization)
    CITY_COORDS = {
        'Chicago': [41.8781, -87.6298],
        'New York City': [40.7589, -73.9851],
        'Washington': [38.9072, -77.0369]
    }
    
    def __init__(self):
        """Initialize the web application."""
        self.df = None
        self.init_session_state()
    
    def init_session_state(self):
        """Initialize session state variables."""
        if 'data_loaded' not in st.session_state:
            st.session_state.data_loaded = False
        if 'df' not in st.session_state:
            st.session_state.df = None
    
    @st.cache_data
    def load_data(_self, city: str) -> pd.DataFrame:
        """Load and preprocess data with caching."""
        try:
            file_path = Path(_self.CITY_DATA[city])
            if not file_path.exists():
                st.error(f"Data file not found: {file_path}")
                return pd.DataFrame()
            
            # Load data
            df = pd.read_csv(file_path)
            
            # Preprocess
            df['Start Time'] = pd.to_datetime(df['Start Time'], errors='coerce')
            df = df.dropna(subset=['Start Time'])
            
            # Create additional features
            df['month'] = df['Start Time'].dt.month
            df['day_of_week'] = df['Start Time'].dt.day_name()
            df['hour'] = df['Start Time'].dt.hour
            df['date'] = df['Start Time'].dt.date
            df['is_weekend'] = df['day_of_week'].isin(['Saturday', 'Sunday'])
            
            # Create route column
            if 'Start Station' in df.columns and 'End Station' in df.columns:
                df['route'] = df['Start Station'] + ' → ' + df['End Station']
            
            return df
            
        except Exception as e:
            st.error(f"Error loading data: {e}")
            return pd.DataFrame()
    
    def filter_data(self, df: pd.DataFrame, month_filter: str, day_filter: str, 
                   hour_range: Tuple[int, int]) -> pd.DataFrame:
        """Apply filters to the data."""
        filtered_df = df.copy()
        
        # Month filter
        if month_filter != 'All':
            month_num = ['All', 'January', 'February', 'March', 'April', 'May', 'June'].index(month_filter)
            filtered_df = filtered_df[filtered_df['month'] == month_num]
        
        # Day filter
        if day_filter != 'All':
            filtered_df = filtered_df[filtered_df['day_of_week'] == day_filter]
        
        # Hour range filter
        filtered_df = filtered_df[
            (filtered_df['hour'] >= hour_range[0]) & 
            (filtered_df['hour'] <= hour_range[1])
        ]
        
        return filtered_df
    
    def create_sidebar(self) -> Tuple[str, str, str, Tuple[int, int]]:
        """Create sidebar with filters and controls."""
        st.sidebar.markdown("# 🎛️ Control Panel")
        
        # City selection
        city = st.sidebar.selectbox(
            "🏙️ Select City",
            options=list(self.CITY_DATA.keys()),
            help="Choose which city's data to analyze"
        )
        
        # Month filter
        month = st.sidebar.selectbox(
            "📅 Filter by Month",
            options=['All', 'January', 'February', 'March', 'April', 'May', 'June'],
            help="Filter data by specific month"
        )
        
        # Day filter
        day = st.sidebar.selectbox(
            "📆 Filter by Day",
            options=['All', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
            help="Filter data by day of the week"
        )
        
        # Hour range filter
        hour_range = st.sidebar.slider(
            "🕐 Hour Range",
            min_value=0,
            max_value=23,
            value=(0, 23),
            help="Filter data by hour of the day"
        )
        
        # Additional controls
        st.sidebar.markdown("---")
        st.sidebar.markdown("### 📊 Display Options")
        
        return city, month, day, hour_range
    
    def display_overview_metrics(self, df: pd.DataFrame):
        """Display key metrics in an attractive layout."""
        if df.empty:
            return
        
        st.markdown("## 📊 Quick Overview")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="🚴 Total Trips",
                value=f"{len(df):,}",
                delta=f"Data from {df['Start Time'].min().date()} to {df['Start Time'].max().date()}"
            )
        
        with col2:
            if 'Trip Duration' in df.columns:
                avg_duration = df['Trip Duration'].mean() / 60  # Convert to minutes
                st.metric(
                    label="⏱️ Avg Trip Duration",
                    value=f"{avg_duration:.1f} min",
                    delta=f"Range: {df['Trip Duration'].min()/60:.1f} - {df['Trip Duration'].max()/60:.1f} min"
                )
        
        with col3:
            unique_stations = df['Start Station'].nunique() if 'Start Station' in df.columns else 0
            st.metric(
                label="🚉 Unique Stations",
                value=f"{unique_stations:,}",
                delta=f"Start & End combined"
            )
        
        with col4:
            if 'User Type' in df.columns:
                subscriber_pct = (df['User Type'] == 'Subscriber').mean() * 100
                st.metric(
                    label="👥 Subscriber Rate",
                    value=f"{subscriber_pct:.1f}%",
                    delta="of all users"
                )
    
    def create_time_analysis_charts(self, df: pd.DataFrame):
        """Create comprehensive time-based analysis charts."""
        if df.empty:
            return
        
        st.markdown("## ⏰ Time Pattern Analysis")
        
        # Hourly distribution
        col1, col2 = st.columns(2)
        
        with col1:
            hourly_data = df.groupby('hour').size().reset_index(name='trips')
            fig_hourly = px.bar(
                hourly_data, 
                x='hour', 
                y='trips',
                title="🕐 Trips by Hour of Day",
                labels={'hour': 'Hour', 'trips': 'Number of Trips'},
                color='trips',
                color_continuous_scale='viridis'
            )
            fig_hourly.update_layout(showlegend=False)
            st.plotly_chart(fig_hourly, use_container_width=True)
        
        with col2:
            daily_data = df.groupby('day_of_week').size().reset_index(name='trips')
            # Reorder days
            day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            daily_data['day_of_week'] = pd.Categorical(daily_data['day_of_week'], categories=day_order, ordered=True)
            daily_data = daily_data.sort_values('day_of_week')
            
            fig_daily = px.bar(
                daily_data,
                x='day_of_week',
                y='trips',
                title="📅 Trips by Day of Week",
                labels={'day_of_week': 'Day', 'trips': 'Number of Trips'},
                color='trips',
                color_continuous_scale='plasma'
            )
            fig_daily.update_layout(showlegend=False)
            st.plotly_chart(fig_daily, use_container_width=True)
        
        # Heatmap of hour vs day
        if len(df) > 0:
            pivot_data = df.pivot_table(
                values='Start Time',
                index='hour',
                columns='day_of_week',
                aggfunc='count',
                fill_value=0
            )
            
            # Reorder columns
            day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            pivot_data = pivot_data.reindex(columns=day_order)
            
            fig_heatmap = px.imshow(
                pivot_data,
                title="🔥 Trip Intensity Heatmap (Hour vs Day)",
                labels=dict(x="Day of Week", y="Hour of Day", color="Number of Trips"),
                color_continuous_scale='YlOrRd'
            )
            st.plotly_chart(fig_heatmap, use_container_width=True)
    
    def create_station_analysis(self, df: pd.DataFrame):
        """Create station popularity and route analysis."""
        if df.empty or 'Start Station' not in df.columns:
            return
        
        st.markdown("## 🚉 Station & Route Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Top start stations
            top_start = df['Start Station'].value_counts().head(10).reset_index()
            top_start.columns = ['Station', 'Trips']
            
            fig_start = px.bar(
                top_start,
                x='Trips',
                y='Station',
                orientation='h',
                title="🚀 Top 10 Start Stations",
                labels={'Trips': 'Number of Trips', 'Station': 'Station Name'},
                color='Trips',
                color_continuous_scale='blues'
            )
            fig_start.update_layout(yaxis={'categoryorder':'total ascending'})
            st.plotly_chart(fig_start, use_container_width=True)
        
        with col2:
            # Top end stations
            if 'End Station' in df.columns:
                top_end = df['End Station'].value_counts().head(10).reset_index()
                top_end.columns = ['Station', 'Trips']
                
                fig_end = px.bar(
                    top_end,
                    x='Trips',
                    y='Station',
                    orientation='h',
                    title="🏁 Top 10 End Stations",
                    labels={'Trips': 'Number of Trips', 'Station': 'Station Name'},
                    color='Trips',
                    color_continuous_scale='reds'
                )
                fig_end.update_layout(yaxis={'categoryorder':'total ascending'})
                st.plotly_chart(fig_end, use_container_width=True)
        
        # Top routes
        if 'route' in df.columns:
            top_routes = df['route'].value_counts().head(10).reset_index()
            top_routes.columns = ['Route', 'Trips']
            
            fig_routes = px.bar(
                top_routes,
                x='Trips',
                y='Route',
                orientation='h',
                title="🛣️ Top 10 Popular Routes",
                labels={'Trips': 'Number of Trips', 'Route': 'Route'},
                color='Trips',
                color_continuous_scale='greens'
            )
            fig_routes.update_layout(yaxis={'categoryorder':'total ascending'})
            st.plotly_chart(fig_routes, use_container_width=True)
    
    def create_user_demographics_analysis(self, df: pd.DataFrame):
        """Create user demographics visualizations."""
        if df.empty:
            return
        
        st.markdown("## 👥 User Demographics")
        
        col1, col2, col3 = st.columns(3)
        
        # User Type Distribution
        if 'User Type' in df.columns:
            with col1:
                user_type_data = df['User Type'].value_counts().reset_index()
                user_type_data.columns = ['User Type', 'Count']
                
                fig_user_type = px.pie(
                    user_type_data,
                    values='Count',
                    names='User Type',
                    title="📋 User Type Distribution",
                    color_discrete_sequence=px.colors.qualitative.Set3
                )
                st.plotly_chart(fig_user_type, use_container_width=True)
        
        # Gender Distribution
        if 'Gender' in df.columns:
            with col2:
                gender_data = df['Gender'].value_counts().reset_index()
                gender_data.columns = ['Gender', 'Count']
                
                fig_gender = px.pie(
                    gender_data,
                    values='Count',
                    names='Gender',
                    title="⚥ Gender Distribution",
                    color_discrete_sequence=px.colors.qualitative.Pastel
                )
                st.plotly_chart(fig_gender, use_container_width=True)
        
        # Age Distribution
        if 'Birth Year' in df.columns:
            with col3:
                birth_years = df['Birth Year'].dropna()
                if not birth_years.empty:
                    current_year = datetime.now().year
                    ages = current_year - birth_years
                    
                    fig_age = px.histogram(
                        x=ages,
                        nbins=30,
                        title="🎂 Age Distribution",
                        labels={'x': 'Age', 'y': 'Count'},
                        color_discrete_sequence=['#ff6b6b']
                    )
                    st.plotly_chart(fig_age, use_container_width=True)
    
    def create_advanced_analytics(self, df: pd.DataFrame):
        """Create advanced analytics and insights."""
        if df.empty:
            return
        
        st.markdown("## 📈 Advanced Analytics")
        
        # Trip duration analysis
        if 'Trip Duration' in df.columns:
            col1, col2 = st.columns(2)
            
            with col1:
                # Trip duration distribution
                fig_duration = px.histogram(
                    df,
                    x='Trip Duration',
                    nbins=50,
                    title="⏱️ Trip Duration Distribution",
                    labels={'Trip Duration': 'Duration (seconds)', 'count': 'Number of Trips'}
                )
                fig_duration.update_layout(
                    xaxis=dict(range=[0, df['Trip Duration'].quantile(0.95)])  # Remove outliers for better view
                )
                st.plotly_chart(fig_duration, use_container_width=True)
            
            with col2:
                # Average trip duration by hour
                hourly_duration = df.groupby('hour')['Trip Duration'].mean().reset_index()
                hourly_duration['Trip Duration (min)'] = hourly_duration['Trip Duration'] / 60
                
                fig_hourly_duration = px.line(
                    hourly_duration,
                    x='hour',
                    y='Trip Duration (min)',
                    title="📊 Average Trip Duration by Hour",
                    labels={'hour': 'Hour of Day', 'Trip Duration (min)': 'Average Duration (minutes)'},
                    markers=True
                )
                st.plotly_chart(fig_hourly_duration, use_container_width=True)
        
        # Weekend vs Weekday comparison
        weekend_comparison = df.groupby('is_weekend').size().reset_index(name='trips')
        weekend_comparison['Day Type'] = weekend_comparison['is_weekend'].map({True: 'Weekend', False: 'Weekday'})
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig_weekend = px.bar(
                weekend_comparison,
                x='Day Type',
                y='trips',
                title="📅 Weekend vs Weekday Usage",
                labels={'trips': 'Number of Trips', 'Day Type': 'Day Type'},
                color='Day Type',
                color_discrete_sequence=['#ff9999', '#66b3ff']
            )
            st.plotly_chart(fig_weekend, use_container_width=True)
        
        with col2:
            # Monthly trend (if data spans multiple months)
            if df['month'].nunique() > 1:
                monthly_data = df.groupby('month').size().reset_index(name='trips')
                month_names = ['', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
                monthly_data['Month'] = monthly_data['month'].map(lambda x: month_names[x] if x < len(month_names) else str(x))
                
                fig_monthly = px.line(
                    monthly_data,
                    x='Month',
                    y='trips',
                    title="📈 Monthly Usage Trend",
                    labels={'trips': 'Number of Trips', 'Month': 'Month'},
                    markers=True
                )
                st.plotly_chart(fig_monthly, use_container_width=True)
    
    def create_city_map(self, city: str, df: pd.DataFrame):
        """Create an interactive map for the selected city."""
        st.markdown("## 🗺️ Interactive City Map")
        
        if city not in self.CITY_COORDS:
            st.warning("Map data not available for this city.")
            return
        
        # Create base map
        center_coords = self.CITY_COORDS[city]
        m = folium.Map(location=center_coords, zoom_start=12, tiles='OpenStreetMap')
        
        # Add city center marker
        folium.Marker(
            center_coords,
            popup=f"{city} City Center",
            tooltip=f"{city} City Center",
            icon=folium.Icon(color='red', icon='star')
        ).add_to(m)
        
        # Add information box
        st.info(f"🗺️ This is a representative map of {city}. In a full implementation, actual station locations would be plotted here with trip data overlays.")
        
        # Display map
        folium_static(m, width=700, height=500)
    
    def create_download_section(self, df: pd.DataFrame):
        """Create download section for filtered data."""
        if df.empty:
            return
        
        st.markdown("## 💾 Download Data")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # Download filtered data as CSV
            csv = df.to_csv(index=False)
            st.download_button(
                label="📄 Download as CSV",
                data=csv,
                file_name=f"bikeshare_filtered_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
        
        with col2:
            # Download summary statistics
            summary_stats = df.describe().to_csv()
            st.download_button(
                label="📊 Download Summary Stats",
                data=summary_stats,
                file_name=f"bikeshare_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
        
        with col3:
            st.info(f"💡 Total filtered records: {len(df):,}")
    
    def run(self):
        """Run the main application."""
        # Header
        st.markdown('<h1 class="main-header">🚴 Interactive Bikeshare Data Explorer</h1>', unsafe_allow_html=True)
        st.markdown("### Explore bikeshare patterns with interactive visualizations and advanced analytics")
        
        # Sidebar controls
        city, month, day, hour_range = self.create_sidebar()
        
        # Load data
        with st.spinner(f"Loading data for {city}..."):
            df = self.load_data(city)
        
        if df.empty:
            st.error("❌ No data available. Please ensure the data files are in the correct location.")
            return
        
        # Apply filters
        filtered_df = self.filter_data(df, month, day, hour_range)
        
        if filtered_df.empty:
            st.warning("⚠️ No data matches the selected filters. Please adjust your criteria.")
            return
        
        # Display filter summary
        st.success(f"✅ Loaded {len(filtered_df):,} trips from {city} (filtered from {len(df):,} total)")
        
        # Main content
        self.display_overview_metrics(filtered_df)
        
        # Create tabs for different analyses
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
            "⏰ Time Analysis", 
            "🚉 Stations & Routes", 
            "👥 Demographics", 
            "📈 Advanced Analytics", 
            "🗺️ Map View",
            "💾 Data Export"
        ])
        
        with tab1:
            self.create_time_analysis_charts(filtered_df)
        
        with tab2:
            self.create_station_analysis(filtered_df)
        
        with tab3:
            self.create_user_demographics_analysis(filtered_df)
        
        with tab4:
            self.create_advanced_analytics(filtered_df)
        
        with tab5:
            self.create_city_map(city, filtered_df)
        
        with tab6:
            self.create_download_section(filtered_df)
        
        # Footer
        st.markdown("---")
        st.markdown("### 💡 About This App")
        st.info("""
        This interactive web application provides comprehensive analysis of bikeshare data with:
        - **Interactive Filtering**: Filter by city, month, day, and hour
        - **Visual Analytics**: Charts, graphs, and heatmaps
        - **Station Analysis**: Popular stations and routes
        - **User Demographics**: Age, gender, and user type analysis
        - **Advanced Insights**: Trip patterns and usage trends
        - **Data Export**: Download filtered data and statistics
        
        Built with Streamlit, Plotly, and advanced data science techniques.
        """)


def main():
    """Main function to run the web application."""
    app = BikeshareWebApp()
    app.run()


if __name__ == "__main__":
    main()