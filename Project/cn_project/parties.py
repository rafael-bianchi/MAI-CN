from cn_project.utils import get_content
import datetime

#Constants
API_PARTIES = "https://www.camara.leg.br/SitCamaraWS/Deputados.asmx/ObterPartidosCD"

class Party:
    def __init__(self, id, cod, name, creation, ended):
        self.id = id
        self.cod = cod
        self.name = name
        self.creation = None if creation == None or creation == '' else datetime.datetime.strptime(creation, '%d/%m/%Y')
        self.ended = None if ended == None or ended == '' else datetime.datetime.strptime(ended, '%d/%m/%Y')
        self.last_updated = datetime.datetime.now()

    def __hash__(self):
        return hash((self.id, self.cod, self.name))

    def __eq__(self,other):
        return self.id == other.id and self.cod == other.cod

    @staticmethod
    def get_all_parties():
        parties =[]
        content = get_content(API_PARTIES)

        for party in content:
            id = None
            cod = None
            name = None
            creation = None
            ended = None

            for elem in party:
                if (elem.tag == 'idPartido'):
                    id = elem.text.rstrip()
                elif(elem.tag == 'siglaPartido'):
                    cod = elem.text.rstrip()
                elif(elem.tag == 'nomePartido'):
                    name = elem.text.rstrip()
                elif(elem.tag == 'dataCriacao'):
                    creation = elem.text.rstrip()
                elif(elem.tag == 'dataExtincao'):
                    ended = elem.text.rstrip()

            p = Party(id, cod, name, creation, ended)

            parties.append(p)

        return parties









#New api
# API_ROOT_URL = 'https://dadosabertos.camara.leg.br/api/v2/'
# PARAM_ALL_LEGISTATURAS = '56,55,54,53,52,51,50,49,48,47,46,45,44,43,42,41,40,39,38,37,36,35,34,33,32,31,30,29,28,27,26,25,24,23,22,21,20,19,18,17,16,15,14,13,12,11,10,9,8,7,6,5,4,3,2,1'
# QUERY_ALL_PARTIES = f'{API_ROOT_URL}partidos?idLegislatura={PARAM_ALL_LEGISTATURAS}&itens=10000&ordem=ASC&ordenarPor=sigla'