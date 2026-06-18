import requests
import json
from datetime import datetime
import time

symbols = [
    "COMI","HRHO","OIH","CSAG","MEPA","OCDI","ARCC","NIPH","CCAP","UEGC","PHAR","AFMC","ORHD","EKHOA","SVCE",
    "MPCO","EFIH","AMER","VALU","EGTS","BIOC","ETRS","EEII","ISMQ","ELSH","TMGH","BTFH","SIPC","FWRY","ISPH",
    "AMES","POUL","SKPC","CEFM","RAYA","EMFD","RMDA","ABUK","ORAS","HELI","DAPH","ZEOT","LCSW","SCFM","MILS",
    "MCQE","ALCN","SWDY","AMIA","DSCW","COSG","MFPC","TAQA","MPRC","EIUD","ASCM","ORWE","PHGC","MENA","COPR",
    "ICFC","IDRE","EBSC","CAED","AMOC","MASR","JUFO","KRDI","IEEC","INEG","PRDC","IRON","EFID","ODIN","ELEC",
    "GIHD","CRST","ISMA","ACTF","BONY","ETEL","GGRN","ADCI","CNFN","GDWA","KASABF","MOED","ARAB","PRMH","OFH",
    "ACAMD","EAST","INFI","EGCH","CIRA","KZPC","MTIE","TANM","ROTO","NCCW","KABO","EHDR","UNIP","MCRO","ATLC",
    "PHTV","SUGR","ELKA","CIEB","ARVA","CLHO","DGTZ","ENGC","OLFI","GGCC","EFIC","AREH","ICID","FERC","MBEG",
    "AFDI","GTWL","SDTI","IFAP","QNBE","CPCI","EASB","SPMD","PRCL","HDBK","RREI","ACGC","NARE","MBSC","FAIT",
    "AIDC","MICH","SAUD","MAAL","CERA","EGAS","ASPI","WKOL","EXPA","FTNS","TALM","AIFI","MOIN","AJWA","NHPS",
    "ECAP","RUBX","ACAP","OBRI","AALR","MHOT","EDFM","ALUM","SUCE","EPCO","TORA","GRCA","LUTS","AIHC","APSW",
    "ADPC","ICMI","MOSC","ELWA","EALR","SEIG","CANA","BINV","HBCO","AXPH","SNFC","UNIT","OCPH","SPIN","NINH",
    "RTVC","UEFM","ANFI","DOMT","CCRS","KWIN","GSSC","AMPI","IBCT","ADRI","SMFR","SCTS","EPPK","BIGP","DTPP",
    "NEDA","WCDF","ACRO","ELNA","MIPH","VERT","ESRS","CICH","HCFI","NAPR","RAKT","APPC","EGREF","UASG","GTHE",
    "RKAZ","MFSC","GMCI","FNAR","ESAC","SNFI","UPMS","EGX30ETF","UBEE","BIDI","EKHO","ALEX","DIFC","EGBE","FIRE",
    "MOIL","FAITA","NCGC","MKIT","UTOP","NAHO","PACH","EOSB","EGSA","WATP","SMPP","GTEX","EITP","NBKE","KORA"
]

prices = {}
today = datetime.utcnow().strftime('%Y-%m-%d')

print(f"🔄 Fetching prices for {len(symbols)} symbols...")

def get_price_yahoo(symbol):
    """جلب السعر من Yahoo Finance"""
    try:
        ticker = symbol + ".CA"
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            result = data.get("chart", {}).get("result", [])
            if result:
                meta = result[0].get("meta", {})
                # نجيب السعر الفوري أو سعر الإغلاق السابق
                price = meta.get("regularMarketPrice")
                if not price:
                    price = meta.get("previousClose")
                if price and float(price) > 0:
                    return round(float(price), 4)
        return None
    except:
        return None

def get_price_alpha(symbol):
    """جلب السعر من Alpha Vantage (بديل)"""
    try:
        # استخدام API مجاني
        url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}.CA&apikey=demo"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            quote = data.get("Global Quote", {})
            price = quote.get("05. price")
            if price and float(price) > 0:
                return round(float(price), 4)
        return None
    except:
        return None

# جلب الأسعار
for sym in symbols:
    price = None
    
    # المحاولة الأولى: Yahoo Finance
    price = get_price_yahoo(sym)
    
    # لو فشلت، جرب البديل
    if not price:
        price = get_price_alpha(sym)
    
    if price and price > 0:
        prices[sym] = price
        print(f"✅ {sym}: {price}")
    else:
        print(f"— {sym}: no price")
    
    time.sleep(0.3)  # تأخير عشان ما نضغطش API

# نضيف تاريخ التحديث
output = {"last_updated": today}
output.update(prices)

with open("prices.json", "w") as f:
    json.dump(output, f, indent=2)

print(f"\n✅ Done: {len(prices)} prices saved, date: {today}")
