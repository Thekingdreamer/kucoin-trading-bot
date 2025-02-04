import os
from dotenv import load_dotenv
from kucoin.client import Market, Trade, User

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Leer las claves API desde el entorno
API_KEY = os.getenv("KUCOIN_API_KEY")
API_SECRET = os.getenv("KUCOIN_API_SECRET")
API_PASSPHRASE = os.getenv("KUCOIN_API_PASSPHRASE")

# Verificar que las claves se cargaron correctamente (solo para pruebas, luego puedes quitarlo)
print("API_KEY:", API_KEY)
print("API_SECRET:", API_SECRET)
print("API_PASSPHRASE:", API_PASSPHRASE)

#############################################
# Sección: Cliente Market (datos públicos)
#############################################

# Instanciar el cliente Market (la URL por defecto suele ser "https://api.kucoin.com")
market_client = Market()

# Ejemplo: obtener el ticker de un par de trading, por ejemplo, BTC-USDT
try:
    ticker = market_client.get_ticker("BTC-USDT")
    print("Ticker BTC-USDT:", ticker)
except Exception as e:
    print("Error al obtener el ticker:", e)

# Ejemplo: obtener el libro de órdenes (order book) para BTC-USDT
try:
    order_book = market_client.get_order_book("BTC-USDT")
    print("Order book BTC-USDT:", order_book)
except Exception as e:
    print("Error al obtener el libro de órdenes:", e)

#############################################
# Sección: Cliente Trade (operaciones de trading)
#############################################

# Instanciar el cliente Trade. Si operas en producción, deja is_sandbox en False
trade_client = Trade(API_KEY, API_SECRET, API_PASSPHRASE, is_sandbox=False)

# Ejemplo: crear una orden de mercado para comprar BTC utilizando USDT
try:
    order = trade_client.create_market_order(
        symbol="BTC-USDT",
        side="buy",   # "buy" para comprar o "sell" para vender
        funds=100     # Monto en USDT que deseas usar para comprar BTC
    )
    print("Orden creada:", order)
except Exception as e:
    print("Error al crear la orden:", e)

#############################################
# Sección: Cliente User (información de cuenta)
#############################################

# Instanciar el cliente User
user_client = User(API_KEY, API_SECRET, API_PASSPHRASE, is_sandbox=False)

# Ejemplo: obtener información de la cuenta (balances)
try:
    accounts = user_client.get_accounts()
    print("Cuentas y balances:", accounts)
except Exception as e:
    print("Error al obtener la información de la cuenta:", e)

#############################################
# Prueba de conexión (utilizando Trade para obtener lista de cuentas)
#############################################

try:
    account_info = trade_client.get_account_list()
    print("Conexión exitosa con KuCoin:", account_info)
except Exception as e:
    print("Error conectando con KuCoin:", e)

