import yfinance as yf
import json
from datetime import datetime

def fetch_current_prices():
    # قراءة الأسهم من portfolio_symbols.json
    try:
        with open('portfolio_symbols.json', 'r') as f:
            data = json.load(f)
            symbols = data.get('symbols', [])
    except:
        print("⚠️ ملف portfolio_symbols.json مش موجود")
        return
    
    if not symbols:
        print("⚠️ مفيش أسهم في الملف")
        return
    
    print(f"📊 جاري تحديث {len(symbols)} سهم...")
    prices = {}
    
    for symbol in symbols:
        try:
            ticker = yf.Ticker(symbol)
            data = ticker.history(period="2d")
            if not data.empty:
                current_price = round(data['Close'].iloc[-1], 2)
                prices[symbol] = current_price
                print(f"✅ {symbol}: {current_price} EGP")
            else:
                prices[symbol] = None
                print(f"❌ {symbol}: مفيش بيانات")
        except Exception as e:
            print(f"❌ {symbol}: خطأ - {str(e)}")
            prices[symbol] = None
    
    with open('prices.json', 'w') as f:
        json.dump({
            'last_update': datetime.now().isoformat(),
            'prices': prices
        }, f, indent=2)
    
    updated = len([p for p in prices.values() if p])
    print(f"\n✅ تم تحديث {updated} من {len(symbols)} سهم")

if __name__ == "__main__":
    fetch_current_prices()
