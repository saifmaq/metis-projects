import pandas as pd
import pickle
import numpy as np
import random

p4k = pickle.load( (open('pitchfork_data.p', 'rb')))


good_music = p4k[p4k['score'] > (p4k['score'].mean() + 1)]

def cool_music(artist):
    d = p4k[p4k['artist']==artist]['topic']
    topics = list(d[:].unique())
    subtopics = []
    for topic in topics:
        d2 = p4k[(p4k['topic'] == topic) & (p4k.artist == artist)]
        lists = list(d2['subtopic'][:].unique())
        for l in lists:
            subtopics.append(l)
    recs = []
    ids = []
    for subtopic in subtopics:
        subtopic_suggestions = good_music[(good_music['subtopic'] == subtopic) & 
                                      (good_music['artist'] != artist)]
        for _ in range(10):
            ids.append(random.choice(list(subtopic_suggestions.reviewid)))
    
    ids = list(set(ids))
    rids = list(np.random.choice(ids, size=14))
    rids = list(set(rids))
    for i in rids:
        p_title = list(p4k[p4k.reviewid == i]['title'])
        p_artist = list(p4k[p4k.reviewid == i]['artist'])        
        rec = list(zip(p_title, p_artist))
        recs.append(rec)
    clean_recs = ''
    for r in recs:
        for l in r:
            l = list(l)
            clean_recs += l[0] + ' - ' + l[1] + '<br>' 
    return clean_recs
    
    
    
        
        
        
        
        
        
    

    