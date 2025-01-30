import os
import time
import pandas as pd
import numpy as np
from dotenv import load_dotenv
from kucoin.market.market import MarketData
from kucoin.trade.trade import TradeData
from kucoin.user.user import UserData

# Cargar las claves desde el archivo .env
load_dotenv()
api_key = os.getenv("KUCOIN_API_KEY")
api_secret = os.getenv("KUCOIN_API_SECRET")
api_passphrase = os.getenv("KUCOIN_API_PASSPHRASE")

# Instanciar las clases con autenticación
market = MarketData(api_key, api_secret, api_passphrase)
trade = TradeData(api_key, api_secret, api_passphrase)
user = UserData(api_key, api_secret, api_passphrase)

# Probar una solicitud, por ejemplo, obtener datos de mercado
print(market.get_ticker('BTC-USDT'))


# Función para calcular RSI mejorada
def calcular_rsi(data, periodo=14):
    delta = data['close'].diff()
    ganancias = delta.clip(lower=0)
    perdidas = -delta.clip(upper=0)
    
    # Usar promedio móvil exponencial
    avg_ganancia = ganancias.ewm(alpha=1/periodo, adjust=False).mean()
    avg_perdida = perdidas.ewm(alpha=1/periodo, adjust=False).mean()
    
    rs = avg_ganancia / avg_perdida
    return 100 - (100 / (1 + rs))

# Función para calcular ATR mejorada
def calcular_atr(data, periodo=14):
    high_low = data['high'] - data['low']
    high_close = np.abs(data['high'] - data['close'].shift())
    low_close = np.abs(data['low'] - data['close'].shift())
    
    tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    return tr.rolling(periodo).mean()

# Estrategia principal con mejor manejo de errores
def ejecutar_estrategia(symbol="BTC-USDT"):
    try:
        # Obtener datos históricos
        velas = client.get_kline_data(symbol=symbol, interval="1day")
        
        # Crear DataFrame con nombres de columnas correctos
        df = pd.DataFrame(velas, columns=[
            'timestamp', 'open', 'high', 'low', 'close', 'volume', 'turnover'
        ])
        
        # Conversión de tipos de datos
        df = df.apply(pd.to_numeric)
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
        
        # Calcular indicadores
        df['MA50'] = df['close'].rolling(50).mean()
        df['MA200'] = df['close'].rolling(200).mean()
        df['RSI'] = calcular_rsi(df)
        df['ATR'] = calcular_atr(df)
        
        # Filtrar datos válidos
        if len(df.dropna()) < 50:
            raise ValueError("Datos insuficientes para análisis")
            
        # Obtener últimos valores
        ultimo = df.iloc[-1]
        
        # Lógica de trading
        if ultimo['MA50'] > ultimo['MA200'] and ultimo['RSI'] < 70:
            stop_loss = ultimo['close'] - (ultimo['ATR'] * 1.5)
            return f"🚀 COMPRAR {symbol} | Precio: {ultimo['close']:.2f} | Stop Loss: {stop_loss:.2f}"
            
        elif ultimo['MA50'] < ultimo['MA200'] and ultimo['RSI'] > 30:
            return f"🔴 VENDER {symbol} | Precio: {ultimo['close']:.2f}"
            
        return "🟡 Mantener posición actual"
        
    except Exception as e:
        return f"❌ Error en estrategia: {str(e)}"

# Ejecutar en ciclo continuo
if __name__ == "__main__":
    while True:
        try:
            señal = ejecutar_estrategia()
            print(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {señal}")
            time.sleep(3600)  # Esperar 1 hora entre ejecuciones
            
        except KeyboardInterrupt:
            print("\n🔧 Ejecución detenida por el usuario")
            break
            
        except Exception as e:
            print(f"⚠️ Error general: {str(e)}")
            time.sleep(300)  # Esperar 5 minutos ante errores
