# 🌐 SWSC - Startjobs Websites Status Checker

A modern, real-time website monitoring dashboard built with Streamlit. Monitor multiple websites simultaneously and get instant visual feedback with a beautiful, responsive interface.

![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-v1.28+-red.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## ✨ Features

### 🎯 Core Features
- **Real-time Monitoring**: Check multiple websites simultaneously with concurrent processing
- **Modern UI**: Beautiful, responsive dashboard with gradient styling and hover effects
- **Clickable URLs**: Website URLs in results are clickable links that open in new tabs
- **Export Reports**: Generate JSON reports with detailed statistics and timestamps
- **Auto-refresh**: Optional automatic status updates at configurable intervals

### 🚀 Advanced Features
- **Concurrent Checking**: Multi-threaded website monitoring for faster results
- **Response Time Tracking**: Monitor website performance and response times
- **Status Code Analysis**: Detailed HTTP status code reporting
- **Error Categorization**: Distinguish between timeouts, connection errors, and HTTP errors
- **Configuration Management**: Adjustable timeouts and concurrency settings

### 📊 Dashboard Components
- **Summary Statistics**: Overview of online/offline/warning sites
- **Detailed Status Cards**: Individual website status with response times and clickable URLs
- **Progress Indicators**: Real-time progress during monitoring
- **Management Panel**: Easy website addition/removal interface

## 🛠️ Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Quick Start

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd swsc
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the dashboard**
   ```bash
   streamlit run main.py
   ```

4. **Access the application**
   Open your browser and navigate to `http://localhost:8501`

## 📖 Usage Guide

### 🎛️ Dashboard Usage

#### Managing Websites
1. **Add Websites**: Use the left panel to add URLs (one per line)
2. **Save Changes**: Click "💾 Save Changes" to persist your website list
3. **Reset to Default**: Use "🔄 Reset to Default" to restore original websites

#### Monitoring Websites
1. **Configure Settings**: Use the sidebar to adjust timeout and concurrency
2. **Start Monitoring**: Click "🚀 Start Check" to begin status checks
3. **View Results**: See real-time status updates with response times and clickable URLs
4. **Export Reports**: Generate JSON reports with detailed analytics

#### Auto-refresh Mode
1. **Enable Auto-refresh**: Check the "Auto Refresh" option in the sidebar
2. **Set Interval**: Configure refresh interval (10-300 seconds)
3. **Monitor Continuously**: Dashboard will update automatically

## 🔧 Configuration

### 📁 File Structure
```
swsc/
├── main.py              # Main Streamlit dashboard (all-in-one application)
├── requirements.txt     # Python dependencies
├── websites.json        # Website list (auto-generated)
└── README.md           # This file
```

### ⚙️ Configuration Options

#### Dashboard Settings
- **Request Timeout**: 5-30 seconds (default: 10)
- **Concurrent Checks**: 1-10 simultaneous checks (default: 5)
- **Auto-refresh Interval**: 10-300 seconds (default: 30)

### 📄 Website Configuration

#### Format Requirements
- URLs must include protocol (`http://` or `https://`)
- One URL per line in the dashboard
- JSON format in `websites.json` file

#### Example `websites.json`
```json
[
  "https://example.com",
  "https://google.com",
  "https://github.com",
  "https://stackoverflow.com"
]
```

## 🧪 Development

### 🛠️ Setting up Development Environment

1. **Clone and setup**
   ```bash
   git clone <repository-url>
   cd swsc
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Install development dependencies**
   ```bash
   pip install pytest black flake8
   ```

3. **Run tests**
   ```bash
   pytest
   ```

4. **Format code**
   ```bash
   black *.py
   flake8 *.py
   ```

### 🏗️ Architecture Overview

#### Core Components
- **WebsiteManager**: Handles website data persistence and validation
- **WebsiteStatus**: Dataclass for website status information
- **Concurrent Processing**: ThreadPoolExecutor for parallel website checks
- **Modern UI Components**: Streamlit-based dashboard with custom CSS

#### Key Design Patterns
- **All-in-One Architecture**: Single file application for simplicity
- **Dataclass Usage**: Type-safe configuration and status objects
- **Concurrent Processing**: ThreadPoolExecutor for parallel website checks
- **Error Handling**: Comprehensive exception handling
- **Modern UI**: Custom CSS with gradient styling and hover effects

## 📊 Monitoring Reports

### 📈 Report Format
Reports are generated in JSON format with the following structure:

```json
{
  "timestamp": "2025-09-04T10:30:00.123456",
  "summary": {
    "total_sites": 10,
    "online": 8,
    "warnings": 1,
    "offline": 1
  },
  "details": {
    "https://example.com": {
      "status": "🟢 Online",
      "response_time": 142.5,
      "status_code": 200
    },
    "https://startjobs.ma": {
      "status": "🟢 Online", 
      "response_time": 89.3,
      "status_code": 200
    }
  }
}
```

### 📋 Available Metrics
- **Response Time**: Milliseconds to complete request
- **Status Codes**: HTTP response codes (200, 404, 500, etc.)
- **Error Categories**: Timeout, Connection Error, HTTP Error
- **Timestamp Data**: Precise monitoring timestamps
- **Success Rates**: Online/offline ratios
- **Visual Status**: Color-coded status indicators (🟢 Online, 🟡 Warning, 🔴 Offline)

## 🚨 Troubleshooting

### Common Issues

#### Dashboard Won't Start
```bash
# Check Python version
python --version  # Should be 3.8+

# Reinstall dependencies
pip install --upgrade -r requirements.txt

# Check port availability
netstat -tulpn | grep :8501
```

#### Websites Not Loading
1. **Check URL Format**
   - Must include `http://` or `https://`
   - Verify URLs are accessible from your network

2. **Adjust Timeout Settings**
   - Increase timeout in dashboard sidebar
   - Check for slow network connections

3. **Check Browser Console**
   - Look for JavaScript errors
   - Verify Streamlit is running properly

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/karkouri-zakaria/swsc/issues)
- **Discussions**: [GitHub Discussions](https://github.com/karkouri-zakaria/swsc/discussions)
- **Email**: zakaria.karkouri@outlook.com

---

<div align="center">
  <p>⭐ Star this repository if you find it helpful!</p>
  <p>🚀 SWSC - Startjobs Websites Status Checker</p>
</div>