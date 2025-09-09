# In Backend/Agents/StockAgent.py

# --- IMPORTS ---
import json
import yfinance as yf
from datetime import datetime
from dotenv import dotenv_values
from groq import Groq

# --- CONFIGURATION (Following your exact pattern) ---
env_vars = dotenv_values(".env")
GroqAPIKey = env_vars.get("GroqAPIKey")
Username = env_vars.get("Username")

# --- API CLIENT INITIALIZATION (Your pattern) ---
try:
    client = Groq(api_key=GroqAPIKey)
except Exception as e:
    print(f"❌ Failed to initialize Groq client in StockAgent: {e}")
    client = None

# --- CONSTANTS ---
PORTFOLIO_FILE = r"Data\portfolio.json"

# --- HELPER FUNCTIONS ---
def load_portfolio():
    try:
        with open(PORTFOLIO_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"holdings": {}, "cash": 10000.0, "total_invested": 0.0}

def save_portfolio(portfolio):
    try:
        with open(PORTFOLIO_FILE, 'w', encoding='utf-8') as f:
            json.dump(portfolio, f, indent=4)
    except IOError as e:
        print(f"❌ Error saving portfolio: {e}")

def get_stock_price(symbol: str):
    try:
        stock = yf.Ticker(symbol)
        info = stock.info
        current_price = info.get('currentPrice') or info.get('regularMarketPrice')
        if current_price:
            print(f"✅ Got {symbol} price: ${current_price:.2f}")
            return current_price
        else:
            print(f"❌ Could not get price for {symbol}")
            return None
    except Exception as e:
        print(f"❌ Error in get_stock_price: {e}")
        return None

# --- CORE STOCK AGENT FUNCTIONS ---
def analyze_portfolio():
    portfolio = load_portfolio()
    total_value = portfolio["cash"]
    analysis = []
    
    for symbol, holding in portfolio["holdings"].items():
        current_price = get_stock_price(symbol)
        if current_price:
            current_value = holding["shares"] * current_price
            total_value += current_value
            gain_loss = current_value - holding["invested"]
            gain_loss_pct = (gain_loss / holding["invested"]) * 100 if holding["invested"] > 0 else 0
            
            analysis.append({
                "symbol": symbol,
                "shares": holding["shares"],
                "current_price": current_price,
                "invested": holding["invested"],
                "current_value": current_value,
                "gain_loss": gain_loss,
                "gain_loss_pct": gain_loss_pct
            })
    
    return {
        "total_portfolio_value": total_value,
        "cash": portfolio["cash"],
        "holdings_analysis": analysis
    }

def get_individual_stock_info(query: str):
    """Extract stock symbol from query and get current price"""
    # Simple symbol extraction
    symbols = ["AAPL", "MSFT", "GOOGL", "TSLA", "AMZN", "NVDA", "META"]
    query_upper = query.upper()
    
    for symbol in symbols:
        if symbol in query_upper or symbol.replace("AAPL", "APPLE").replace("MSFT", "MICROSOFT") in query_upper:
            price = get_stock_price(symbol)
            if price:
                return f"Current {symbol} stock price: ${price:.2f} (as of {datetime.now().strftime('%Y-%m-%d %H:%M')})"
    return None

def StockAgent(query: str):
    if not client:
        return "Stock analysis is not available due to AI model configuration issues."
    
    # Check for portfolio summary request
    if "summarize" in query.lower() and "portfolio" in query.lower():
        try:
            from Backend.Agents.PortfolioAnalytics import summarize_portfolio
            
            # Check if time period is specified
            query_lower = query.lower()
            time_period = None
            
            if "weekly" in query_lower or "week" in query_lower:
                time_period = "weekly"
            elif "monthly" in query_lower or "month" in query_lower:
                time_period = "monthly"
            elif "quarterly" in query_lower or "quarter" in query_lower:
                time_period = "quarterly"
            elif "annually" in query_lower or "annual" in query_lower or "yearly" in query_lower or "year" in query_lower:
                time_period = "annually"
            
            if time_period:
                return summarize_portfolio(time_period)
            else:
                # Ask user for time period preference
                return """I'd be happy to summarize your portfolio! Which time period would you like?
                
📊 Available Reports:
• **Weekly Report** - Last 7 days analysis
• **Monthly Report** - Last 30 days analysis  
• **Quarterly Report** - Last 90 days analysis
• **Annual Report** - Last 365 days analysis

Just say something like:
- "weekly portfolio summary"
- "show me monthly portfolio report"
- "quarterly portfolio analysis"
- "annual portfolio summary"

Or I can show you the **full history** if you just want to see everything!"""
                
        except ImportError:
            return "Portfolio analytics module not available. Please install matplotlib and pandas."
    
    # Check if this is a specific stock price query
    individual_stock = get_individual_stock_info(query)
    if individual_stock:
        context = individual_stock
    else:
        # Portfolio analysis
        portfolio_analysis = analyze_portfolio()
        context = f"""Portfolio Status:
- Total Value: ${portfolio_analysis['total_portfolio_value']:.2f}
- Cash: ${portfolio_analysis['cash']:.2f}

Holdings:"""
        
        for holding in portfolio_analysis['holdings_analysis']:
            context += f"\n- {holding['symbol']}: {holding['shares']} shares at ${holding['current_price']:.2f} (P&L: ${holding['gain_loss']:.2f})"
    
    system_prompt = f"You are Nexus, {Username}'s witty stock advisor. Use the provided data to answer with personality."
    
    messages_to_send = [
        {"role": "system", "content": system_prompt},
        {"role": "system", "content": context},
        {"role": "user", "content": query}
    ]
    
    try:
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=messages_to_send,
            max_tokens=1024,
            temperature=0.7,
            stream=False
        )
        
        return completion.choices[0].message.content.strip()
        
    except Exception as e:
        print(f"❌ Error in StockAgent: {e}")
        return "I'm having trouble analyzing your portfolio right now."

# --- TESTING BLOCK ---
if __name__ == "__main__":
    print("StockAgent test. Type 'exit' to end.")
    while True:
        user_input = input(f"{Username}: ")
        if user_input.lower() == 'exit':
            break
        response = StockAgent(user_input)
        print(f"Nexus: {response}")