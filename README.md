# 🌐 AI-Powered Network Scanner

A **fast, intelligent network scanning tool** that discovers devices on your network and provides AI-powered analysis using Groq API. Built with Python, Streamlit, and modern concurrency patterns.

**Perfect for:** Computer Networks coursework, internship portfolios, and portfolio projects.

---

## ⚡ What's New (v2.0)

✅ **Performance:** ThreadPoolExecutor for 10x faster scanning  
✅ **AI Upgrade:** Switched to Groq API (faster than Gemini)  
✅ **Modern UI:** Professional cards, charts, responsive layout  
✅ **Smart Features:** Auto-network detection, search, filters  
✅ **Settings:** Configurable timeout, threads, API keys  
✅ **Export:** CSV and JSON support  
✅ **Code Quality:** Better logging, validation, type hints  

---

## ✨ Features

### Core Scanning
- 🔍 **Fast Concurrent Scanning** using ThreadPoolExecutor
- 📊 **Device Detection** - Identify all active devices
- 🏠 **Hostname Resolution** - Reverse DNS lookup with timeout
- ⚡ **Response Time Tracking** - Measure ping latency
- 📈 **Progress Tracking** - Real-time progress bar
- 🎯 **Auto-Detection** - Automatically detect your local network

### Data Visualization
- 📊 **Status Pie Chart** - Online vs Offline distribution
- 📈 **Response Time Chart** - Device latency visualization
- 🎨 **Professional Dashboard** - Clean, organized statistics cards
- 📱 **Responsive Design** - Works on desktop and mobile

### Search & Filter
- 🔎 **Search** - Find devices by IP or hostname
- 🏷️ **Status Filter** - Show Online, Offline, or All
- 📋 **Sortable Table** - Interactive results display

### AI Analysis (Groq)
- 🤖 **Network Summary** - AI overview of your network
- 💡 **Smart Recommendations** - Security & performance suggestions
- ❤️ **Health Assessment** - Overall network status rating
- 🔍 **Pattern Recognition** - Device type identification

### Export & Integration
- 💾 **CSV Export** - For spreadsheets and reports
- 📄 **JSON Export** - For data processing
- 🔄 **Copy to Clipboard** - Easy data sharing

### Configuration
- ⚙️ **Scanner Settings** - Adjust timeout and thread count
- 🔑 **API Configuration** - Set Groq API key
- 🎨 **Theme Selection** - Light/Dark mode
- 📝 **Persistent Settings** - Configuration persists between sessions

---

## 🛠️ Technology Stack

| Component | Technology |
|-----------|-----------|
| **Backend** | Python 3.8+ |
| **Concurrency** | ThreadPoolExecutor |
| **Frontend** | Streamlit 1.28+ |
| **AI Engine** | Groq API (Mixtral 8x7B) |
| **Data Processing** | Pandas |
| **Visualization** | Plotly |
| **Networking** | Socket, Subprocess, IPAddress |

### Why These Choices?

- **ThreadPoolExecutor**: Simple, safe concurrent scanning (no race conditions)
- **Groq API**: Lightning-fast inference, perfect for real-time analysis
- **Streamlit**: Rapid development, professional-looking web UI
- **Plotly**: Interactive, publication-quality charts
- **Pandas**: Efficient data manipulation and export

---

## 📋 Requirements

- **Python:** 3.8 or higher
- **OS:** Windows, macOS, or Linux
- **Internet:** Required for Groq API
- **Permissions:** Admin/sudo for ICMP ping (some systems)
- **API Key:** Free Groq API key (get at https://console.groq.com)

---

## 🚀 Installation

### Step 1: Get the Code

```bash
# Clone repository
git clone https://github.com/sufyan-builds/AI-Network-Scanner.git
cd AI-Network-Scanner

# Or download and extract the ZIP file
```

### Step 2: Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure Groq API Key (Optional but Recommended)

**Option A: Using .env file (Recommended & Secure) ⭐**

1. **Copy the example file**:
   ```bash
   cp .env.example .env
   ```

2. **Get API key from** https://console.groq.com:
   - Sign up (free tier available)
   - Go to Settings → API Keys
   - Create new API key
   - Copy the key (looks like: `gsk_...`)

3. **Edit `.env` file** and add your key:
   ```
   GROQ_API_KEY=gsk_your_actual_key_here
   ```

4. **Security**:
   - `.env` is in `.gitignore` (won't commit to GitHub)
   - Never share `.env` file
   - Never commit `.env` to repositories

**Option B: Using Settings Tab (Session-only)**

1. Skip creating `.env` file
2. Run the app
3. Go to ⚙️ Settings tab
4. Paste API key
5. Key only works for current session

### Step 5: Run Application

```bash
streamlit run app.py
```

Opens automatically at `http://localhost:8501`

The app will automatically:
- ✅ Load API key from `.env` file (if exists)
- ✅ Fall back to Settings tab (if no .env)
- ✅ Work fine without API key (scanning only, no AI)

---

## 📖 How to Use

### Basic Scanning

1. **Open Dashboard**
   - Click "Dashboard" in sidebar
   - Or just refresh (defaults to Dashboard)

2. **Enter Network Range**
   - Example: `192.168.1.0/24`
   - Format: IPv4/prefix (CIDR notation)
   - Or click "Auto-Detect" button

3. **Start Scan**
   - Click "🚀 Start Scan" button
   - Watch progress bar (usually 1-3 minutes)
   - Results appear automatically when done

4. **Review Results**
   - **Statistics Cards**: Quick overview
   - **Charts**: Visual distribution
   - **Table**: Detailed device list
   - **AI Analysis**: Intelligent insights

5. **Export Data**
   - Click "📥 Download CSV" or "📥 Download JSON"
   - Save for reports or further analysis

### Common Network Ranges

| Network Type | Example | Note |
|--------------|---------|------|
| Home | 192.168.1.0/24 | Most common home network |
| Home Alt | 192.168.0.0/24 | Some routers use this |
| Office | 10.0.0.0/24 | Common enterprise range |
| Small | 172.16.0.0/25 | 126 possible hosts |

### Using Auto-Detect

```
1. Click "🔎 Auto-Detect" button
2. App scans your local IP
3. Automatically fills network range
4. You can manually edit if needed
5. Click "🚀 Start Scan" to begin
```

### Configuring Settings

#### API Key Setup
**Best Practice: Use `.env` file**
```
1. Copy .env.example to .env
2. Add your Groq API key
3. Restart the app
4. ✅ API key auto-loaded
```

**Alternative: Settings Tab (Session only)**
```
1. Go to ⚙️ Settings tab
2. Paste Groq API key
3. Click "🧪 Test API Key"
4. Key only valid for this session
```

#### Scanner Settings
1. **Click Settings tab**
2. **Adjust Scanner Settings:**
   - Timeout: How long to wait for each ping
   - Threads: More threads = faster but more CPU
3. **Choose Theme:**
   - Light or Dark mode
4. **Click "💾 Save Settings"**

**Note**: If API key is loaded from `.env`, Settings tab will show "✅ API key loaded from environment"

### Understanding Results

#### Statistics Cards
- **Total Scanned**: All IPs checked
- **Online**: Responding devices
- **Offline**: Not responding
- **Avg Response**: Average ping time

#### Status
- 🟢 **Online**: Device responded to ping
- 🔴 **Offline**: Device didn't respond

#### Response Time
- < 5ms: Same network segment (very fast)
- 5-50ms: Normal connection
- 50-200ms: Slower connection
- N/A: Device offline or error

#### Network Health
- 🟢 **Excellent**: Most devices online
- 🟢 **Good**: Healthy network
- 🟡 **Average**: Some issues
- 🔴 **Poor**: Many problems

---

## 🏗️ Project Structure

```
network-scanner/
│
├── app.py              # Main Streamlit application
│                       # Routes between Dashboard/Settings/About
│
├── scanner.py          # Network scanning engine
│                       # ThreadPoolExecutor-based concurrent scanning
│
├── ai.py              # Groq AI analysis
│                       # Generates insights and recommendations
│
├── ui.py              # Reusable UI components
│                       # Cards, charts, tables, inputs
│
├── utils.py           # Utility functions
│                       # Validation, formatting, export
│
├── requirements.txt   # Python dependencies
│
└── README.md          # This file
```

### File Descriptions

**app.py** (Main Application)
- Streamlit configuration and page routing
- Dashboard with scanning interface
- Settings configuration panel
- About and help information
- Session state management
- Progress tracking

**scanner.py** (Network Scanner)
- NetworkScanner class
- ThreadPoolExecutor-based concurrent pinging
- Hostname resolution with timeout
- Response time measurement
- Cross-platform support (Windows/Linux/macOS)
- ~150 lines, well-documented

**ai.py** (AI Analysis)
- GroqAnalyzer class
- Groq API integration (Mixtral 8x7B)
- Structured prompt generation
- Response parsing
- Error handling
- ~150 lines, easy to understand

**ui.py** (UI Components)
- Reusable Streamlit components
- Cards, metrics, charts
- Input components
- Search and filter UI
- Professional styling
- ~250 lines, modular

**utils.py** (Utilities)
- Network validation and parsing
- Input sanitization
- CSV/JSON export
- Statistics calculation
- Device classification
- ~250 lines, comprehensive

---

## 💡 Code Quality

### Best Practices Demonstrated

✅ **Modular Architecture**
- Separation of concerns
- Reusable components
- Single responsibility principle

✅ **Type Hints**
- Full type annotations
- Better IDE support
- Easier debugging

✅ **Comprehensive Documentation**
- Detailed docstrings
- Comments for complex logic
- README with examples

✅ **Error Handling**
- Graceful error handling
- User-friendly messages
- Logging for debugging

✅ **Performance**
- ThreadPoolExecutor for concurrency
- Timeout protection
- Efficient data structures

✅ **Security**
- No hardcoded secrets
- Input validation
- API key protection

---

## 🔐 Security & Privacy

### What This App Does
✅ Sends ICMP pings to IP addresses  
✅ Performs reverse DNS lookups  
✅ Analyzes results with AI  
✅ Stores results locally  

### What This App Does NOT Do
❌ Port scanning  
❌ Vulnerability testing  
❌ Packet inspection  
❌ Data exfiltration  
❌ Unauthorized access  

### Best Practices
- 🔒 **Never commit API keys** to repositories
- 🔒 **Keep API key confidential**
- 🔒 **Only scan networks you own** or have permission to scan
- 🔒 **Don't share scan results** publicly (may reveal network topology)
- 🔒 **Use environment variables** for sensitive data

---

## 🐛 Troubleshooting

### Scan is Very Slow

**Cause**: Default settings, large network, or network latency

**Solution**:
```
1. Try reducing network range (/25 instead of /24)
2. In Settings, reduce "Max Concurrent Threads"
3. Check your internet connection
4. Try scanning at a different time
```

### "Permission denied" Error

**Cause**: ICMP ping needs elevated privileges on some systems

**Solution**:
```bash
# macOS/Linux
sudo streamlit run app.py

# Windows: Run Command Prompt as Administrator
# Then run: streamlit run app.py
```

### No Hostnames Resolved (All "Unknown")

**Cause**: DNS resolution unavailable on network

**Solution**:
- This is normal and doesn't break scanning
- IP addresses are still correctly identified
- Functionality not affected

### AI Analysis Not Working

**Cause**: API key missing or invalid

**Solution**:
1. Go to Settings tab
2. Paste your Groq API key
3. Click "🧪 Test API Key"
4. Check https://console.groq.com for quota issues

### App Won't Start

**Cause**: Missing dependencies

**Solution**:
```bash
# Make sure virtual environment is activated
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Reinstall dependencies
pip install -r requirements.txt --upgrade
```

### "Invalid network range" Error

**Cause**: Wrong format

**Solution**:
- Use CIDR notation: `192.168.1.0/24`
- Don't use: `192.168.1.*` or `192.168.1.1-254`
- Check for typos

---

## 📊 Understanding Network Ranges

### CIDR Notation Explained

**192.168.1.0/24** means:
- `192.168.1.0` = network address
- `/24` = prefix length (first 24 bits are network)
- Covers: `192.168.1.0` to `192.168.1.255` (256 addresses)
- Usable hosts: `192.168.1.1` to `192.168.1.254` (254 devices)

### Common Prefix Lengths

| Prefix | Addresses | Usable Hosts | Typical Use |
|--------|-----------|--------------|------------|
| /32 | 1 | 1 | Single host |
| /30 | 4 | 2 | Point-to-point |
| /28 | 16 | 14 | Small office |
| /27 | 32 | 30 | Medium office |
| /26 | 64 | 62 | Office building |
| /25 | 128 | 126 | Large office |
| /24 | 256 | 254 | Standard subnet |
| /23 | 512 | 510 | Campus network |
| /22 | 1024 | 1022 | Large network |

---

## 📚 Learning Outcomes

By studying and using this project, you'll learn:

### Networking Fundamentals
- CIDR notation and IP addressing
- ICMP protocol and ping
- Reverse DNS lookups
- Network addressing schemes
- Subnetting concepts

### Python Programming
- Socket programming
- Subprocess management
- Exception handling
- List comprehensions
- Dictionary operations

### Concurrent Programming
- ThreadPoolExecutor usage
- Thread-safe operations
- Race condition prevention
- Progress tracking in threads
- Timeout handling

### API Integration
- REST API requests (Groq)
- API key management
- Prompt engineering
- Response parsing
- Error handling with APIs

### Web UI Development
- Streamlit framework
- Responsive layouts
- Form inputs
- Data visualization
- State management

### Data Science
- Pandas dataframes
- Data filtering and sorting
- CSV/JSON export
- Statistical calculations
- Data visualization with Plotly

### Software Engineering
- Modular code organization
- Type hints
- Docstring documentation
- Logging
- Configuration management
- Comments and readability

---

## 🚀 Deployment (Optional)

### Run on Your Machine

Already covered in "Installation" section above.

### Share with Friends

```bash
# They need to:
1. Install Python 3.8+
2. Download this repository
3. Run: pip install -r requirements.txt
4. Run: streamlit run app.py
5. Open http://localhost:8501 in browser
```

### Cloud Deployment (Advanced)

For production deployment, consider:
- **Streamlit Cloud**: Free tier available
- **Heroku**: Affordable hosting
- **AWS/Google Cloud**: For enterprise use

(Out of scope for this beginner project)

---

## 🎓 Portfolio Tips

### Interview Talking Points

When presenting this project in an interview, you can discuss:

1. **Performance Optimization**
   - "I used ThreadPoolExecutor instead of basic threading for better resource management and cleaner code"
   - "Implemented timeout handling to prevent hanging on DNS lookups"

2. **Modern APIs**
   - "Integrated Groq API for real-time AI analysis"
   - "Chose Groq for speed and efficiency compared to alternatives"

3. **User Experience**
   - "Designed a professional Streamlit UI with charts and filters"
   - "Added auto-detection and search features for better UX"

4. **Code Quality**
   - "Followed Python best practices: type hints, docstrings, logging"
   - "Separated concerns into modular components"

5. **Problem Solving**
   - "Identified and fixed performance bottlenecks in concurrent scanning"
   - "Handled cross-platform differences (Windows vs Linux/Mac ping)"

### What Makes This Portfolio-Worthy

✅ **Practical**: Solves real network discovery problem  
✅ **Complete**: Fully functional, ready to use  
✅ **Professional**: Clean code, documentation, UI  
✅ **Educational**: Demonstrates multiple skills  
✅ **Scalable**: Can be enhanced (database, scheduling, etc.)  
✅ **Portable**: No external services required (except API)  

---

## 🔄 Future Enhancements

### Level 1 (Easy)
- [ ] Add device MAC address detection
- [ ] Save scan history (JSON file)
- [ ] Show online/offline trends
- [ ] Device grouping/tagging
- [ ] Scan scheduling (weekly, daily)

### Level 2 (Medium)
- [ ] SQLite database for history
- [ ] Report generation (PDF)
- [ ] Email notifications
- [ ] Network topology visualization
- [ ] Multiple network profiles

### Level 3 (Advanced)
- [ ] Port scanning (nmap integration)
- [ ] Service detection
- [ ] Vulnerability scanning
- [ ] Wake-on-LAN support
- [ ] SNMP device info collection
- [ ] Network traffic analysis

---

## 📝 Notes

### Version History

**v2.0** (Current)
- Refactored with ThreadPoolExecutor
- Switched to Groq API
- Modern UI redesign
- Added settings panel
- Search and filter features
- JSON export support
- Improved documentation

**v1.0** (Original)
- Initial release
- Basic Gemini AI integration
- Simple Streamlit UI
- CSV export only

### Known Limitations

- IPv4 only (IPv6 support could be added)
- Simple ping-based detection (not port scanning)
- No persistent storage (data stored in session)
- Requires internet for Groq API

### Contributing

Suggestions and improvements welcome:
- Better error messages
- Performance optimizations
- UI/UX enhancements
- Additional export formats
- Documentation improvements

---

## 📄 License

Open source for educational and personal use.

---

## ❓ FAQ

**Q: Can I scan any network?**
A: Only networks you own or have explicit permission to scan. Unauthorized scanning may have legal consequences.

**Q: Is my Groq API key safe?**
A: Keep it private! Never commit to GitHub or share publicly. Use environment variables for production.

**Q: How accurate is device detection?**
A: Very accurate. Ping is reliable for detecting online devices. Offline detection is also accurate (no false positives).

**Q: What about IPv6 networks?**
A: Current version is IPv4 only. IPv6 support could be added in future.

**Q: Can I run this on a server?**
A: Yes, but you'd need to run Streamlit in headless mode. Consider deploying on Streamlit Cloud instead.

**Q: Do I need the Groq API key?**
A: No, scanning works without it. AI analysis just won't be available.

**Q: How long does scanning take?**
A: Typically 1-3 minutes depending on network size and device responsiveness.

**Q: Will this work with corporate firewalls?**
A: Probably not. Corporate networks often block ICMP. This tool works best on home/office networks.

---

## 📞 Support

For issues or questions:

1. **Check Troubleshooting** section above
2. **Review error messages** carefully
3. **Check project structure** and file layout
4. **Verify dependencies**: `pip list | grep streamlit`
5. **Re-install if needed**: `pip install -r requirements.txt --upgrade`

---

## 🌟 Thank You

This project is ready for:
- ✅ Personal learning
- ✅ Portfolio submission
- ✅ Internship applications
- ✅ Code interviews
- ✅ Computer networking coursework
- ✅ Friends and colleagues to use

---

**Happy Scanning! 🚀**

Last Updated: 2024  
Version: 2.0.0  
Status: Production Ready ✅

---

## Quick Command Reference

```bash
# Install dependencies
pip install -r requirements.txt

# Run application
streamlit run app.py

# Run with admin (if needed)
sudo streamlit run app.py  # macOS/Linux

# Set API key (bash)
export GROQ_API_KEY="your-key-here"

# Set API key (Windows PowerShell)
$env:GROQ_API_KEY="your-key-here"

# Deactivate virtual environment
deactivate
```
