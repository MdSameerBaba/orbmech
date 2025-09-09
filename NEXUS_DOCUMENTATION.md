# 🚀 NEXUS AI Assistant - Complete Documentation

## 📋 Table of Contents
1. [System Overview](#system-overview)
2. [Installation & Setup](#installation--setup)
3. [Mode System](#mode-system)
4. [General Mode](#general-mode)
5. [Stock Mode](#stock-mode)
6. [DSA Mode](#dsa-mode)
7. [Project Mode](#project-mode)
8. [Voice & Text Interface](#voice--text-interface)
9. [File Management](#file-management)
10. [Troubleshooting](#troubleshooting)

---

## 🎯 System Overview

**Nexus** is a comprehensive AI assistant with specialized modes for different tasks:
- **Multi-Modal Interface**: Voice + Text interaction
- **Intelligent Mode Switching**: Dedicated contexts for different workflows
- **Real-Time Data Integration**: Live stock prices, coding progress, project tracking
- **Visual Analytics**: Charts and dashboards for all data
- **Background Monitoring**: Automatic reminders and notifications

### Core Features
- ✅ **4 Specialized Modes**: General, Stock, DSA, Project
- ✅ **Voice Recognition**: Speech-to-text with activation sounds
- ✅ **Real-Time APIs**: Yahoo Finance, LeetCode, CodeChef integration
- ✅ **Visual Dashboards**: Matplotlib charts for all analytics
- ✅ **Document Analysis**: PDF summarization and analysis
- ✅ **Image Generation**: AI-powered image creation
- ✅ **Automation**: System control and web automation

---

## 🛠️ Installation & Setup

### Prerequisites
```bash
pip install pygame requests beautifulsoup4 matplotlib pandas python-dotenv groq yfinance
```

### GitHub CLI Installation (for Git integration)
```bash
# Windows
winget install GitHub.cli

# macOS
brew install gh

# Linux
sudo apt install gh

# Verify installation
gh --version
gh auth login
```

### Environment Configuration
Create `.env` file in root directory:
```env
Username=YourName
Assistantname=Nexus
GroqAPIKey=your_groq_api_key_here
SENDER_EMAIL=your_email@gmail.com
SENDER_PASSWORD=your_app_password
GITHUB_USERNAME=your_github_username
GITHUB_TOKEN=your_github_personal_access_token
```

### Launch System
```bash
python Main.py
```

---

## 🔄 Mode System

### Mode Commands
| Command | Description | Example |
|---------|-------------|---------|
| `"general mode"` | Default AI assistant | General conversations, weather, jokes |
| `"stock mode"` | Portfolio & market analysis | Stock prices, portfolio tracking |
| `"dsa mode"` | Coding practice assistant | LeetCode progress, study guides |
| `"project mode"` | Project management | Task tracking, deadlines, progress |
| `"mode info"` | Show all available modes | Current mode status |

### Mode Switching Examples
```
User: "stock mode"
Nexus: "✅ Switched to STOCK mode! Stock market analysis and portfolio tracking"

User: "normal mode"  
Nexus: "✅ Switched to GENERAL mode! General AI assistant mode"
```

---

## 🤖 General Mode

### Core Capabilities
- **Conversations**: Natural language chat
- **Real-Time Search**: News, weather, current events
- **System Control**: Volume, applications, file operations
- **Content Creation**: Writing, coding, explanations
- **Web Automation**: Google search, YouTube search
- **Email**: Send emails with natural language

### Command Examples
```
# Conversations
"How are you today?"
"Tell me a joke"
"What's the weather like?"

# System Control
"open chrome"
"close notepad"
"volume up"
"mute system"

# Content Creation
"write a Python function to sort a list"
"explain quantum computing"
"create a business plan outline"

# Web & Email
"google search artificial intelligence"
"youtube search python tutorials"
"email john about the meeting tomorrow"
```

### Automation Features
- **Application Control**: Open/close any application
- **Web Navigation**: Automated browsing and searching
- **System Commands**: Volume, power, file operations
- **Email Integration**: Natural language email composition

---

## 📈 Stock Mode

### Features Overview
- **Real-Time Data**: Yahoo Finance integration (no API key required)
- **Portfolio Tracking**: Multiple stocks with purchase history
- **Visual Analytics**: 6-chart dashboard with comprehensive metrics
- **Time Period Analysis**: Weekly, monthly, quarterly, annual filtering
- **Smart Notifications**: Price alerts and portfolio updates

### Setup Process
1. **Switch to Stock Mode**: `"stock mode"`
2. **Configure Portfolio**: Edit `Data/portfolio.json`
3. **View Dashboard**: `"show my portfolio"`

### Portfolio Configuration
Edit `Data/portfolio.json`:
```json
{
  "holdings": [
    {
      "symbol": "AAPL",
      "shares": 10,
      "purchase_price": 150.00,
      "purchase_date": "2024-01-15"
    },
    {
      "symbol": "MSFT", 
      "shares": 5,
      "purchase_price": 380.00,
      "purchase_date": "2024-01-20"
    }
  ]
}
```

### Stock Mode Commands
| Command | Description | Example Output |
|---------|-------------|----------------|
| `"show my portfolio"` | Complete portfolio analysis | 6-chart dashboard with P&L |
| `"portfolio performance this month"` | Time-filtered analysis | Monthly gains/losses |
| `"AAPL stock price"` | Individual stock data | Current price + change |
| `"market summary"` | Overall market overview | Major indices performance |
| `"portfolio alerts"` | Price notifications | Significant price movements |

### Dashboard Charts
1. **Portfolio Overview**: Total value and daily change
2. **Asset Allocation**: Pie chart of holdings distribution  
3. **Individual Performance**: Bar chart of each stock's P&L
4. **Price History**: Line charts with moving averages
5. **Volume Analysis**: Trading volume patterns
6. **Correlation Matrix**: Stock relationship analysis

### Time Period Filtering
```
"show portfolio performance this week"
"monthly portfolio analysis" 
"quarterly stock performance"
"annual portfolio review"
```

---

## 🧠 DSA Mode

### Features Overview
- **Multi-Platform Tracking**: LeetCode, CodeChef, Codeforces, HackerRank
- **Real-Time Progress**: Live data fetching from platforms
- **Study Guides**: Curated resources with YouTube videos
- **Language Preferences**: Python, Java, C++, JavaScript support
- **Visual Analytics**: Progress charts and topic mastery

### Setup Process
1. **Switch to DSA Mode**: `"dsa mode"`
2. **Configure Usernames**: `"setup DSA"`
3. **Set Language**: `"set language to Python"`
4. **View Progress**: `"DSA summary"`

### Platform Setup
```
User: "setup DSA"
System: Enter your LeetCode username: sameerbaba2405
System: Enter your CodeChef username: sameerbaba2405  
System: Enter your Codeforces username: [skip]
System: Enter your HackerRank username: @sameerbaba2405
```

### DSA Mode Commands
| Command | Description | Features |
|---------|-------------|----------|
| `"DSA summary"` | Complete progress overview | Real-time stats + charts |
| `"arrays guide"` | Topic-specific study plan | YouTube videos + problems |
| `"show my progress"` | Visual dashboard | 4-panel analytics |
| `"set language to Java"` | Change programming language | Updates all guides |
| `"trees prep"` | Study guide for trees | Curated learning path |

### Study Guide Topics
- **Arrays & Two Pointers**: Sliding window, two-sum patterns
- **Strings**: Pattern matching, KMP algorithm
- **Trees**: Binary trees, BST operations, traversals
- **Dynamic Programming**: Memoization, tabulation, patterns
- **Graphs**: BFS, DFS, shortest paths, topological sort
- **Advanced**: Backtracking, greedy, binary search

### Study Guide Format
```
🎯 ARRAYS STUDY GUIDE
📺 RECOMMENDED YOUTUBE VIDEOS:
• Arrays Complete Course - Striver (2:30:00)
  🔗 https://www.youtube.com/watch?v=37E9ckMDdTk
• Two Pointer Technique - Love Babbar (45:00)
  🔗 https://www.youtube.com/watch?v=OnLoX6Nhvmg

💻 LEETCODE PROBLEMS:
• Two Sum (Easy)
  🔗 https://leetcode.com/problems/two-sum/
• Maximum Subarray (Medium)
  🔗 https://leetcode.com/problems/maximum-subarray/

🏆 CODECHEF PROBLEMS:
• LAPIN (Easy)
  🔗 https://www.codechef.com/problems/LAPIN
```

### Language Preferences
```
"set language to Python"    # Updates all guides to Python
"arrays guide in Java"      # One-time Java guide
"set language to C++"       # Permanent C++ preference
```

### Progress Analytics
- **Platform Breakdown**: Problems solved per platform
- **Topic Mastery**: Percentage completion by topic
- **Weekly Activity**: Daily problem-solving trends
- **Goals Tracking**: Daily/weekly/monthly targets

---

## 📊 Project Mode

### Features Overview
- **Project Creation**: Multiple project types with templates
- **Progress Tracking**: Visual dashboards and time logging
- **Deadline Management**: Automatic alerts and reminders
- **Work Session Logging**: Time tracking with descriptions
- **Background Monitoring**: Continuous deadline checking

### Setup Process
1. **Switch to Project Mode**: `"project mode"`
2. **Create Project**: `"create project"`
3. **Track Progress**: `"dashboard"`
4. **Log Work**: `"log 3 hours work on project 1"`

### Project Types & Templates
| Type | Description | Default Tasks |
|------|-------------|---------------|
| `software_development` | Coding projects | Planning → Design → Development → Testing → Deployment |
| `web_development` | Web applications | Planning → Frontend → Backend → Integration → Launch |
| `research_project` | Academic research | Research → Analysis → Writing → Review |
| `custom` | Any other project | User-defined tasks |

### Project Creation Examples
```
# Guided Creation
"create project"

# Full Command
"create project 'Mobile App' with description 'iOS shopping app' deadline 2024-03-15 type software_development"

# Quick Creation
"create project Website Redesign"
```

### Project Mode Commands
| Command | Description | Example |
|---------|-------------|---------|
| `"create project"` | Start new project | Guided setup process |
| `"dashboard"` | Visual progress charts | 4-panel analytics |
| `"project status"` | List all projects | Progress summary |
| `"log 3 hours work on project 1"` | Time tracking | Work session logging |
| `"update project 1 progress 75%"` | Progress update | Manual progress setting |
| `"setup github"` | Configure GitHub credentials | One-time authentication setup |
| `"set project path to C:\\MyProject"` | Link to local directory | Enables Git integration |
| `"git init"` | Initialize Git repository | Creates .git folder |
| `"create github repo"` | Create GitHub repository | Uses GitHub CLI |
| `"push to git"` | Push changes to GitHub | Commits and pushes |
| `"git status"` | Check Git status | Shows uncommitted changes |

### Dashboard Analytics
1. **Progress Bars**: Completion percentage per project
2. **Time Tracking**: Spent vs estimated hours
3. **Deadline Timeline**: Days remaining visualization
4. **Status Summary**: Alerts and project overview

### Work Logging Examples
```
"log 3 hours work on project 1"
"worked 2 hours on Mobile App debugging"
"log work: 4 hours frontend development"
```

### Git Integration Features
- **GitHub Authentication**: Secure token-based authentication
- **Repository Management**: Create and manage GitHub repositories
- **Automatic Commits**: Timestamped commits with progress updates
- **Exit Warnings**: Alerts for uncommitted changes when leaving project mode
- **Status Monitoring**: Real-time Git status checking

### Complete Git Workflow
```bash
# One-time GitHub setup
"setup github"          # Configure GitHub credentials

# Per project workflow
"project mode"          # Switch to project mode
"create project MyApp"  # Create new project
"set project path to C:\\MyApp"  # Link to local directory
"git init"             # Initialize Git repository
"create github repo"   # Create GitHub repository
"push to git"          # Push initial commit

# During development
"log 3 hours work on project 1"  # Track work time
"push to git"          # Push changes regularly
"git status"           # Check uncommitted changes

# When switching modes
"normal mode"          # System checks for uncommitted changes
```

### GitHub Setup Process
1. **Install GitHub CLI**: `winget install GitHub.cli`
2. **Authenticate**: `gh auth login`
3. **Configure in Nexus**: `"setup github"`
4. **Enter credentials**: GitHub username and Personal Access Token
5. **Create PAT**: https://github.com/settings/tokens (repo, workflow, write:packages)

### Exit Protection System
When leaving project mode, Nexus automatically:
- Scans all active projects for uncommitted changes
- Shows warning with project details
- Offers options: push changes, ignore, or cancel exit
- Prevents accidental loss of work

### Automatic Reminders
- **Daily Checks**: Every hour deadline monitoring
- **Alert Levels**: 🔴 1 day, 🟡 3 days, 🟠 7 days
- **Console Notifications**: Background reminder system
- **Progress Tracking**: Last activity timestamps

---

## 🎤 Voice & Text Interface

### Voice Activation
- **Microphone Button**: Click to activate voice input
- **Activation Sound**: Audio feedback when listening starts
- **Speech Recognition**: Converts speech to text commands
- **Voice Feedback**: Text-to-speech responses

### Text Interface
- **Chat Input**: Type commands directly
- **Command History**: Previous interactions saved
- **Rich Formatting**: HTML-styled chat display
- **Real-Time Updates**: Live status indicators

### Interface Features
- **Dual Input**: Voice OR text for all commands
- **Visual Feedback**: Status indicators and progress bars
- **Chat History**: Persistent conversation log
- **PDF Analysis**: Drag-and-drop document processing

---

## 📁 File Management

### Document Analysis
```
# PDF Processing
Drag PDF file to interface → Automatic summarization
"analyze this document" → AI-powered insights
"summarize the key points" → Structured summary
```

### Image Generation
```
"generate image of a sunset over mountains"
"create logo for tech startup"
"generate abstract art with blue colors"
```

### Data Storage Locations
```
📁 Data/
├── portfolio.json          # Stock holdings
├── portfolio_history.json  # Historical data
├── dsa_progress.json       # Coding progress
├── dsa_study_guides.json   # Learning resources
├── projects.json           # Project tracking
├── system_mode.json        # Current mode
├── Chatlog.json           # Conversation history
├── portfolio_analysis.png  # Stock charts
├── dsa_analysis.png        # DSA charts
└── project_dashboard.png   # Project charts
```

---

## 🔧 Troubleshooting

### Common Issues

#### 1. Voice Recognition Not Working
```bash
# Check WebDriver Service
✅ WebDriver Service is running.
❌ Could not start WebDriver, STT will not be available.

# Solution: Restart application
python Main.py
```

#### 2. API Integration Issues
```bash
# Groq API Error
❌ Failed to initialize Groq client

# Solution: Check .env file
GroqAPIKey=your_actual_api_key_here
```

#### 3. Stock Data Not Loading
```bash
# Yahoo Finance Error
❌ Error fetching stock data

# Solution: Check internet connection and stock symbols
```

#### 4. DSA Progress Not Updating
```bash
# Platform API Error
❌ Error fetching LeetCode stats

# Solution: Verify usernames in setup
"setup DSA" → Re-enter correct usernames
```

### Debug Mode
Enable detailed logging by checking console output:
```bash
Debug: mode=project, is_stock=False, is_dsa=False, is_project=True
📈 Calling ProjectAgent with query: 'dashboard'
```

### File Permissions
Ensure write permissions for Data/ directory:
```bash
# Windows
icacls Data /grant Users:F

# Check file creation
ls -la Data/
```

### Performance Optimization
- **Background Processes**: Project reminders run continuously
- **Memory Usage**: Charts generated on-demand
- **API Limits**: Reasonable request intervals
- **Cache Management**: Historical data stored locally

---

## 🎯 Quick Reference

### Essential Commands
```bash
# Mode Switching
"stock mode" | "dsa mode" | "project mode" | "normal mode"

# Stock Analysis  
"show my portfolio" | "AAPL stock price" | "portfolio performance this month"

# DSA Learning
"DSA summary" | "arrays guide" | "set language to Python" | "setup DSA"

# Project Management
"create project" | "dashboard" | "log 3 hours work on project 1" | "setup github"

# Git Integration
"git init" | "create github repo" | "push to git" | "git status"

# General Assistant
"what's the weather" | "open chrome" | "tell me a joke"
```

### File Locations
- **Main Application**: `Main.py`
- **Configuration**: `.env`
- **Data Storage**: `Data/` directory
- **Documentation**: `NEXUS_DOCUMENTATION.md`

### Support
For issues or feature requests:
1. Check console output for error messages
2. Verify .env configuration
3. Ensure all dependencies installed
4. Restart application if needed

---

**🚀 Nexus AI Assistant - Your Complete Productivity Companion**