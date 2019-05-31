import pickle

import networkx as nx

import cn_project.congressman as cm
import cn_project.parties as parties
import cn_project.proposition as propostions
import cn_project.voting as voting

refresh_data = False

if(refresh_data):
    #Refreshing parties
    ps = parties.Party.get_all_parties()
    ps_dic = {}
    for p in ps:
        ps_dic[p.id] = p

    parties_pickle = open('cn_project/data/parties.pickle', 'wb')
    pickle.dump(ps_dic, parties_pickle)
    parties_pickle.close()

    #Refreshing propositions
    props = propostions.Proposition.get_all_propositions(1991, 2020)
    props_pickle = open('cn_project/data/propositions.pickle', 'wb')
    pickle.dump(props, props_pickle)
    props_pickle.close()

    #Refreshing votings
    vote_pickle = open('cn_project/data/votes.pickle', 'wb')
    congressman_to_check = {}
    votes = {}
    try:
        count = 1
        for proposition in props.keys():
            print(f'Getting votes for proposition {proposition} ({count}/{len(props.keys())})')
            v = voting.Voting.get_votes(props[proposition].number, props[proposition].type, props[proposition].year)
            for check in v:
                for c in check.congressmen_votes.keys():
                    if check.congressmen_votes[c].id_congressman not in congressman_to_check.keys():
                        congressman_to_check[c] = check.congressmen_votes[c]
            votes[proposition] = v

            count += 1
    finally:
        pickle.dump(votes, vote_pickle)
        vote_pickle.close()

    #Refreshing congressman details
    congressmen = {}
    count = 1
    for c_id in congressman_to_check.keys():
        print(f'Getting info for congressman id {c_id} ({count}/{len(congressman_to_check)})')
        congressman = cm.Congressman(c_id, c_id.isdigit())
        
        if (congressman.full_name == None or congressman.full_name == ''):
            print('Using info from voting')
            congressman.cod_state_repr = congressman_to_check[c_id].state
            congressman.full_name = congressman_to_check[c_id].name
            congressman.display_name = congressman_to_check[c_id].name
            congressman.id_current_party = congressman_to_check[c_id].party

        congressmen[c_id] = congressman
        count += 1

    congressmen_pickle = open('cn_project/data/congressmen.pickle', 'wb')
    pickle.dump(congressmen, congressmen_pickle)
    congressmen_pickle.close()
else:    
    parties_pickle = open("cn_project/data/parties.pickle","rb")
    ps = pickle.load(parties_pickle)

    props_pickle = open("cn_project/data/propositions.pickle","rb")
    props = pickle.load(props_pickle)

    vote_pickle = open("cn_project/data/votes.pickle","rb")
    vs = pickle.load(vote_pickle)

    congressman_pickle = open("cn_project/data/congressmen.pickle","rb")
    cms = pickle.load(congressman_pickle)

    g = nx.Graph()

    for prop in vs:
        for v in vs[prop]:
            cmv_votes = {}
            for cmv in v.congressmen_votes:
                if cmv not in cms:
                    continue

                vote = v.congressmen_votes[cmv].vote.lower()
                if vote not in cmv_votes:
                    cmv_votes[vote] = []
                
                cmv_votes[vote].append(v.congressmen_votes[cmv].id_congressman)
            
            for cmv_key in cmv_votes.keys():
                cmsv = cmv_votes[cmv_key]
                for i in range(0, len(cmsv)):
                    congressman1 = cms[cmsv[i]]
                    if (not g.has_node(congressman1)):
                        g.add_node(congressman1)
                    for j in range(i+1, len(cmsv)):
                        congressman2 = cms[cmsv[j]]

                        #just in case ...
                        if(congressman1 == congressman2):
                            continue

                        if (not g.has_node(congressman2)):
                            g.add_node(congressman2)
                        
                        if g.has_edge(congressman1, congressman2):
                            g[congressman1][congressman2]['weight'] += 1
                        else:
                            g.add_edge(congressman1, congressman2, weight=1)

nx.write_pajek(g, 'cn_project/data/voting_relation_brazil.net')
print('finished')

#congressman = cm.Congressman(160554)

#print(p.__len__)
