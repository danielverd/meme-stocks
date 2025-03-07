import pandas as pd
import json

def createRTlist(tweetsDF,outpath):

    retweetedIDs = []
    userIDs = []
    timestamps = []

    for index,row in tweetsDF.iterrows():
        test_string = tweetsDF.iloc[index].referenced_tweets

        if pd.isna(test_string):
            print('out')
            continue

        if 'author_id' in test_string:
            continue
        if '},' in test_string:
            continue

        test_string = test_string.strip('[').strip(']')
        print(test_string)

        res = json.loads(test_string)
        print(res)

        if 'retweeted' not in res['type']:
            continue

        retweetedIDs.append(res['id'])
        userIDs.append(str(row['author.id']))
        timestamps.append(row['created_at'])

    out = pd.DataFrame({'retweeted_id':retweetedIDs, 'user_id':userIDs,'timestamp':timestamps})
    out.to_csv(outpath)


if __name__ == '__main__':
    ##replace xyz with the symbol of the stock being analyzed
    tweetsDF = pd.read_csv('xyz-tweets.csv',dtype=str)

    createRTlist(tweetsDF,'xyz-rts.csv')