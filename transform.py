import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from io import StringIO

class Parser:
    def __init__(self):
        pass
    
    def parse_report_canc(self, text):
        soup = BeautifulSoup(text, 'html.parser')
        table = soup.find_all(class_='datagrid')
        table_str = str(table)

        df = pd.read_html(StringIO(table_str))[0]
        df.columns = df.iloc[0]
        df.drop(0, inplace=True)

        df = df[["Nro.cupom", "PDV", "Data", "Operador", "merc", "Valor", "Tipo cancelamento"]]
        df.rename(columns={"Nro.cupom": "Cupom", "merc": "Item", "PDV": "Pdv"}, inplace=True)
        df.dropna(inplace=True)

        df["Valor"] = df["Valor"].astype(str)
        df["Valor"] = df["Valor"].str.replace(".", ",")
        df["Data"] = pd.to_datetime(df["Data"], format="%d/%m/%Y")
        
        return df
    
    def parse_report_reimps(self, reimps):
        if (reimps.iloc[0].values == reimps.columns).all():
            reimps.iloc[0] = ""
            reimps["CE"] = ""
        else: 
            reimps["CE"] = [t[3].replace(",", "") for t in reimps["Item"].str.split().values]
            reimps["Descrição"] = "CUPOM RECUPERADO"
    
        return reimps
    def parse_report_cupons(self, cupons):
        return cupons[["Cupom", "Pdv", "Hora", "Operador", "Valor", "Descrição"]]
    
    def parse_report_itens(self, itens):
        return itens[["Cupom", "Pdv", "Hora", "Operador", "EAN", "Item", "Valor", "Descrição"]]
    
    def join_dataframes(self, canc, cupons, itens, reimps):
        for ic, rc in canc.iterrows():
            for ii, ri in itens.iterrows():
                if rc["Item"] == "năo encontrado" and rc["Cupom"] == ri["Cupom"]:
                    canc.loc[ic, "Tipo de Estorno"] = "ESTORNO DE ITEM"
                if rc["Cupom"] == ri["Cupom"] and rc["Item"] == ri["Item"] and rc["Valor"] == ri["Valor"]:
                    canc.loc[ic, "Tipo de Estorno"] = "ESTORNO DE ITEM"  
                    #print("index canc:", ic,"index item: ",ii, ri[["Hora", "Item"]])
                    #print("-------------------------------------------------------")  
                    itens.drop(ii, inplace=True)
                    break
        canc.loc[(canc["Tipo de Estorno"] == "nan") | (canc["Tipo de Estorno"].isna()), "Tipo de Estorno"] = "ESTORNO DE CUPOM"
        canc["Status"] = np.where(canc["Cupom"].isin(reimps["CE"]), "CUPOM RECUPERADO", "CUPOM NÃO RECUPERADO")
        # canc.to_json("dados.json")
        return canc
 