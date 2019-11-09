import requests
import json
from pandas.io.json import json_normalize
import numpy as np
import pandas as pd

headers = {'content-type': 'application/json', 'auth_token': 'daSY92P7JMXZzFBkZCDDMYiU'}
url = 'https://tecton.buk.cl/api/v1/accounting/export?month=10&year=2019&company_id=76.407.152-2'
r = requests.get(url, headers=headers)

buk = json.loads(r.content)

data = json_normalize(buk["data"]["76.407.152-2"]["Constructora Tecton S.p.A."])

data["deber"] = data["deber"].replace({'': 0})
data["haber"] = data["haber"].replace({'': 0})

with open("relaciones.json", "r") as read_file:
    relaciones = json.load(read_file)

data["cuenta_contable"] = data["cuenta_contable"].replace(relaciones)

data_buk_agrupada = data.groupby(["centro_costo", "cuenta_contable"])["deber", "haber"].agg(np.sum)

#imprimir los distintos centros de costo
print(data.centro_costo.unique())

#for(centro_costo in data.centro_costo.unique()):


print(data_buk_agrupada.loc['2014.OFI.001'])

#for index, row in data_buk_agrupada.iterrows():
#    print(index[0], index[1], row['deber'], row['haber'])


