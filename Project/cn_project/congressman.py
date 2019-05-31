from cn_project.utils import get_content
import datetime
from lxml import etree

API_CONGRESSMAN = "https://www.camara.leg.br/SitCamaraWS/Deputados.asmx/ObterDetalhesDeputado?ideCadastro="

class Congressman:
    def __init__(self, id, get_info = True):
        self.id = id
        self.id_legislature = None
        self.email = None
        self.occupation = None
        self.birth_date = None
        self.death_date = None
        self.cod_state_repr = None
        self.current_situation = None
        self.last_updated = datetime.datetime.now()
        self.id_deprecated = None
        self.full_name = None
        self.display_name = None
        self.gender = None
        #self.picture_url = None
        self.id_current_party = None
        self.party_history = None

        if (get_info):
            self.get_info()

    def __hash__(self):
        return hash((self.id, self.email))

    def __eq__(self,other):
        return self.id == other.id

    def get_info(self):
        if (self.id == ''):
            print (f'Invalid congressman id {self.id}')
            return

        content = get_content(f'{API_CONGRESSMAN}{self.id}&numLegislatura=')
        
        if (len(content) < 1):
            return

        for elem in content[0]:
            if (elem.tag == 'numLegislatura'):
                self.id_legislature = elem.text.rstrip()
            elif(elem.tag == 'email'):
                self.email = elem.text.rstrip()
            elif(elem.tag == 'nomeProfissao'):
                self.occupation = elem.text.rstrip()
            elif(elem.tag == 'dataNascimento'):
                self.birth_date = datetime.datetime.strptime( elem.text.rstrip(), '%d/%m/%Y')  
            elif(elem.tag == 'dataFalecimento'):
                date = elem.text.rstrip()
                self.death_date = None if date == None or date == '' else datetime.datetime.strptime(date, '%d/%m/%Y')
            elif(elem.tag == 'ufRepresentacaoAtual'):
                self.cod_state_repr = elem.text.rstrip()
            elif(elem.tag == 'situacaoNaLegislaturaAtual'):
                self.current_situation = elem.text.rstrip()
            elif(elem.tag == 'idParlamentarDeprecated'):
                self.id_deprecated = elem.text.rstrip()
            elif(elem.tag == 'nomeParlamentarAtual'):
                self.display_name = elem.text.rstrip()
            elif(elem.tag == 'nomeCivil'):
                self.full_name = elem.text.rstrip()
            elif(elem.tag == 'sexo'):
                self.gender = elem.text.rstrip()
            elif(elem.tag == 'partidoAtual'):
                for subelem in elem:
                    if(subelem.tag == 'idPartido'):
                        self.id_current_party = subelem.text.rstrip()
                        break
            elif(elem.tag == 'filiacoesPartidarias'):
                self.party_history = elem.values()
        
        self.last_updated =  datetime.datetime.now()














