import pandas as pd
import networkx as nx
import numpy as np

def retweetsByDate(retweetsDF,days,volumesDF):

    tweetsDF = pd.read_csv('pltr-tweets-emotion.csv',dtype={'id': str, 'author.id':str}) ##
    
    for index, row in retweetsDF.iterrows():
        print('index',index)
        temp = row['timestamp']
        temp = temp.split('T')[0]
        retweetsDF.at[index,'timestamp'] = temp

    data = []

    print(len(days))

    flag = 0
    for day in days:
        if flag > 75:
            break
        todaysGraph = retweetsDF[retweetsDF['timestamp'] == day]
        todaysGraph = todaysGraph.reset_index()

        todaysVolume = volumesDF[volumesDF['Date'] == day]
        todaysVolume = todaysVolume.reset_index()
        print(todaysVolume['Volume'][0])
        print(todaysVolume['Close'][0] - todaysVolume['Open'][0])

        todayG = nx.DiGraph()

        angers = []
        disgusts = []
        fears = []
        joys = []
        sadnesses = []
        surprises = []
        for i in todaysGraph.index:
            print(i)
            tweet = tweetsDF.loc[tweetsDF['id'] == todaysGraph['retweeted_id'][i]]

            if tweet.empty:
                continue
            source = tweet['author.id'].iloc[0] #source is the user who posted the tweet
            target = todaysGraph['user_id'][i] #target is the user who retweeted the tweet
            print(source,'whee',target)

            angers.append(tweet['anger'].iloc[0])
            disgusts.append(tweet['disgust'].iloc[0])
            fears.append(tweet['fear'].iloc[0])
            joys.append(tweet['joy'].iloc[0])
            sadnesses.append(tweet['sadness'].iloc[0])
            surprises.append(tweet['surprise'].iloc[0])

            if todayG.has_edge(source,target):
                todayG[source][target]['weight'] = todayG[source][target]['weight'] + 1
            else:
                todayG.add_weighted_edges_from([(source,target,1)])
        
        Gcc = sorted(nx.weakly_connected_components(todayG), key=len, reverse=True)
        digraphTCC = todayG.subgraph(Gcc[0])
        print(todayG.size(),digraphTCC.size())

        nx.readwrite.write_edgelist(digraphTCC,'PLTR'+str(flag)+'edgelist.csv',delimiter=',',data=['weight'])

        headers = ['date','size','edges','diameter','clustering','core_percent','anger','disgust','fear','joy','sadness','surprise','volume','daychange']

        centralities = []

        #date,size,edges
        centralities.append(todaysGraph['timestamp'][0])
        centralities.append(todayG.order())
        centralities.append(todayG.size())

        #avgdeg,diameter,mincut
        #avgdegree = nx.degree_assortativity_coefficient(todayG)
        #centralities.append(avgdegree)
        centralities.append(nx.diameter(digraphTCC.to_undirected()))

        #clustering,transitivity
        centralities.append(nx.algorithms.cluster.average_clustering(todayG,weight='weight'))

        '''
        removes = []
        for node in digraphTCC.nodes():
            if (digraphTCC.in_degree(node) < 2) and (digraphTCC.out_degree(node) == 0):
                removes.append(node)
        higraphHCC = digraphTCC.copy()
        higraphHCC.remove_nodes_from(removes)
        two = nx.node_connectivity(higraphHCC)
        print(two)
        centralities.append(two)
        '''

        #core_percent
        newTG = todayG.copy()
        newTG.remove_edges_from(nx.selfloop_edges(newTG))
        cores = nx.k_core(newTG).nodes
        boundary = list(nx.edge_boundary(newTG,cores))
        centralities.append(len(boundary)/todayG.size())

        #emotions
        centralities.append(sum(angers) / len(angers))
        centralities.append(sum(disgusts) / len(disgusts))
        centralities.append(sum(fears) / len(fears))
        centralities.append(sum(joys) / len(joys))
        centralities.append(sum(sadnesses) / len(sadnesses))
        centralities.append(sum(surprises) / len(surprises))

        #volume,daychange
        centralities.append(todaysVolume['Volume'][0])
        centralities.append(todaysVolume['Close'][0] - todaysVolume['Open'][0])
   
        data.append(centralities)
        flag += 1

    return pd.DataFrame(data, columns=headers)    


if __name__ == '__main__':
    from datetime import datetime
    startTime = datetime.now()

    retweetsDF = pd.read_csv('pltr-rts-01-07.csv',dtype=str) ##
    
    volumesDF = pd.read_csv('PLTR.csv') ##
    volumes = volumesDF['Volume']
    dayChanges = volumesDF['Close'] - volumesDF['Open']

    days = volumesDF['Date'].unique()

    xdata = retweetsByDate(retweetsDF,days,volumesDF)


    xdata.to_csv('pltrDF-kq2.csv') ##

    print(datetime.now() - startTime)

