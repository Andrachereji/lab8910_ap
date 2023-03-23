from Domain.masina import Masina


class MasinaValidationError(Exception):
    pass


class MasinaValidator:

    def validate(self, masina: Masina):
        '''
        Face validarile necesare pentru masina nou introdusa
        :param masina: masina care se valideaza
        :return:erori daca exista
        '''
        valid_in_garantie = ['Da', 'Nu']
        errors = []
        if masina.in_garantie not in valid_in_garantie:
            errors.append(f'tastati "Da"=in garantie sau "Nu"=caz contrar')
        if masina.nr_km < 0:
            errors.append('Numarul de km trebuie sa fie strict pozitiv')
        if masina.an_achizitie < 0:
            errors.append('Anul achizitiei trebuie sa fie strict pozitiv')
        if errors:
            raise MasinaValidationError(errors)
