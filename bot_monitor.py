import requests
import time
import os

def get_top_50_dollar_volume_coins():
    url = "https://api.bybit.com/v5/market/tickers"
    params = {"category": "spot"}
    try:
        response = requests.get(url, params=params)
        data = response.json()
        if data.get("retCode") == 0:
            tickers = data["result"]["list"]
            valid_coins = []
            for ticker in tickers:
                symbol = ticker["symbol"]
                if symbol.endswith("USDT") and symbol != "USDCUSDT":
                    valid_coins.append({
                        "symbol": symbol,
                        "turnover": float(ticker.get("turnover24h", 0)),
                        "price": float(ticker.get("lastPrice", 0)),
                        "change_24h": float(ticker.get("price24hPcnt", 0)) * 100
                    })
            valid_coins.sort(key=lambda x: x["turnover"], reverse=True)
            return valid_coins[:50]
        return []
    except:
        return []

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def start_bot_with_monitor():
    my_positions = {}
    trade_log = []
    loop_count = 0

    while True:
        current_market = get_top_50_dollar_volume_coins()
        if not current_market:
            time.sleep(5)
            continue
            
        loop_count += 1
        market_dict = {coin["symbol"]: coin for coin in current_market}
        
        for symbol in list(my_positions.keys()):
            buy_price = my_positions[symbol]
            current_price = market_dict[symbol]["price"]
            profit_loss_percent = ((current_price - buy_price) / buy_price) * 100
            
            if profit_loss_percent <= -1.0:
                trade_log.append(f"[{time.strftime('%H:%M:%S')}] !!! STOP-LOSS !!! Eladva: {symbol} ({profit_loss_percent:.2f}%)")
                del my_positions[symbol]
                
        for symbol, coin_info in market_dict.items():
            if coin_info["change_24h"] >= 2.0 and symbol not in my_positions:
                if len(my_positions) < 3:
                    my_positions[symbol] = coin_info["price"]
                    trade_log.append(f"[{time.strftime('%H:%M:%S')}] *** VÉTEL *** {symbol} megvéve: {coin_info['price']:.4f}")

        clear_screen()
        print("=" * 70)
        print(f" BINANCE/BYBIT ALGORITHMIC TRADING MONITOR | Frissítés #{loop_count}")
        print(f" Idő: {time.strftime('%Y-%m-%d %H:%M:%S')} | Nyomj Ctrl+C-t a kilépéshez")
        print("=" * 70)
        
        print("\n[1] AKTÍV POZÍCIÓK (Védelmi vonal: -1.00% Stop-Loss)")
        print("-" * 70)
        print(f"{'COIN':<12} | {'VÉTELI ÁR':<12} | {'AKTUÁLIS ÁR':<12} | {'PROFIT / LOSS'}")
        print("-" * 70)
        
        if not my_positions:
            print("   Nincsenek aktív pozíciók. Robot keresi a megfelelő belépőt...")
        else:
            for symbol, buy_price in my_positions.items():
                curr_price = market_dict[symbol]["price"]
                pl = ((curr_price - buy_price) / buy_price) * 100
                print(f"{symbol:<12} | {buy_price:<12.4f} | {curr_price:<12.4f} | {pl:+.2f}%")
        print("-" * 70)

        print("\n[2] PIACI MONITOR (Top 5 legnagyobb forgalmú coin állapota)")
        print("-" * 70)
        for coin in current_market[:5]:
            print(f"-> {coin['symbol']:<10} | Ár: {coin['price']:<10.4f} | Napi változás: {coin['change_24h']:+.2f}%")
        
        print("\n[3] UTOLSÓ TRANZAKCIÓK ÉS ESEMÉNYEK")
        print("-" * 70)
        if not trade_log:
            print("   Még nem történt tranzakció.")
        else:
            for log in trade_log[-4:]:
                print(log)
        print("=" * 70)
        
        time.sleep(5)

if __name__ == "__main__":
    try:
        start_bot_with_monitor()
    except KeyboardInterrupt:
        print("\nRobot leállítva. Szép napot!")
