import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import numpy as np
import pandas as pd
import nltk
nltk.download('punkt') # one time execution
import re
import tensorflow as tf
import tensorflow_hub as hub
import json
from sklearn.metrics.pairwise import cosine_similarity
import networkx as nx

module_url = "https://tfhub.dev/google/universal-sentence-encoder-large/3"
embed = hub.Module(module_url)

def cons_clean_sentence (json_file):
    cons_list = []
    for x in json_file['cons'][0]:
        spec = x.split(",")
        cleaned = [x.strip() for x in spec]
        cons_list += cleaned
    cons_list2 = []
    for y in cons_list:
        if '.' in y:
            spec = y.split(".")
            cleaned = [x.strip() for x in spec]
            cons_list2 += cleaned
        else:
            cons_list2.append(y)
    return cons_list2

def pros_clean_sentence (json_file):
    pros_list = []
    for x in json_file['pros'][0]:
        spec = x.split(",")
        cleaned = [x.strip() for x in spec]
        pros_list += cleaned
    pros_list2 = []
    for y in pros_list:
        if '.' in y:
            spec = y.split(".")
            cleaned = [x.strip() for x in spec]
            pros_list2 += cleaned
        else:
            pros_list2.append(y)
    return pros_list2

def textrank(sentences, num_return = 5):
    with tf.Session() as session:
        session.run([tf.global_variables_initializer(), tf.tables_initializer()])
        message_embeddings = session.run(embed(sentences))
    sim_mat = np.zeros([len(sentences), len(sentences)])

    for i in range(len(sentences)):
        for j in range(len(sentences)):
            if i != j:
                sim_mat[i][j] = cosine_similarity(message_embeddings[i].reshape(1,512), message_embeddings[j].reshape(1,512))[0,0]

    nx_graph = nx.from_numpy_array(sim_mat)
    scores = nx.pagerank(nx_graph)
    ranked_sentences = sorted(((scores[i],s) for i,s in enumerate(sentences)), reverse=True)
    return_list = []
    for i in range(num_return):
        return_list.append(ranked_sentences[i][1])
    return return_list

def pros_cons(json_file, num_result):
    # with open("pros_cons.json", "r") as file:
    #     json_file = json.load(file)

    pros = pros_clean_sentence(json_file)
    cons = cons_clean_sentence(json_file)

    pros_list = textrank(pros,num_result)
    cons_list = textrank(cons,num_result)

    return {"pros":pros_list,"cons":cons_list}