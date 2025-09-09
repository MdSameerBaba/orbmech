# In Backend/Agents/PortfolioAnalytics.py

import json
import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime, timedelta
from dotenv import dotenv_values

# --- CONFIGURATION ---
env_vars = dotenv_values(".env")
Username = env_vars.get("Username")

PORTFOLIO_FILE = r"Data\portfolio.json"
HISTORY_FILE = r"Data\portfolio_history.json"

def load_portfolio_history():
    try:
        with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"daily_snapshots": [], "transactions": []}

def save_portfolio_history(history):
    try:
        with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
            json.dump(history, f, indent=2)
    except IOError as e:
        print(f"❌ Error saving history: {e}")

def update_daily_snapshot():
    """Update today's portfolio snapshot"""
    from Backend.Agents.StockAgent import analyze_portfolio
    
    today = datetime.now().strftime("%Y-%m-%d")
    history = load_portfolio_history()
    
    # Check if today's snapshot already exists
    existing_dates = [snap["date"] for snap in history["daily_snapshots"]]
    if today in existing_dates:
        return
    
    # Get current portfolio analysis
    portfolio_data = analyze_portfolio()
    
    snapshot = {
        "date": today,
        "total_value": portfolio_data["total_portfolio_value"],
        "cash": portfolio_data["cash"],
        "holdings": {}
    }
    
    for holding in portfolio_data["holdings_analysis"]:
        snapshot["holdings"][holding["symbol"]] = {
            "shares": holding["shares"],
            "price": holding["current_price"],
            "value": holding["current_value"]
        }
    
    history["daily_snapshots"].append(snapshot)
    save_portfolio_history(history)
    print(f"📊 Updated portfolio snapshot for {today}")

def calculate_portfolio_growth():
    """Calculate growth metrics"""
    history = load_portfolio_history()
    snapshots = history["daily_snapshots"]
    
    if len(snapshots) < 2:
        return {"error": "Need at least 2 days of data for growth calculation"}
    
    first_value = snapshots[0]["total_value"]
    latest_value = snapshots[-1]["total_value"]
    
    total_growth = ((latest_value - first_value) / first_value) * 100
    
    # Daily growth rates
    daily_growth = []
    for i in range(1, len(snapshots)):
        prev_val = snapshots[i-1]["total_value"]
        curr_val = snapshots[i]["total_value"]
        growth = ((curr_val - prev_val) / prev_val) * 100
        daily_growth.append({
            "date": snapshots[i]["date"],
            "growth": growth,
            "value": curr_val
        })
    
    return {
        "total_growth": total_growth,
        "first_value": first_value,
        "latest_value": latest_value,
        "daily_growth": daily_growth,
        "days_tracked": len(snapshots)
    }

def generate_portfolio_charts():
    """Generate comprehensive portfolio charts"""
    history = load_portfolio_history()
    snapshots = history["daily_snapshots"]
    
    if len(snapshots) < 2:
        return "Need more historical data for charts"
    
    # Create figure with 6 subplots (2x3 grid)
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    fig.suptitle(f"{Username}'s Portfolio Analysis Dashboard", fontsize=20, fontweight='bold')
    
    # Flatten axes for easier indexing
    axes = axes.flatten()
    
    # 1. Portfolio Value with Moving Averages
    ax1 = axes[0]
    dates = [snap["date"] for snap in snapshots]
    values = [snap["total_value"] for snap in snapshots]
    
    ax1.plot(dates, values, marker='o', linewidth=2, markersize=4, color='#2E8B57', label='Portfolio Value')
    
    # Add moving averages if enough data
    if len(values) >= 7:
        ma7 = pd.Series(values).rolling(window=min(7, len(values))).mean()
        ax1.plot(dates, ma7, '--', color='orange', alpha=0.8, label='7-day MA')
    if len(values) >= 30:
        ma30 = pd.Series(values).rolling(window=min(30, len(values))).mean()
        ax1.plot(dates, ma30, '--', color='red', alpha=0.8, label='30-day MA')
    
    ax1.set_title('Portfolio Value & Moving Averages', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Value ($)')
    ax1.grid(True, alpha=0.3)
    ax1.legend()
    ax1.tick_params(axis='x', rotation=45)
    
    # 2. Daily Growth Rate
    ax2 = axes[1]
    growth_data = calculate_portfolio_growth()
    if "daily_growth" in growth_data:
        growth_dates = [d["date"] for d in growth_data["daily_growth"]]
        growth_values = [d["growth"] for d in growth_data["daily_growth"]]
        
        colors = ['#2E8B57' if x >= 0 else '#DC143C' for x in growth_values]
        ax2.bar(growth_dates, growth_values, color=colors, alpha=0.7)
        ax2.set_title('Daily Growth Rate (%)', fontsize=12, fontweight='bold')
        ax2.set_ylabel('Growth (%)')
        ax2.axhline(y=0, color='black', linestyle='-', alpha=0.3)
        ax2.tick_params(axis='x', rotation=45)
    
    # 3. Asset Allocation Pie Chart
    ax3 = axes[2]
    latest_snapshot = snapshots[-1]
    holdings = latest_snapshot["holdings"]
    
    if holdings:
        symbols = list(holdings.keys())
        values = [holdings[symbol]["value"] for symbol in symbols]
        colors = plt.cm.Set3(range(len(symbols)))
        
        wedges, texts, autotexts = ax3.pie(values, labels=symbols, autopct='%1.1f%%', 
                                          colors=colors, startangle=90)
        ax3.set_title('Asset Allocation', fontsize=12, fontweight='bold')
        
        # Add value labels
        for i, (symbol, value) in enumerate(zip(symbols, values)):
            autotexts[i].set_text(f'{symbol}\n{value/sum(values)*100:.1f}%\n${value:.0f}')
            autotexts[i].set_fontsize(8)
    
    # 4. Individual Stock Performance
    ax4 = axes[3]
    stock_history = {}
    
    # Collect individual stock data
    for snapshot in snapshots:
        date = snapshot["date"]
        for symbol, data in snapshot["holdings"].items():
            if symbol not in stock_history:
                stock_history[symbol] = {"dates": [], "prices": []}
            stock_history[symbol]["dates"].append(date)
            stock_history[symbol]["prices"].append(data["price"])
    
    # Plot each stock
    colors = ['#2E8B57', '#4169E1', '#DC143C', '#FF8C00', '#9932CC']
    for i, (symbol, data) in enumerate(stock_history.items()):
        color = colors[i % len(colors)]
        ax4.plot(data["dates"], data["prices"], marker='o', linewidth=2, 
                markersize=3, label=symbol, color=color)
    
    ax4.set_title('Individual Stock Performance', fontsize=12, fontweight='bold')
    ax4.set_ylabel('Stock Price ($)')
    ax4.legend()
    ax4.grid(True, alpha=0.3)
    ax4.tick_params(axis='x', rotation=45)
    
    # 5. Portfolio Composition (Cash vs Stocks)
    ax5 = axes[4]
    cash = latest_snapshot["cash"]
    total_stocks = sum(holdings[symbol]["value"] for symbol in holdings)
    
    composition_labels = ['Cash', 'Stocks']
    composition_values = [cash, total_stocks]
    composition_colors = ['#FFD700', '#2E8B57']
    
    ax5.pie(composition_values, labels=composition_labels, autopct='%1.1f%%',
           colors=composition_colors, startangle=90)
    ax5.set_title('Cash vs Stocks', fontsize=12, fontweight='bold')
    
    # 6. Performance Summary (Text)
    ax6 = axes[5]
    ax6.axis('off')
    
    # Calculate summary stats
    total_return = ((values[-1] - values[0]) / values[0]) * 100
    best_day = max(growth_data["daily_growth"], key=lambda x: x["growth"]) if "daily_growth" in growth_data else None
    worst_day = min(growth_data["daily_growth"], key=lambda x: x["growth"]) if "daily_growth" in growth_data else None
    
    summary_text = f"""PERFORMANCE SUMMARY
    
📊 Total Return: {total_return:+.2f}%
💰 Current Value: ${values[-1]:,.2f}
📈 Initial Value: ${values[0]:,.2f}
📅 Days Tracked: {len(snapshots)}
"""
    
    if best_day:
        summary_text += f"\n🟢 Best Day: {best_day['growth']:+.2f}%\n   ({best_day['date']})"
    if worst_day:
        summary_text += f"\n🔴 Worst Day: {worst_day['growth']:+.2f}%\n   ({worst_day['date']})"
    
    ax6.text(0.1, 0.9, summary_text, transform=ax6.transAxes, fontsize=11,
            verticalalignment='top', bbox=dict(boxstyle='round', facecolor='lightgray', alpha=0.8))
    
    plt.tight_layout()
    
    # Save chart
    chart_path = r"Data\portfolio_analysis.png"
    plt.savefig(chart_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    return chart_path

def filter_data_by_period(snapshots, period):
    """Filter snapshots by time period"""
    if not snapshots:
        return snapshots
    
    today = datetime.now()
    
    if period == "weekly":
        cutoff_date = today - timedelta(days=7)
    elif period == "monthly":
        cutoff_date = today - timedelta(days=30)
    elif period == "quarterly":
        cutoff_date = today - timedelta(days=90)
    elif period == "annually":
        cutoff_date = today - timedelta(days=365)
    else:
        return snapshots  # Return all data for full history
    
    cutoff_str = cutoff_date.strftime("%Y-%m-%d")
    filtered = [snap for snap in snapshots if snap["date"] >= cutoff_str]
    
    return filtered if filtered else snapshots[-1:]  # At least return latest snapshot

def summarize_portfolio(time_period=None):
    """Main function to summarize portfolio with analytics"""
    print("📊 Updating portfolio snapshot...")
    update_daily_snapshot()
    
    # Load and filter data based on time period
    history = load_portfolio_history()
    all_snapshots = history["daily_snapshots"]
    
    if time_period:
        filtered_snapshots = filter_data_by_period(all_snapshots, time_period)
        print(f"📅 Analyzing {time_period} data: {len(filtered_snapshots)} days")
    else:
        filtered_snapshots = all_snapshots
        print(f"📅 Analyzing full history: {len(filtered_snapshots)} days")
    
    if len(filtered_snapshots) < 2:
        return f"Need at least 2 days of data for {time_period or 'full'} analysis. Current data: {len(filtered_snapshots)} days."
    
    # Calculate growth for the filtered period
    first_value = filtered_snapshots[0]["total_value"]
    latest_value = filtered_snapshots[-1]["total_value"]
    period_growth = ((latest_value - first_value) / first_value) * 100
    
    print("📈 Calculating growth metrics...")
    print("📊 Generating charts...")
    
    # Temporarily update history with filtered data for chart generation
    original_snapshots = history["daily_snapshots"]
    history["daily_snapshots"] = filtered_snapshots
    save_portfolio_history(history)
    
    chart_path = generate_portfolio_charts()
    
    # Restore original data
    history["daily_snapshots"] = original_snapshots
    save_portfolio_history(history)
    
    # Create period-specific summary
    period_name = time_period.upper() if time_period else "FULL HISTORY"
    
    summary = f"""
📊 {period_name} PORTFOLIO SUMMARY for {Username}

💰 Current Value: ${latest_value:,.2f}
🚀 {period_name.title()} Growth: {period_growth:+.2f}%
📅 Period Analyzed: {len(filtered_snapshots)} days
💵 Period Start Value: ${first_value:,.2f}
📈 Value Change: ${latest_value - first_value:+,.2f}

📈 {period_name.title()} charts saved to: {chart_path}
"""
    
    return summary

# --- TESTING ---
if __name__ == "__main__":
    result = summarize_portfolio()
    print(result)