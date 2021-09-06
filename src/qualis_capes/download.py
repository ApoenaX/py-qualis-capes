import os
import re
import requests
from tqdm import tqdm
from bs4 import BeautifulSoup

_ROOT = os.path.abspath(os.path.dirname(__file__))
_url = "https://sucupira.capes.gov.br/sucupira/public/consultas/coleta/veiculoPublicacaoQualis/listaConsultaGeralPeriodicos.xhtml"


def _get_event_option(html: str, name: str) -> str:
    keyword = name.upper()
    soup = BeautifulSoup(html, "html.parser")
    event = soup.find("select", {"id": "form:evento"})
    if event:
        for op in event.findAll("option")[1:]:
            if keyword in op.get_text():
                return op.get("value")


def _download_data(keyword: str = "quadriênio") -> None:

    if keyword.lower() not in ["quadriênio", "triênio"]:
        return

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept-Encoding": "gzip, deflate, br",
    }

    # Definição dos campos do formulário
    data = {
        "form": "form",
        "form:area": 0,
        "form:estrato": 0,
        "form:consultar": "Consultar",
    }

    # Abre uma sessão para realizar o download dos dados
    with requests.session() as session:

        # realiza primeiro acesso a página para obter ViewState
        init = session.get(_url)
        soup = BeautifulSoup(init.text, "html.parser")

        # preenche os campos restantes do formulário de busca
        data["form:evento"] = _get_event_option(init.text, keyword)
        data["javax.faces.ViewState"] = soup.find(
            "input", {"id": "javax.faces.ViewState"}
        ).get("value")

        # realiza nova solicitação com os campos faltantes preenchidos
        response = session.post(_url, data=data)
        page = BeautifulSoup(response.text, "lxml")

        # obtém informações sobre o campo de download do arquivo
        field_file = page.select_one("td > a")["onclick"]
        file_download = re.compile(r"form:j_idt\d+")
        field_file = file_download.search(field_file)
        field_file = field_file.group()
        data[field_file] = field_file

        #  realiza solicitação para fazer download do arquivo
        response = session.post(_url, data=data, stream=True, headers=headers)

        # definição de propriedades da progress bar
        total_size_in_bytes = int(response.headers.get("content-length", 0))
        block_size = 1024
        progress_bar = tqdm(
            total=total_size_in_bytes,
            unit="iB",
            unit_scale=True,
            desc=f"Fazendo download de {keyword}.csv",
        )

        # realizar o download do arquivo no disco
        with open(os.path.join(_ROOT, f"data/{keyword}.tsv"), "wb") as file:
            for data in response.iter_content(block_size, decode_unicode=True):
                progress_bar.update(len(data))
                file.write(data)
        progress_bar.close()
