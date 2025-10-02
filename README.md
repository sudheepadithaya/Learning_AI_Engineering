# 🚴 Interactive Bikeshare Data Explorer

A comprehensive, interactive web application for exploring and analyzing bikeshare data with advanced visualizations, filtering capabilities, and statistical insights.

## ✨ Features

### 🎯 Core Functionality
- **Interactive Data Exploration**: Filter by city, month, day, and hour
- **Advanced Analytics**: Statistical insights and trend analysis
- **Beautiful Visualizations**: Interactive charts, graphs, and heatmaps
- **Station Analysis**: Popular stations and route mapping
- **User Demographics**: Age, gender, and user type analysis
- **Data Export**: Download filtered data and statistics

### 📊 Visualizations
- Time pattern heatmaps
- Station popularity charts
- Trip duration distributions
- Demographic pie charts
- Interactive city maps
- Usage trend analyses

### 🔧 Technical Features
- Object-oriented design with type hints
- Efficient data processing with pandas
- Responsive web interface with Streamlit
- Interactive plots with Plotly
- Geographic visualization with Folium
- Data caching for improved performance

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone or download the project files** to your local machine

2. **Navigate to the project directory**:
   ```bash
   cd /path/to/bikeshare-explorer
   ```

3. **Create a virtual environment** (recommended):
   ```bash
   python -m venv bikeshare_env
   
   # On macOS/Linux:
   source bikeshare_env/bin/activate
   
   # On Windows:
   bikeshare_env\Scripts\activate
   ```

4. **Install required packages**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Ensure you have the data files**:
   - `chicago.csv`
   - `new_york_city.csv`
   - `washington.csv`
   
   Place these files in the same directory as the application files.

### Running the Applications

#### 🌐 Web Application (Recommended)
```bash
streamlit run bikeshare_webapp.py
```
Then open your browser to `http://localhost:8501`

#### 💻 Command Line Application
```bash
python bikeshare_analyzer.py
```

## 📁 Project Structure

```
bikeshare-explorer/
├── bikeshare_webapp.py       # Interactive web application
├── bikeshare_analyzer.py     # Enhanced command-line version
├── bikeshare_2.py           # Original script (for reference)
├── requirements.txt         # Python dependencies
├── README.md               # This file
├── chicago.csv             # Chicago bikeshare data
├── new_york_city.csv       # NYC bikeshare data
└── washington.csv          # Washington DC bikeshare data
```

## 🎮 How to Use

### Web Application
1. **Launch** the web app using `streamlit run bikeshare_webapp.py`
2. **Select filters** in the sidebar:
   - Choose city (Chicago, New York City, Washington)
   - Filter by month (January-June or All)
   - Filter by day of week (or All)
   - Set hour range (0-23)
3. **Explore tabs**:
   - **Time Analysis**: Hourly/daily patterns and heatmaps
   - **Stations & Routes**: Popular stations and trip routes
   - **Demographics**: User type, gender, and age analysis
   - **Advanced Analytics**: Duration analysis and trends
   - **Map View**: Interactive city map
   - **Data Export**: Download filtered data

### Command Line Application
1. **Run** `python bikeshare_analyzer.py`
2. **Follow prompts** to select:
   - City to analyze
   - Month filter (or 'all')
   - Day filter (or 'all')
3. **View results** with enhanced formatting and emojis
4. **Choose** to restart with different filters

## 📊 Sample Insights

The application provides insights such as:
- **Peak Usage Hours**: Typically 8 AM and 5-6 PM (commuter patterns)
- **Popular Stations**: High-traffic areas and business districts
- **User Demographics**: Subscriber vs. customer ratios, age distributions
- **Seasonal Trends**: Monthly usage variations
- **Trip Patterns**: Average duration, route popularity
- **Weekend vs. Weekday**: Usage pattern differences

## 🔧 Customization

### Adding New Cities
1. Add new city data file (CSV format)
2. Update `CITY_DATA` dictionary in both applications
3. Add city coordinates to `CITY_COORDS` (for web app maps)

### Modifying Visualizations
- Charts are created using Plotly - easy to customize colors, layout
- Add new chart types by extending the respective methods
- Modify filtering options in the sidebar creation method

### Performance Optimization
- Data is cached using Streamlit's `@st.cache_data` decorator
- Large datasets are automatically optimized with efficient data types
- Consider data preprocessing for very large files

## 🐛 Troubleshooting

### Common Issues

1. **Import Errors**
   ```bash
   # Ensure all packages are installed
   pip install -r requirements.txt
   ```

2. **Data File Not Found**
   - Verify CSV files are in the same directory
   - Check file names match exactly (case-sensitive)

3. **Web App Won't Start**
   ```bash
   # Try upgrading Streamlit
   pip install --upgrade streamlit
   
   # Or run with explicit Python version
   python -m streamlit run bikeshare_webapp.py
   ```

4. **Slow Performance**
   - Use data filtering to reduce dataset size
   - Close other browser tabs
   - Consider using a smaller date range

5. **Visualization Issues**
   - Clear browser cache
   - Try a different browser
   - Ensure Plotly is properly installed

## 💡 Tips for Best Experience

1. **Start with broad filters** then narrow down for specific insights
2. **Use the hour range slider** to focus on specific time periods
3. **Compare different cities** by switching between them
4. **Download data** for offline analysis or reporting
5. **Try different combinations** of filters for unique insights

## 🚀 Deployment Options

### Local Development
- Run directly with `streamlit run bikeshare_webapp.py`
- Perfect for personal analysis and exploration

### Cloud Deployment
- **Streamlit Cloud**: Push to GitHub and deploy via share.streamlit.io
- **Heroku**: Create `Procfile` and deploy as web app
- **AWS/GCP**: Deploy using container services
- **Docker**: Create containerized version for consistent deployment

### Docker Deployment (Optional)
Create a `Dockerfile`:
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8501

CMD ["streamlit", "run", "bikeshare_webapp.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

## 🤝 Contributing

Feel free to enhance this project by:
- Adding more visualization types
- Implementing additional analytical features
- Improving the user interface
- Adding support for more data formats
- Creating automated testing

## 📄 License

This project is open source and available under the MIT License.

## 📞 Support

If you encounter any issues or have questions:
1. Check the troubleshooting section above
2. Verify all requirements are installed correctly
3. Ensure data files are in the correct location
4. Try running the command-line version first to isolate issues

---

## 🎉 Enjoy Exploring!

This enhanced bikeshare analyzer transforms simple data exploration into an engaging, visual experience. Whether you're a data scientist, urban planner, or just curious about transportation patterns, this tool provides comprehensive insights into bikeshare usage patterns.

**Happy analyzing!** 🚴‍♀️🚴‍♂️