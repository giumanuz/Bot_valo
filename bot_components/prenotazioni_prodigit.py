from datetime import date, time
from enum import Enum

from requests import Session

from bot_components.prodigit_business_rules import Prodigit


class PrenotazioneProdigit:
    REQUEST_TIMEOUT = 6

    def __init__(self,
                 username: str,
                 prodigit_password: str,
                 email: str,
                 nome: str,
                 cognome: str,
                 aula: 'Aula'):
        self.username = username
        self.password = prodigit_password
        self.email = email
        self.nome = nome
        self.cognome = cognome
        self.aula = aula.value
        self.codice_edificio = aula.get_codice_edificio()
        self._session = Session()
        self.booked_days: dict[int, tuple[time, time]] = {}

    def add_day(self, day: date, hour_from: time, hour_to: time):
        day_code = Prodigit.get_prenotation_day(day)
        self.booked_days[day_code] = (hour_from, hour_to)

    def prenota(self):
        self.__login()
        data = self.get_data()
        self._make_prenotation(data)

    def _make_prenotation(self, data: dict):
        self._session.post(url=Prodigit.PRENOTATION_URL,
                           data=data,
                           timeout=self.REQUEST_TIMEOUT)

    def __login(self):
        self._session.post(
            url=Prodigit.LOGIN_URL,
            data={"Username": self.username, "Password": self.password},
            timeout=self.REQUEST_TIMEOUT
        )

    def get_data(self) -> dict[str, str]:
        data = {
            '__Click': 'C12585E7003519C8.c8e9f943d3b2819fc12587ed0064a0a2/$Body/2.16E',
            'codiceedificio': self.codice_edificio,
            'aula': self.aula,
            'email': self.email,
            'cognome': self.cognome,
            'nome': self.nome
        }
        for day, hours in self.booked_days.items():
            data[f'dalleore{day}'] = hours[0].strftime("%H:%M")
            data[f'alleore{day}'] = hours[1].strftime("%H:%M")
        return data


class PrenotazioneEsameProdigit(PrenotazioneProdigit):
    def _make_prenotation(self, data: dict):
        self._session.post(url=Prodigit.EXAM_PRENOTATION_URL,
                           data=data,
                           timeout=self.REQUEST_TIMEOUT)


class Aula(Enum):
    MP_204 = "AULA 204 -- RM021-P02L004"
    MP_108 = "AULA 108 -- RM021-P01L008"
    MP_106 = "AULA 106 -- RM021-P01L006"
    LAB_TIB_15 = "AULA INFORMATICA 15 -- RM025-E01PTEL024"
    LAB_TIB_17 = "AULA INFORMATICA 17 -- RM025-E01PTEL001"

    def get_nome_aula(self):
        return self.value.split('--')[0].strip()

    def get_codice_edificio(self):
        codice_edificio_aula: str = self.value.split('--')[1].strip()
        return codice_edificio_aula.split('-')[0]
