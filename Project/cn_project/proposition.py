from cn_project.utils import get_content
import datetime

#Constants
API_LIST_PROPOSITIONS = "https://www.camara.leg.br/SitCamaraWS/Proposicoes.asmx/ListarProposicoesVotadasEmPlenario?ano="
API_PROPOSITION_DETAILS = "https://www.camara.leg.br/SitCamaraWS/Proposicoes.asmx/ObterProposicaoPorID?IdProp="

class Proposition:
    def __init__(self, id, name, year, p_type, p_number, voting_date):
        self.id = id
        self.name = name
        self.year = year
        self.voting_date = None if voting_date == None or voting_date == '' else datetime.datetime.strptime(voting_date, '%d/%m/%Y')
        self.type = p_type
        self.number = p_number
        self.last_updated = datetime.datetime.now()

    def __hash__(self):
        return hash((self.id, self.name))

    def __eq__(self,other):
        return self.id == other.id

    @staticmethod
    def get_all_propositions(year_start = 1991, year_end = 2020):
        propositions = {}

        for year in range(year_start, year_end):
            print(f'Getting propositions for year {year}')
            content = get_content(f'{API_LIST_PROPOSITIONS}{year}&tipo=')

            print(f'Returned {len(content)} propositions.')
            prop_count = 0
            for party in content:
                p_id = None
                name = None
                voting_date = None
                p_type = None
                p_year = None
                p_number = None

                for elem in party:
                    if (elem.tag == 'codProposicao'):
                        p_id = elem.text.rstrip()
                    elif(elem.tag == 'dataVotacao'):
                        voting_date = elem.text.rstrip()
                    elif(elem.tag == 'nomeProposicao'):
                        name = elem.text.rstrip()

                prop_count += 1
                if(p_id in propositions):
                    continue

                print(f'Getting details for prop n# {prop_count}')
                contentProp = get_content(f'{API_PROPOSITION_DETAILS}{p_id}')
                
                if(len(list(contentProp)) == 1):
                    print('Type of proposition {p_id} not found.')
                else:
                    p_type = contentProp.attrib['tipo'].rstrip()
                    p_year = contentProp.attrib['ano'].rstrip()
                    p_number =contentProp.attrib['numero'].rstrip()

                p = Proposition(p_id, name, p_year, p_type, p_number, voting_date)

                propositions[p_id] = p
        return propositions









#New api
# API_ROOT_URL = 'https://dadosabertos.camara.leg.br/api/v2/'
# PARAM_ALL_LEGISTATURAS = '56,55,54,53,52,51,50,49,48,47,46,45,44,43,42,41,40,39,38,37,36,35,34,33,32,31,30,29,28,27,26,25,24,23,22,21,20,19,18,17,16,15,14,13,12,11,10,9,8,7,6,5,4,3,2,1'
# QUERY_ALL_PARTIES = f'{API_ROOT_URL}partidos?idLegislatura={PARAM_ALL_LEGISTATURAS}&itens=10000&ordem=ASC&ordenarPor=sigla'