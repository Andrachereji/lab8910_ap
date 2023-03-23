from Service.card_client_service import Card_clientService
from Service.masina_service import MasinaService


class CautareText:
    def __init__(self,
                 masina_service: MasinaService,
                 card_client_service: Card_clientService):
        self.masina_service = masina_service
        self.card_client_service = card_client_service

    def cautare_full_text(self, text_str):
        '''
        se cauta toate obiectele ce contin textul "text_str"
        :param text_str:textul introdus
        :return: o lista cu toate obiectele
        '''

        result = []
        masini = self.masina_service.get_all()
        carduri_clienti = self.card_client_service.get_all()
        for masina in masini:
            if text_str in masina.id_entity:
                result.append(masina)
            if text_str in masina.model:
                result.append(masina)
            if text_str in str(masina.nr_km):
                result.append(masina)
            if text_str in str(masina.an_achizitie):
                result.append(masina)
            if text_str in masina.in_garantie:
                result.append(masina)
        for card in carduri_clienti:
            if text_str in card.id_entity:
                result.append(card)
            if text_str in card.nume:
                result.append(card)
            if text_str in card.prenume:
                result.append(card)
            if text_str in card.cnp:
                result.append(card)
            if text_str in card.data_inregistrarii:
                result.append(card)
            if text_str in card.data_nasterii:
                result.append(card)
        return result
