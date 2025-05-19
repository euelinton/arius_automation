from requests import Session
import pdfplumber
import pandas as pd

class Extractor:
    def __init__(self, url):
        self.session = Session()
        self.cookies = { "PHPSESSID": self.session.get(url).cookies["PHPSESSID"] } 
        self.headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36' }
    
    def login(self, url, data):
        self.session.post(url, cookies=self.cookies, headers=self.headers, data=data, verify=False)

    def fetch_html_after_login(self, url, params):
        resp = self.session.get(url, params=params, cookies=self.cookies, headers=self.headers, verify=False)
        return resp.content
    
    def extract_data_from_pdf(self, path):
        pdf = pdfplumber.open(path)
        dados = []

        for i, page in enumerate(pdf.pages):
            table = pdf.pages[i].extract_table()
            table = pd.DataFrame(table, columns=["Descrição", "Pdv",	"Hora",	"Operador",	"Supervisor",	"Valor",	"Cupom",	"EAN",	"Item"])
            dados.append(table)

        dados = pd.concat(dados)
        dados.dropna(inplace=True)
        dados.reset_index(drop=True, inplace=True)

        return dados
    