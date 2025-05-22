from extract import Extractor
from transform import Parser
from load import Load

url = "http://192.168.0.160/index.php"
url_login = "http://192.168.0.160/sistema/login.php"
url_canc = "http://192.168.0.160/ferramentas/relatorios/cancelamentos/selecao.php"
url_oc = "http://192.168.0.160/ferramentas/relatorios/ocorrencias/relatorio.php"

e = Extractor(url)
p = Parser()
l = Load()

data_login = {
    "USUARIO": "1000",
    "SENHA": "1947",
    "nroloja": "2",
}

params = {
<<<<<<< HEAD
    "dataproc_i": "14/05/2025",
    "dataproc_f": "21/05/2025",
=======
    "dataproc_i": "01/05/2025",
    "dataproc_f": "13/05/2025",
>>>>>>> 079e4a36b2d250212ff2f929ff24d315a48868c1
}

def main():
    # fazendo o login na página e criando uma sessão
    e.login(url=url_login, data=data_login)
    
    # adicionando conteudo da pagina de relatório de ocorrencia em um arquivo
    # pdf e salvando o caminho do arquivo em uma variável
    file_path_ec = l.append_to_pdf(e, url_oc, params, "ESTORNO CUPOM")
    file_path_ei = l.append_to_pdf(e, url_oc, params, "ESTORNO DE ITEM")
    file_path_rc = l.append_to_pdf(e, url_oc, params, "REIMP CUPOM")

    # extraindo dados da pagina arius (cancelamentos) e dos pdfs de ocorrencia
    canc = e.fetch_html_after_login(url=url_canc, params=params) 
    cupons = e.extract_data_from_pdf(file_path_ec)
    itens = e.extract_data_from_pdf(file_path_ei)
    reimps = e.extract_data_from_pdf(file_path_rc)

    #fazendo o parse dos dados
    canc = p.parse_report_canc(canc)
    cupons = p.parse_report_cupons(cupons)
    itens = p.parse_report_itens(itens)
    reimps = p.parse_report_reimps(reimps)

    data = p.join_dataframes(canc, cupons, itens, reimps)
    l.append_to_excel(data)

if __name__ == "__main__":
    main()
