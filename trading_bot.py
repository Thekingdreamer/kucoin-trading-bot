import os
from dotenv import load_dotenv
from kucoin.trade import TradeData

# Cargar las variables desde el .env
load_dotenv()

# Leer las claves API desde el entorno
API_KEY = os.getenv("KUCOIN_API_KEY")
API_SECRET = os.getenv("KUCOIN_API_SECRET")
API_PASSPHRASE = os.getenv("KUCOIN_API_PASSPHRASE")

# Verificar que las claves se cargaron correctamente (esto es solo para pruebas, luego puedes quitarlo)
print("API_KEY:", API_KEY)
print("API_SECRET:", API_SECRET)
print("API_PASSPHRASE:", API_PASSPHRASE)

# Inicializar el cliente de KuCoin
client = Client(API_KEY, API_SECRET, API_PASSPHRASE)

# Prueba de conexión
try:
    account_info = client.get_account_list()
    print("Conexión exitosa con KuCoin:", account_info)
except Exception as e:
    print("Error conectando con KuCoin:", e)
