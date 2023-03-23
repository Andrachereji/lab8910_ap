from Service.card_client_service import Card_clientService
from Service.cautare_full_text import CautareText
from Service.masina_service import MasinaService
from Service.tranzactie_service import TranzactieService
from Service.undo_redo_service import UndoRedoService


class Console:
    def __init__(self,
                 masina_service: MasinaService,
                 card_client_service: Card_clientService,
                 tranzactie_service: TranzactieService,
                 undo_redo_service: UndoRedoService):
        self.masina_service = masina_service
        self.card_client_service = card_client_service
        self.tranzactie_service = tranzactie_service
        self.undo_redo_service = undo_redo_service

    def show_menu(self):
        print('a[masina|card|tran]:adaugare masina/card_client/tranzactie')
        print('u[masina|card|tran]:update masina/card_client/tranzactie')
        print('d[masina|card|tran]:stergere masina/card_client/tranzactie')
        print('s[masina|card|tran]:show all masina/card_client/tranzactie')
        print('cft:Cautare masini si carduri.Cautare full text')
        print('at: Afișare tranzactii cu suma in interval dat.')
        print('rm: Generare n entitati de tip masina cu valori random')
        print('ordmasina: Ordonare masini descrescător după '
              'suma obținută pe manoperă')
        print('ordcard:Afișarea cardurilor client ordonate descrescător'
              'după valoarea reducerilor obținute.')
        print('straninterval:Ștergerea tuturor tranzacțiilor '
              'dintr-un anumit interval de zile')
        print('actmasina: Actualizarea masinii '
              '(daca masina are maxim 3 ani de la achizitie si nu '
              'mai mult de 60 000 de km va fi in garantie daca nu nu')
        print('undo')
        print('redo')
        print('x.Iesire')

    def run_console(self):
        while True:
            self.show_menu()
            opt = input('Alegeti optiunea:')
            if opt == 'amasina':
                self.handle_adaugare_masina()
            elif opt == 'umasina':
                self.handle_update_masina()
            elif opt == 'dmasina':
                self.handle_stergere_masina()
            elif opt == 'smasina':
                self.handle_show_all(self.masina_service.get_all())
            elif opt == 'acard':
                self.handle_adaugare_card_client()
            elif opt == 'ucard':
                self.handle_update_card_client()
            elif opt == 'dcard':
                self.handle_stergere_card_client()
            elif opt == 'scard':
                self.handle_show_all(self.card_client_service.get_all())
            elif opt == 'atran':
                self.handle_adaugare_tranzactie()
            elif opt == 'utran':
                self.handle_update_tranzactie()
            elif opt == 'dtran':
                self.handle_stergere_tranzactie()
            elif opt == 'stran':
                self.handle_show_all(self.tranzactie_service.get_all())
            elif opt == 'cft':
                self.handle_cautare_full_text()
            elif opt == 'at':
                self.handle_get_interval()
            elif opt == 'rm':
                self.handle_random_cars()
            elif opt == 'ordmasina':
                result = self.tranzactie_service \
                    .get_ordonare_masini_dupa_suma_manopera()
                self.handle_show_all(result)
            elif opt == 'ordcard':
                result = self.tranzactie_service \
                    .get_ordonare_card_dupa_reducere()
                self.handle_show_all(result)
            elif opt == 'straninterval':
                self.handle_stergere_tranzactie_interval()
            elif opt == 'actmasina':
                self.handle_actualizare_masina()
            elif opt == 'undo':
                self.undo_redo_service.do_undo()
            elif opt == 'redo':
                self.undo_redo_service.do_redo()
            elif opt == 'x':
                break
            else:
                print('optiune invalida')

    def handle_adaugare_masina(self):
        try:
            id_masina = input('Dati id-ul masinii:')
            model = input('Dati modelul masinii:')
            an_achizitie = int(input('Dati anul achizitiei masinii:'))
            nr_km = float(input('Dati numarul de km al masinii:'))
            in_garantie = input('Precizati daca masina e in garantie:')
            self.masina_service.adaugare_masina(id_masina, model, an_achizitie,
                                                nr_km, in_garantie)
        except ValueError as ve:
            print('Eroare de validare:', ve)
        except KeyError as ke:
            print('Eroare de ID:', ke)
        except Exception as ex:
            print('Eroare:', ex)

    def handle_show_all(self, objects):
        for obj in objects:
            print(obj)

    def handle_adaugare_card_client(self):
        try:
            id_card_client = input('Dati id-ul cardului:')
            nume = input('Dati numele clientului:')
            prenume = input('Dati prenumele clientului:')
            cnp = input('Dati cnp-ul clientului:')
            data_nasterii = input('Dati data nasterii clientului:')
            data_inregistrarii = input('Dati data inregistrarii')
            self.card_client_service.adaugare_card_client(id_card_client,
                                                          nume,
                                                          prenume,
                                                          cnp,
                                                          data_nasterii,
                                                          data_inregistrarii)
        except ValueError as ve:
            print('Eroare de validare:', ve)
        except KeyError as ke:
            print('Eroare de ID:', ke)
        except Exception as ex:
            print('Eroare:', ex)

    def handle_adaugare_tranzactie(self):
        try:
            id_tranzactie = input('Dati id-ul tranzactiei')
            id_masina = input('Dati id-ul masinii')
            id_card_client = input('Dati id-ul cardului doar '
                                   'daca acesta exista:')
            suma_piese = float(input('Dati suma pieselor:'))
            suma_manopera = float(input('Dati suma manoperelor:'))
            data = input('Dati data tranzactiei:')
            ora = input('Dati ora tranzactiei:')
            self.tranzactie_service.adaugare_tranzactie(id_tranzactie,
                                                        id_masina,
                                                        id_card_client,
                                                        suma_piese,
                                                        suma_manopera,
                                                        data,
                                                        ora)
        except ValueError as ve:
            print('Eroare de validare:', ve)
        except KeyError as ke:
            print('Eroare de ID:', ke)
        except Exception as ex:
            print('Eroare:', ex)

    def handle_update_masina(self):
        try:
            id_masina = input('Dati id-ul masinii care se modifica:')
            model = input('Dati noul  model al masinii:')
            an_achizitie = int(input('Dati noul an al achizitiei masinii:'))
            nr_km = float(input('Dati noul numar de km al masinii:'))
            in_garantie = input('Precizati daca masina e in garantie:')
            self.masina_service.update_masina(id_masina, model,
                                              an_achizitie, nr_km, in_garantie)
        except ValueError as ve:
            print('Eroare de validare:', ve)
        except KeyError as ke:
            print('Eroare de ID:', ke)
        except Exception as ex:
            print('Eroare:', ex)

    def handle_stergere_masina(self):
        try:
            id_masina = input('Dati id-ul masinii care se sterge:')
            self.masina_service.stergere_masina(id_masina)
            self.tranzactie_service.stergere_tranzactie_masina(id_masina)
        except ValueError as ve:
            print('Eroare de validare:', ve)
        except KeyError as ke:
            print('Eroare de ID:', ke)
        except Exception as ex:
            print('Eroare:', ex)

    def handle_update_card_client(self):
        try:
            id_card_client = input('Dati id-ul cardului care se actualizeaza:')
            nume = input('Dati noul nume al clientului:')
            prenume = input('Dati noul prenume al clientului:')
            cnp = input('Dati noul cnp al  clientului:')
            data_nasterii = input('Dati noua data nasterii a  clientului:')
            data_inregistrarii = input('Dati noua data inregistrarii')
            self.card_client_service.update_card_client(id_card_client,
                                                        nume,
                                                        prenume,
                                                        cnp,
                                                        data_nasterii,
                                                        data_inregistrarii)
        except ValueError as ve:
            print('Eroare de validare:', ve)
        except KeyError as ke:
            print('Eroare de ID:', ke)
        except Exception as ex:
            print('Eroare:', ex)

    def handle_stergere_card_client(self):
        try:
            id_card_client = input('Dati id-ul cardului care se sterge:')
            self.card_client_service.stergere_card_client(id_card_client)
        except ValueError as ve:
            print('Eroare de validare:', ve)
        except KeyError as ke:
            print('Eroare de ID:', ke)
        except Exception as ex:
            print('Eroare:', ex)

    def handle_update_tranzactie(self):
        try:
            id_tranzactie = input('Dati id-ul tranzactiei')
            id_masina = input('Dati id-ul masinii')
            id_card_client = input('Dati id-ul cardului:')
            suma_piese = input('Dati noua suma pieselor:')
            suma_manopera = input('Dati noua suma manoperelor:')
            data = input('Dati noua data a tranzactiei:')
            ora = input('Dati noua ora a tranzactiei:')
            self.tranzactie_service.update_tranzactie(id_tranzactie,
                                                      id_masina,
                                                      id_card_client,
                                                      suma_piese,
                                                      suma_manopera,
                                                      data,
                                                      ora)
        except ValueError as ve:
            print('Eroare de validare:', ve)
        except KeyError as ke:
            print('Eroare de ID:', ke)
        except Exception as ex:
            print('Eroare:', ex)

    def handle_stergere_tranzactie(self):
        try:
            id_tranzactie = input('Dati id-ul tranzactiei care se sterge')
            self.tranzactie_service.stergere_tranzactie(id_tranzactie)
        except ValueError as ve:
            print('Eroare de validare:', ve)
        except KeyError as ke:
            print('Eroare de ID:', ke)
        except Exception as ex:
            print('Eroare:', ex)

    def handle_get_interval(self):
        capat_stanga = float(input('Dati capatul din stanga al intervalului:'))
        capat_dreapta = float(input('Dati capatul drept al intervalului:'))
        result = self.tranzactie_service.get_interval(capat_stanga,
                                                      capat_dreapta)
        for elem in result:
            print(elem)

    def handle_random_cars(self):
        n = int(input('Dati numarul de masini care se genereaza'))
        self.masina_service.random_cars(n)

    def handle_stergere_tranzactie_interval(self):
        befor = input('dati prima data')
        after = input('dati a doua data')
        self.tranzactie_service.stergere_tranzactii_interval(befor, after)

    def handle_actualizare_masina(self):
        self.masina_service.actualizare_garantie()

    def handle_cautare_full_text(self):
        cautare_txt = CautareText(self.masina_service,
                                  self.card_client_service)
        text = input('Dati textul care se cauta')
        result = cautare_txt.cautare_full_text(text)
        for i in result:
            print(i)
