import time
import pandas as pd
import numpy as np
from kucoin.client import Client

# Configura tus credenciales de API de KuCoin
api_key = 'tu_api_key'
api_secret = 'tu_api_secret'
api_passphrase = 'tu_api_passphrase'

client = Client(api_key, api_secret, api_passphrase)

# Prueba de conexión
try:
    account_info = client.get_account_list()  # Ejemplo de prueba
    print("Conexión exitosa con KuCoin:", account_info)
except Exception as e:
    print("Error conectando con KuCoin:", e)

def calcular_rsi(data, periodo=14):
    delta = data['close'].diff()
    ganancias = delta.clip(lower=0)
    perdidas = -delta.clip(upper=0)
    avg_ganancia = ganancias.rolling(periodo).mean()
    avg_perdida = perdidas.rolling(periodo).mean()
    rs = avg_ganancia / avg_perdida
    return 100 - (100 / (1 + rs))

def calcular_atr(data, periodo=14):
    high_low = data['high'] - data['low']
    high_close = np.abs(data['high'] - data['close'].shift())
    low_close = np.abs(data['low'] - data['close'].shift())
    tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    return tr.rolling(periodo).mean()

def estrategia_trading(symbol="BTC-USDT"):
    try:
        # Obtener datos históricos
        velas = client.get_kline_data(symbol=symbol, interval="1day")
        df = pd.DataFrame(velas, columns=["timestamp", "open", "close", "high", "low", "volume"])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
        
        # Calcular indicadores
        df['MA50'] = df['close'].rolling(50).mean()
        df['MA200'] = df['close'].rolling(200).mean()
        df['RSI'] = calcular_rsi(df)
        df['ATR'] = calcular_atr(df)
        
        # Últimos valores
        ultimo_precio = df['close'].iloc[-1]
        ma50 = df['MA50'].iloc[-1]
        ma200 = df['MA200'].iloc[-1]
        rsi = df['RSI'].iloc[-1]
        atr = df['ATR'].iloc[-1]
        
        # Lógica de trading
        if (ma50 > ma200) and (rsi < 70):
            # Señal de COMPRA
            stop_loss = ultimo_precio - (atr * 1.5)
            print(f"🚀 COMPRAR {symbol} | Precio: {ultimo_precio} | Stop Loss: {stop_loss}")
            
        elif (ma50 < ma200) and (rsi > 30):
            # Señal de VENTA
            print(f"🔴 VENDER {symbol} | Precio: {ultimo_precio}")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    while True:
        estrategia_trading()
        time.sleep(86400)  # Ejecutar cada 24 horas
