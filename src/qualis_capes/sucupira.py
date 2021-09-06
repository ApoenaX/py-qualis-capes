import os
import pandas as pd
from pandas import DataFrame
from datetime import datetime
from .download import _download_data


class QualisCapes:
    _ROOT = os.path.abspath(os.path.dirname(__file__))

    def __init__(self):
        self.__load_data__()

    def __load_data__(self):
        self.trien = pd.read_csv(
            os.path.join(self._ROOT, "data/triênio.tsv"),
            encoding="ISO-8859-1",
            sep="\t",
        )
        self.quadr = pd.read_csv(
            os.path.join(self._ROOT, "data/quadriênio.tsv"),
            encoding="ISO-8859-1",
            sep="\t",
        )
        with open(os.path.join(self._ROOT, "data/last-update.txt"), "r") as text_file:
            self.last_update = text_file.read()
            text_file.close()

    def __filter_by__(self, key: str, value: str, event: str) -> DataFrame:
        value = value.upper()
        if event == "triênio":
            return self.trien[self.trien[key].str.contains(value, na=False)]
        elif event == "quadriênio":
            return self.quadr[self.quadr[key].str.contains(value, na=False)]

    def by_area(self, area: str, event: str = "quadriênio") -> DataFrame:
        """Obtém lista de revistas para a área informada.

        Args:
            area (str): Nome da área de avaliação
            event (str, optional): Tipo do evento de classificação (quadriênio ou triênio). Defaults to "quadriênio".

        Returns:
            DataFrame: Resultado contendo informações das revistas para a área informada.
        """
        return self.__filter_by__("Área de Avaliação", area, event)

    def by_title(self, title: str, event: str = "quadriênio") -> DataFrame:
        """ "Obtém lista de revistas que contenham parte do título informado.

        Args:
            title (str): título da revista, também pode ser parte dele.
            event (str, optional): Tipo do evento de classificação (quadriênio ou triênio). Defaults to "quadriênio".

        Returns:
            DataFrame: Resultado contendo informações das revistas para o título informado.
        """
        return self.__filter_by__("Título", title, event)

    def by_issn(self, issn: str, event: str = "quadriênio") -> DataFrame:
        """ "Obtém lista de informações da revista para o issn informado.

        Args:
            issn (str): ISSN na revista no formato 1949-8454
            event (str, optional): Tipo do evento de classificação (quadriênio ou triênio). Defaults to "quadriênio".

        Returns:
            DataFrame: Resultado contendo informações da revista para o issn informado.
        """
        return self.__filter_by__("ISSN", issn, event)

    def by_classification(self, value: str, event: str = "quadriênio") -> DataFrame:
        """ "Obtém lista de revistas para o estrato informado.

        Args:
            value (str): Pode ser um dos seguintes valores A1, A2, B1, B2, B3, B4 e C
            event (str, optional): Tipo do evento de classificação (quadriênio ou triênio). Defaults to "quadriênio".

        Returns:
            DataFrame: Resultado contendo informações das revistas para o estrato informado.
        """
        return self.__filter_by__("Estrato", value, event)

    def get_table(self, event="quadriênio") -> DataFrame:
        """Obtém lista de revistas para o evento de classificação informado.

        Args:
            event (str, optional): Tipo do evento de classificação (quadriênio ou triênio). Defaults to "quadriênio".

        Returns:
            DataFrame: Resultado contendo uma lista das revistas para o evento de classificação informado.
        """
        if event == "triênio":
            return self.trien
        elif event == "quadriênio":
            return self.quadr

    def update_data(self) -> None:
        """Realiza download das tabelas de qualis-periódicos."""
        # realiza download dos dados
        _download_data("triênio")
        _download_data("quadriênio")

        # obtém a data/hora atual
        now = datetime.now()
        self.last_update = now.strftime("%d/%m/%Y %H:%M:%S")
        with open(os.path.join(self._ROOT, "data/last-update.txt"), "w") as text_file:
            text_file.write(self.last_update)
            text_file.close()
        print(self.last_update)

        # carrega os arquivos baixados na memória
        self.__load_data__()
