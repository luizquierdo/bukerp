import requests
from pandas.io.json import json_normalize
import numpy as np
from voucher import Voucher, JournalEntryAccount
from frappeclient import FrappeClient
import pandas

import json

try:
    client = FrappeClient("https://erp.tecton.cl", "lizquierdo@tecton.cl", "tecton")
except:
    print("ERROR LOGEARSE AL ERP")
    raise

with open("output.json", "r") as read_file:
    voucher = json.load(read_file)

print(client.get_doc('Journal Entry', 'JV-16352'))

headers = {'content-type': 'application/json', 'auth_token': 'daSY92P7JMXZzFBkZCDDMYiU'}
url = 'https://tecton.buk.cl/api/v1/accounting/export?month=10&year=2019&company_id=76.407.152-2'
r = requests.get(url, headers=headers)

buk = json.loads(r.content)

data = json_normalize(buk["data"]["76.407.152-2"]["Constructora Tecton S.p.A."])

data["deber"] = data["deber"].replace({'': 0})
data["haber"] = data["haber"].replace({'': 0})

with open("relaciones_cuentas.json", "r") as read_file:
    relaciones_cuentas = json.load(read_file)

data["cuenta_contable"] = data["cuenta_contable"].replace(relaciones_cuentas)

with open("relaciones_centros_de_costos.json", "r") as read_file:
    relaciones_centros_de_costo = json.load(read_file)

data["centro_costo"] = data["centro_costo"].replace(relaciones_centros_de_costo)

data_buk_agrupada = data.groupby(["centro_costo", "cuenta_contable"])["deber", "haber"].agg(np.sum)

prestamos = data_buk_agrupada.loc[(slice(None), '1.1.6.2 Prestamos al Personal - T'), :]
data_buk_agrupada = data_buk_agrupada.drop(prestamos.index)


for cc in data.centro_costo.unique():

    v = Voucher('2019-10-25', '2019-10-25', cc)

    print(cc)
    data_cc = data_buk_agrupada.loc[cc]
    for cuenta in data_cc.index:
        je = JournalEntryAccount(float(data_cc.loc[cuenta].deber), float(data_cc.loc[cuenta].haber), cuenta, cc)
        v.agregarCuenta(je)
    print(json.dumps(v.dict_voucher))
    #r = client.insert(v.dict_voucher)
    #print(r)

print(data_buk_agrupada)

resultado = client.insert(voucher)








