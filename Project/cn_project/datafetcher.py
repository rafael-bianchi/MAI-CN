import pickle

import cn_project.congressman as cm
import cn_project.parties as parties
import cn_project.proposition as propostions
import cn_project.voting as voting
import networkx as nx

def refresh_data():
    #States & positions dic
    StateDict={
                "AC": ( -8.77, -70.55)
                , "AL": ( -9.71, -35.73)
                , "AM": ( -3.07, -61.66)
                , "AP": (  1.41, -51.77)
                , "BA": (-12.96, -38.51)
                , "CE": ( -3.71, -38.54)
                , "DF": (-15.83, -47.86)
                , "ES": (-19.19, -40.34)
                , "GO": (-16.64, -49.31)
                , "MA": ( -2.55, -44.30)
                , "MT": (-12.64, -55.42)
                , "MS": (-20.51, -54.54)
                , "MG": (-18.10, -44.38)
                , "PA": ( -5.53, -52.29)
                , "PB": ( -7.06, -35.55)
                , "PR": (-24.89, -51.55)
                , "PE": ( -8.28, -35.07)
                , "PI": ( -8.28, -43.68)
                , "RJ": (-22.84, -43.15)
                , "RN": ( -5.22, -36.52)
                , "RO": (-11.22, -62.80)
                , "RS": (-30.01, -51.22)
                , "RR": (  1.89, -61.22)
                , "SC": (-27.33, -49.44)
                , "SE": (-10.90, -37.07)
                , "SP": (-23.55, -46.64)
                , "TO": (-10.25, -48.25)
    }

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

    g_congressmen = nx.Graph()
    g_parties = nx.Graph()
    g_states = nx.Graph()

    prop_count = 1
    for prop in votes:
        print(f'Starting proposition {prop} ({prop_count}/{len(votes)})')
        for v in votes[prop]:
            cmv_votes = {}
            
            for cmv in v.congressmen_votes:
                if cmv not in congressmen:
                    continue

                vote = v.congressmen_votes[cmv].vote.lower()

                if vote not in cmv_votes:
                    cmv_votes[vote] = []
                
                cmv_votes[vote].append(v.congressmen_votes[cmv])

            for cmv_key in cmv_votes.keys():
                cmsv = cmv_votes[cmv_key]
                for i in range(0, len(cmsv)):
                    congressman1 = congressmen[cmsv[i].id_congressman]
                    party1 = cmsv[i].party.upper()
                    state1 = cmsv[i].state.upper()
                    
                    pos1 = StateDict[congressman1.cod_state_repr.upper()]
                    
                    if (not g_congressmen.has_node(congressman1.display_name)):
                        g_congressmen.add_node(congressman1.display_name, x = pos1[0], y = pos1[1])
                    
                    if (not g_parties.has_node(party1)):
                        g_parties.add_node(party1)

                    if (not g_states.has_node(state1)):
                        g_states.add_node(state1, x = StateDict[state1][0], y = StateDict[state1][1])

                    for j in range(i+1, len(cmsv)):
                        congressman2 = congressmen[cmsv[j].id_congressman]
                        party2 = cmsv[j].party.upper()
                        state2 = cmsv[j].state.upper()

                        #just in case ...
                        if(congressman1 == congressman2):
                            continue

                        #Congressmen vote
                        if (not g_congressmen.has_node(congressman2.display_name)):
                            pos2 = StateDict[congressman1.cod_state_repr.upper()]
                            g_congressmen.add_node(congressman2.display_name, x = pos2[0], y = pos2[1])
                        
                        if g_congressmen.has_edge(congressman1.display_name, congressman2.display_name):
                            g_congressmen[congressman1.display_name][congressman2.display_name]['weight'] += 1
                        else:
                            g_congressmen.add_edge(congressman1.display_name, congressman2.display_name, weight=1)

                        #Party vote
                        if (party1 != party2):
                            if (not g_parties.has_node(party2)):
                                g_parties.add_node(party2)
                            
                            if g_parties.has_edge(party1, party2):
                                g_parties[party1][party2]['weight'] += 1
                            else:
                                g_parties.add_edge(party1, party2, weight = 1)
                        
                        #State vote
                        if (state1 != state2):
                            if (not g_states.has_node(state2)):
                                g_states.add_node(state2, x = StateDict[state2][0], y = StateDict[state2][1])
                            
                            if g_states.has_edge(state1, state2):
                                g_states[state1][state2]['weight'] += 1
                            else:
                                g_states.add_edge(state1, state2, weight=1)
            session_count += 1
        prop_count += 1

    nx.write_pajek(g_congressmen, 'cn_project/data/voting_relation_congressmen.net')
    nx.write_pajek(g_parties, 'cn_project/data/g_parties.net')
    nx.write_pajek(g_states, 'cn_project/data/g_states.net')
    print('finished')
