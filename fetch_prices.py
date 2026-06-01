import yfinance as yf
import json

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
    "MOIL","FAITA","NCGC","MKIT","UTOP","NAHO","PACH","EOSB","EGSA","WATP","SMPP","GTEX","EITP","NBKE"
]

prices = {}

for sym in symbols:
    ticker = sym + ".CA"
    try:
        data = yf.download(ticker, period="5d", progress=False, auto_adjust=False)
        if data is not None and not data.empty:
            close = data["Close"].iloc[-1]
            if hasattr(close, 'item'):
                close = close.item()
            price = round(float(close), 4)
            if price > 0:
                prices[sym] = price
                print(f"✅ {sym}: {price}")
            else:
                print(f"— {sym}: invalid price")
        else:
            print(f"— {sym}: no data")
    except Exception as e:
        print(f"❌ {sym}: {e}")

with open("prices.json", "w") as f:
    json.dump(prices, f, indent=2)

print(f"\nDone: {len(prices)} prices saved")
