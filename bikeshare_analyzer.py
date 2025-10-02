"""
Advanced Bikeshare Data Analysis Tool
=====================================
A comprehensive, object-oriented bikeshare data analyzer with enhanced features,
better error handling, and improved performance.
"""

import time
import pandas as pd
import numpy as np
from typing import Dict, Tuple, Optional, List
from pathlib import Path
import logging
from dataclasses import dataclass
from datetime import datetime
import warnings

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Suppress pandas warnings for cleaner output
warnings.filterwarnings('ignore')


@dataclass
class FilterConfig:
    """Configuration class for data filtering parameters."""
    city: str
    month: str
    day: str
    
    def __post_init__(self):
        """Validate filter parameters after initialization."""
        self.city = self.city.lower().strip()
        self.month = self.month.lower().strip()
        self.day = self.day.lower().strip()


class BikeShareAnalyzer:
    """
    Enhanced Bikeshare Data Analyzer with improved OOP design and advanced analytics.
    """
    
    CITY_DATA: Dict[str, str] = {
        'chicago': 'chicago.csv',
        'new york city': 'new_york_city.csv',
        'washington': 'washington.csv'
    }
    
    MONTHS = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
    DAYS = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    
    # Column name constants
    COL_START_STATION = 'Start Station'
    COL_END_STATION = 'End Station'
    COL_USER_TYPE = 'User Type'
    COL_START_TIME = 'Start Time'
    COL_TRIP_DURATION = 'Trip Duration'
    COL_GENDER = 'Gender'
    COL_BIRTH_YEAR = 'Birth Year'
    
    def __init__(self, data_directory: str = "."):
        """Initialize the analyzer with data directory path."""
        self.data_dir = Path(data_directory)
        self.df: Optional[pd.DataFrame] = None
        self.filters: Optional[FilterConfig] = None
        
    def validate_data_files(self) -> bool:
        """Validate that all required data files exist."""
        missing_files = []
        for city, filename in self.CITY_DATA.items():
            file_path = self.data_dir / filename
            if not file_path.exists():
                missing_files.append(f"{city}: {filename}")
        
        if missing_files:
            logger.error(f"Missing data files: {', '.join(missing_files)}")
            return False
        return True
    
    def get_user_filters(self) -> FilterConfig:
        """
        Enhanced user input collection with validation and better UX.
        
        Returns:
            FilterConfig: Validated filter configuration
        """
        print("\n🚴 Welcome to the Advanced Bikeshare Data Explorer! 🚴")
        print("=" * 60)
        
        # City selection with better formatting
        print("\n📍 Available Cities:")
        for i, city in enumerate(self.CITY_DATA.keys(), 1):
            print(f"  {i}. {city.title()}")
        
        city = self._get_validated_input(
            "Enter city name or number: ",
            self.CITY_DATA.keys(),
            allow_numbers=True
        )
        
        # Month selection
        print("\n📅 Available Months:")
        for i, month in enumerate(self.MONTHS, 1):
            print(f"  {i}. {month.title()}")
        
        month = self._get_validated_input(
            "Enter month name/number (or 'all' for no filter): ",
            self.MONTHS,
            allow_numbers=True
        )
        
        # Day selection
        print("\n📆 Available Days:")
        for i, day in enumerate(self.DAYS, 1):
            print(f"  {i}. {day.title()}")
        
        day = self._get_validated_input(
            "Enter day name/number (or 'all' for no filter): ",
            self.DAYS,
            allow_numbers=True
        )
        
        filters = FilterConfig(city, month, day)
        self.filters = filters
        
        print(f"\n✅ Selected filters: {filters.city.title()}, {filters.month.title()}, {filters.day.title()}")
        print("-" * 60)
        
        return filters
    
    def _get_validated_input(self, prompt: str, valid_options: List[str], allow_numbers: bool = False) -> str:
        """Helper method for validated user input with number support."""
        while True:
            try:
                user_input = input(prompt).strip().lower()
                
                # Handle numeric input
                if allow_numbers and user_input.isdigit():
                    index = int(user_input) - 1
                    if 0 <= index < len(valid_options):
                        return list(valid_options)[index]
                    else:
                        print(f"❌ Please enter a number between 1 and {len(valid_options)}")
                        continue
                
                # Handle text input
                if user_input in valid_options:
                    return user_input
                else:
                    print(f"❌ Invalid input. Please choose from: {', '.join(valid_options)}")
                    
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                exit(0)
            except Exception as e:
                logger.error(f"Input error: {e}")
                print("❌ Invalid input. Please try again.")
    
    def load_and_filter_data(self, filters: FilterConfig) -> pd.DataFrame:
        """
        Load and filter data with enhanced error handling and performance optimization.
        
        Args:
            filters: Filter configuration
            
        Returns:
            pd.DataFrame: Filtered dataframe
        """
        try:
            print(f"📊 Loading data for {filters.city.title()}...")
            start_time = time.time()
            
            # Load data with optimized dtypes
            file_path = self.data_dir / self.CITY_DATA[filters.city]
            
            # Optimize data types for better performance
            dtype_dict = {
                'Start Station': 'category',
                'End Station': 'category',
                'User Type': 'category'
            }
            
            df = pd.read_csv(file_path, dtype=dtype_dict)
            
            # Convert datetime with better error handling
            df['Start Time'] = pd.to_datetime(df['Start Time'], errors='coerce')
            df = df.dropna(subset=['Start Time'])  # Remove invalid dates
            
            # Create additional time-based features
            df['month'] = df['Start Time'].dt.month
            df['day_of_week'] = df['Start Time'].dt.day_name()
            df['hour'] = df['Start Time'].dt.hour
            df['date'] = df['Start Time'].dt.date
            
            # Apply filters efficiently
            if filters.month != 'all':
                month_num = self.MONTHS.index(filters.month)  # 0-based for 'all', 1-based for months
                df = df[df['month'] == month_num]
            
            if filters.day != 'all':
                df = df[df['day_of_week'] == filters.day.title()]
            
            load_time = time.time() - start_time
            print(f"✅ Loaded {len(df):,} records in {load_time:.2f} seconds")
            
            if len(df) == 0:
                print("⚠️  No data found for the selected filters. Please try different options.")
                return pd.DataFrame()
            
            self.df = df
            return df
            
        except FileNotFoundError:
            logger.error(f"Data file not found: {file_path}")
            raise
        except Exception as e:
            logger.error(f"Error loading data: {e}")
            raise
    
    def analyze_time_patterns(self) -> None:
        """Enhanced time pattern analysis with additional insights."""
        if self.df is None or len(self.df) == 0:
            return
            
        print('\n⏰ TIME PATTERN ANALYSIS')
        print('=' * 50)
        start_time = time.time()
        
        # Most common month
        if self.filters.month == 'all':
            common_month = self.df['month'].mode()[0]
            month_name = self.MONTHS[common_month] if common_month <= len(self.MONTHS) else 'Unknown'
            month_count = (self.df['month'] == common_month).sum()
            print(f"📅 Most popular month: {month_name.title()} ({month_count:,} trips)")
        
        # Most common day
        if self.filters.day == 'all':
            common_day = self.df['day_of_week'].mode()[0]
            day_count = (self.df['day_of_week'] == common_day).sum()
            print(f"📆 Most popular day: {common_day} ({day_count:,} trips)")
        
        # Peak hours analysis
        common_hour = self.df['hour'].mode()[0]
        hour_count = (self.df['hour'] == common_hour).sum()
        hour_12 = f"{common_hour % 12 or 12}{'AM' if common_hour < 12 else 'PM'}"
        print(f"🕐 Peak hour: {common_hour}:00 ({hour_12}) - {hour_count:,} trips")
        
        # Additional time insights
        print(f"🌅 Early morning trips (5-9 AM): {len(self.df[self.df['hour'].between(5, 9)]):,}")
        print(f"🌇 Evening rush trips (5-7 PM): {len(self.df[self.df['hour'].between(17, 19)]):,}")
        print(f"🌙 Night trips (10 PM-5 AM): {len(self.df[(self.df['hour'] >= 22) | (self.df['hour'] <= 5)]):,}")
        
        print(f"\n⚡ Analysis completed in {time.time() - start_time:.3f} seconds")
        print('-' * 50)
    
    def analyze_stations(self) -> None:
        """Enhanced station analysis with trip patterns."""
        if self.df is None or len(self.df) == 0:
            return
            
        print('\n🚉 STATION POPULARITY ANALYSIS')
        print('=' * 50)
        start_time = time.time()
        
        # Most popular start station
        start_station = self.df['Start Station'].mode()[0]
        start_count = (self.df['Start Station'] == start_station).sum()
        print(f"🚀 Most popular start station: {start_station}")
        print(f"   └─ {start_count:,} trips started here")
        
        # Most popular end station
        end_station = self.df['End Station'].mode()[0]
        end_count = (self.df['End Station'] == end_station).sum()
        print(f"🏁 Most popular end station: {end_station}")
        print(f"   └─ {end_count:,} trips ended here")
        
        # Most common trip route
        self.df['route'] = self.df['Start Station'] + ' → ' + self.df['End Station']
        common_route = self.df['route'].mode()[0]
        route_count = (self.df['route'] == common_route).sum()
        print(f"🛣️  Most popular route: {common_route}")
        print(f"   └─ {route_count:,} trips on this route")
        
        # Additional station insights
        unique_start = self.df['Start Station'].nunique()
        unique_end = self.df['End Station'].nunique()
        print(f"📊 Total unique start stations: {unique_start}")
        print(f"📊 Total unique end stations: {unique_end}")
        
        print(f"\n⚡ Analysis completed in {time.time() - start_time:.3f} seconds")
        print('-' * 50)
    
    def analyze_trip_duration(self) -> None:
        """Enhanced trip duration analysis with statistical insights."""
        if self.df is None or len(self.df) == 0 or 'Trip Duration' not in self.df.columns:
            print("\n⚠️  Trip duration data not available")
            return
            
        print('\n⏱️  TRIP DURATION ANALYSIS')
        print('=' * 50)
        start_time = time.time()
        
        duration_stats = self.df['Trip Duration'].describe()
        total_time = self.df['Trip Duration'].sum()
        
        # Convert seconds to readable format
        def format_duration(seconds):
            """Convert seconds to human-readable format."""
            if pd.isna(seconds):
                return "N/A"
            hours, remainder = divmod(int(seconds), 3600)
            minutes, secs = divmod(remainder, 60)
            if hours > 0:
                return f"{hours}h {minutes}m {secs}s"
            elif minutes > 0:
                return f"{minutes}m {secs}s"
            else:
                return f"{secs}s"
        
        print(f"📊 Total travel time: {format_duration(total_time)} ({total_time:,.0f} seconds)")
        print(f"📊 Average trip duration: {format_duration(duration_stats['mean'])}")
        print(f"📊 Median trip duration: {format_duration(duration_stats['50%'])}")
        print(f"📊 Shortest trip: {format_duration(duration_stats['min'])}")
        print(f"📊 Longest trip: {format_duration(duration_stats['max'])}")
        
        # Trip duration categories
        short_trips = len(self.df[self.df['Trip Duration'] <= 600])  # ≤ 10 minutes
        medium_trips = len(self.df[self.df['Trip Duration'].between(601, 1800)])  # 10-30 minutes
        long_trips = len(self.df[self.df['Trip Duration'] > 1800])  # > 30 minutes
        
        print(f"🚴 Short trips (≤10 min): {short_trips:,} ({short_trips/len(self.df)*100:.1f}%)")
        print(f"🚴 Medium trips (10-30 min): {medium_trips:,} ({medium_trips/len(self.df)*100:.1f}%)")
        print(f"🚴 Long trips (>30 min): {long_trips:,} ({long_trips/len(self.df)*100:.1f}%)")
        
        print(f"\n⚡ Analysis completed in {time.time() - start_time:.3f} seconds")
        print('-' * 50)
    
    def analyze_user_demographics(self) -> None:
        """Enhanced user demographic analysis."""
        if self.df is None or len(self.df) == 0:
            return
            
        print('\n👥 USER DEMOGRAPHICS ANALYSIS')
        print('=' * 50)
        start_time = time.time()
        
        # User type analysis
        if 'User Type' in self.df.columns:
            user_types = self.df['User Type'].value_counts()
            print("📋 User Type Distribution:")
            for user_type, count in user_types.items():
                percentage = count / len(self.df) * 100
                print(f"   {user_type}: {count:,} ({percentage:.1f}%)")
        
        # Gender analysis
        if 'Gender' in self.df.columns:
            gender_counts = self.df['Gender'].value_counts()
            print("\n⚥ Gender Distribution:")
            for gender, count in gender_counts.items():
                percentage = count / len(self.df) * 100
                print(f"   {gender}: {count:,} ({percentage:.1f}%)")
        else:
            print("\n⚠️  Gender data not available for this city")
        
        # Birth year analysis
        if 'Birth Year' in self.df.columns:
            birth_years = self.df['Birth Year'].dropna()
            if not birth_years.empty:
                print(f"\n🎂 Birth Year Statistics:")
                print(f"   Earliest: {int(birth_years.min())}")
                print(f"   Most recent: {int(birth_years.max())}")
                print(f"   Most common: {int(birth_years.mode()[0])}")
                print(f"   Average age (approx): {2024 - birth_years.mean():.0f} years")
                
                # Age groups
                current_year = datetime.now().year
                ages = current_year - birth_years
                
                young = len(ages[ages <= 25])
                adult = len(ages[ages.between(26, 45)])
                senior = len(ages[ages > 45])
                
                print(f"   Young (≤25): {young:,} ({young/len(birth_years)*100:.1f}%)")
                print(f"   Adult (26-45): {adult:,} ({adult/len(birth_years)*100:.1f}%)")
                print(f"   Senior (>45): {senior:,} ({senior/len(birth_years)*100:.1f}%)")
        else:
            print("\n⚠️  Birth year data not available for this city")
        
        print(f"\n⚡ Analysis completed in {time.time() - start_time:.3f} seconds")
        print('-' * 50)
    
    def analyze_usage_patterns(self) -> None:
        """New advanced analysis for usage patterns and trends."""
        if self.df is None or len(self.df) == 0:
            return
            
        print('\n📈 ADVANCED USAGE PATTERN ANALYSIS')
        print('=' * 50)
        start_time = time.time()
        
        # Daily patterns
        daily_usage = self.df.groupby('date').size()
        print(f"📊 Average daily trips: {daily_usage.mean():.0f}")
        print(f"📊 Busiest day: {daily_usage.idxmax()} ({daily_usage.max():,} trips)")
        print(f"📊 Quietest day: {daily_usage.idxmin()} ({daily_usage.min():,} trips)")
        
        # Hourly distribution
        hourly_usage = self.df.groupby('hour').size()
        peak_hours = hourly_usage.nlargest(3).index.tolist()
        print(f"📊 Top 3 peak hours: {', '.join([f'{h}:00' for h in peak_hours])}")
        
        # Weekend vs Weekday
        self.df['is_weekend'] = self.df['day_of_week'].isin(['Saturday', 'Sunday'])
        weekend_trips = self.df[self.df['is_weekend']].shape[0]
        weekday_trips = self.df[~self.df['is_weekend']].shape[0]
        
        if weekend_trips > 0 and weekday_trips > 0:
            print(f"📊 Weekend trips: {weekend_trips:,} ({weekend_trips/len(self.df)*100:.1f}%)")
            print(f"📊 Weekday trips: {weekday_trips:,} ({weekday_trips/len(self.df)*100:.1f}%)")
        
        # Station efficiency (trips per station)
        if 'Start Station' in self.df.columns:
            station_efficiency = self.df.groupby('Start Station').size()
            avg_trips_per_station = station_efficiency.mean()
            print(f"📊 Average trips per station: {avg_trips_per_station:.1f}")
            
            # Most and least active stations
            most_active = station_efficiency.idxmax()
            least_active = station_efficiency.idxmin()
            print(f"📊 Most active station: {most_active} ({station_efficiency.max():,} trips)")
            print(f"📊 Least active station: {least_active} ({station_efficiency.min():,} trips)")
        
        print(f"\n⚡ Analysis completed in {time.time() - start_time:.3f} seconds")
        print('-' * 50)
    
    def display_summary_stats(self) -> None:
        """Display comprehensive summary statistics."""
        if self.df is None or len(self.df) == 0:
            return
            
        print('\n📋 DATA SUMMARY')
        print('=' * 50)
        
        print(f"🔢 Total trips analyzed: {len(self.df):,}")
        print(f"📅 Date range: {self.df['Start Time'].min().date()} to {self.df['Start Time'].max().date()}")
        print(f"🏙️  City: {self.filters.city.title()}")
        print(f"📅 Month filter: {self.filters.month.title()}")
        print(f"📆 Day filter: {self.filters.day.title()}")
        print(f"💾 Memory usage: {self.df.memory_usage(deep=True).sum() / 1024**2:.1f} MB")
        
        print('-' * 50)
    
    def run_analysis(self) -> None:
        """Run the complete analysis workflow."""
        try:
            # Validate data files
            if not self.validate_data_files():
                print("❌ Cannot proceed without required data files.")
                return
            
            while True:
                # Get user preferences
                filters = self.get_user_filters()
                
                # Load and filter data
                df = self.load_and_filter_data(filters)
                
                if len(df) == 0:
                    continue
                
                # Run all analyses
                self.display_summary_stats()
                self.analyze_time_patterns()
                self.analyze_stations()
                self.analyze_trip_duration()
                self.analyze_user_demographics()
                self.analyze_usage_patterns()
                
                # Ask if user wants to continue
                print('\n' + '=' * 60)
                while True:
                    restart = input('\n🔄 Would you like to analyze different data? (yes/no): ').lower().strip()
                    if restart in ['yes', 'y', 'no', 'n']:
                        break
                    print("❌ Please enter 'yes' or 'no'")
                
                if restart in ['no', 'n']:
                    break
                    
        except KeyboardInterrupt:
            print("\n\n👋 Analysis interrupted. Goodbye!")
        except Exception as e:
            logger.error(f"Analysis error: {e}")
            print(f"❌ An error occurred: {e}")
        finally:
            print("\n🎉 Thank you for using the Advanced Bikeshare Analyzer!")


def main():
    """Main function to run the bikeshare analyzer."""
    analyzer = BikeShareAnalyzer()
    analyzer.run_analysis()


if __name__ == "__main__":
    main()