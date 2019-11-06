from frappeclient import FrappeClient
import json

try:
    client = FrappeClient("https://erp.tecton.cl", "lizquierdo@tecton.cl", "tecton")
except:
    print("ERROR LOGEARSE AL ERP")
    raise

with open("voucher_template.json", "r") as read_file:
    voucher = json.load(read_file)

resultado = client.insert(voucher)

print(resultado)
