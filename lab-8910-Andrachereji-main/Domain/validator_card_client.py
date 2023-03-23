from Domain.card_client import Card_client


class Card_clientValidationError(Exception):
    pass


class Card_clientValidator:
    def validate(self, card_client: Card_client):
        '''
        Verifica daca data nasterii si data
        inregistrarii sun de tip dd.mm.yyyy
        :param card_client: cardul la care verificam proprietatile
        :return: erori daca exista
        '''
        lst = []
        errors = []
        data_n = card_client.data_nasterii.split('.')
        for cuv in data_n:
            lst.append(int(cuv))
        if len(lst) != 3:
            errors.append('Data nasterii sa fie de forma dd.mm.yyyy')
        elif lst[0] < 1 or lst[0] > 31:
            errors.append('Data nasterii sa fie de forma dd.mm.yyyy')
        elif lst[1] < 1 or lst[1] > 12:
            errors.append('Data nasterii sa fie de forma dd.mm.yyyy')
        elif lst[2] < 1000:
            errors.append('Data nasterii sa fie de forma dd.mm.yyyy')
        lst2 = []
        data_i = card_client.data_inregistrarii.split('.')
        for cuv in data_i:
            lst2.append(int(cuv))
        if len(lst2) != 3:
            errors.append('Data inregistrarii sa fie de forma dd.mm.yyyy')
        elif lst2[0] < 1 or lst2[0] > 31:
            errors.append('Data inregistrarii sa fie de forma dd.mm.yyyy')
        elif lst2[1] < 1 or lst2[1] > 12:
            errors.append('Data inregistrarii sa fie de forma dd.mm.yyyy')
        elif lst2[2] < 1000:
            errors.append('Data inregistrarii sa fie de forma dd.mm.yyyy')
        if errors:
            raise Card_clientValidationError(errors)
