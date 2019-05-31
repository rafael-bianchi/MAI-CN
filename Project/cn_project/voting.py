from cn_project.utils import get_content
import datetime
from lxml import etree
import re
import string

#Constants
API_LIST_VOTES = "https://www.camara.leg.br/SitCamaraWS/Proposicoes.asmx/ObterVotacaoProposicao?tipo="#PL&numero=1992&ano=2007"

class Voting:
    def __init__(self, session_id, id_proposition, summary, obj_voting, voting_date, voting_time, type, year, party_orientation, congressmen_votes):
        self.session_id = session_id
        self.id_proposition = id_proposition
        self.summary = summary
        self.obj_voting = obj_voting
        self.voting_date = voting_date
        self.voting_time = voting_time
        self.type = type
        self.year = year
        self.party_orientation = party_orientation
        self.congressmen_votes = congressmen_votes
        self.last_updated = datetime.datetime.now()

    def __hash__(self):
        return hash((self.id, self.type, self.year, self.session_id))

    def __eq__(self,other):
        return self.id == other.id and self.type == other.type and other.year == other.year and other.session_id == self.session_id

    @staticmethod
    def get_votes(number, type, year):
        content = get_content(f'{API_LIST_VOTES}{type}&numero={number}&ano={year}')
        
        votings = []

        if (len(content) < 1):
            return votings

        for element in content.iter("Votacoes"):
            participant_congressman = set()
            for voting in content.iter("Votacao"):
                session_id = None 
                summary = None
                obj_voting = None
                voting_date = None
                voting_time = None
                party_orientation = {}
                congressmen_votes = {}

                summary = voting.attrib['Resumo'].rstrip()
                voting_date = None if voting.attrib['Data'].rstrip() == None or voting.attrib['Data'].rstrip() == '' else datetime.datetime.strptime(voting.attrib['Data'].rstrip(), '%d/%m/%Y')
                voting_time = voting.attrib['Hora'].rstrip()
                obj_voting = voting.attrib['ObjVotacao'].rstrip()
                session_id = voting.attrib['codSessao'].rstrip()

                for node in voting:
                    if node.tag == 'orientacaoBancada':
                        for orientation in node:
                            party_cod = orientation.attrib['Sigla'].rstrip()
                            vote_orientation = orientation.attrib['orientacao'].rstrip()
                            if (party_cod != party_cod.upper()):
                                party_cod = party_cod.translate(str.maketrans('', '', string.punctuation))
                                for p_cod in re.findall('^[a-z]+|[A-Z][^A-Z]*', party_cod):
                                    party_orientation[p_cod] = vote_orientation
                            else:
                                party_orientation[party_cod] = vote_orientation
                   
                    if node.tag == 'votos':
                        for cman_vote in node:
                            vote = cman_vote.attrib['Voto'].rstrip()
                            id_congressman = cman_vote.attrib['ideCadastro'].rstrip()
                            name = cman_vote.attrib['Nome'].rstrip()
                            party = cman_vote.attrib['Partido'].rstrip()
                            state = cman_vote.attrib['UF'].rstrip()

                            if(id_congressman == ''):
                                print(f'Could not find congressman id ({name}) for number {number} year {year} type {type} and session {session_id}')
                                id_congressman = name

                            c = CongressMenVote(number, id_congressman, vote, name, party, state)
                            congressmen_votes[id_congressman] = c

                v = Voting(session_id, number, summary, obj_voting, voting_date, voting_time, type, year, party_orientation, congressmen_votes)
                v.participant_congressman = participant_congressman

                votings.append(v)
        
        return votings 



# class PartyOrientation:
#     def __init__(self, id_proposition, party_cod, orientation):
#         self.id_proposition = id_proposition
#         self.party_cod = party_cod
#         self.orientation = orientation
#         self.last_updated = datetime.datetime.now()

#     def __hash__(self):
#         return hash((self.id_proposition, self.party_cod, self.orientation))

#     def __eq__(self,other):
#         return self.id_proposition == other.id_proposition and self.party_cod == other.party_cod

class CongressMenVote:
    def __init__(self, id_proposition, id_congressman, vote, name, party, state):
        self.id_proposition = id_proposition
        self.id_congressman = id_congressman
        self.vote = vote
        self.name = name
        self.party = party
        self.state = state
        self.last_updated = datetime.datetime.now()

    def __hash__(self):
        return hash((self.id_proposition, self.id_congressman, self.name, self.vote))

    def __eq__(self,other):
        return self.id_proposition == other.id_proposition and self.id_congressman == other.id_congressman and self.name == self.name







#New api
# API_ROOT_URL = 'https://dadosabertos.camara.leg.br/api/v2/'
# PARAM_ALL_LEGISTATURAS = '56,55,54,53,52,51,50,49,48,47,46,45,44,43,42,41,40,39,38,37,36,35,34,33,32,31,30,29,28,27,26,25,24,23,22,21,20,19,18,17,16,15,14,13,12,11,10,9,8,7,6,5,4,3,2,1'
# QUERY_ALL_PARTIES = f'{API_ROOT_URL}partidos?idLegislatura={PARAM_ALL_LEGISTATURAS}&itens=10000&ordem=ASC&ordenarPor=sigla'