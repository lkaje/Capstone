from flask import Flask, request, jsonify
import os
import gensim
import re
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import wordnet as wn

print('creating model')
model = gensim.models.KeyedVectors.load_word2vec_format('./lexvec.enwiki+newscrawl.300d.W.pos.vectors')
print('model created')
app = Flask(__name__)


def validate_key(provided_key):
    if provided_key == None:
        print('Key Not Found')
        return False
    if provided_key == os.environ.get('API_KEY'):
        return True
    else:
        print('Key Incorrect')
        return False



masc = ['active', 'adventurous', 'aggress', 'ambitio', 'analy', 'assert', 'athlet', 'autonom', 'boast', 'challeng', 'compet', 'confident', 'courag', 'decide', 'decisive', 'decision', 'determin', 'force', 'greedy', 'headstrong', 'hierarch', 'hostil', 'impulsive', 'independen', 'individual', 'intellect', 'lead', 'logic', 'masculine', 'objective', 'opinion', 'outspoken', 'persist', 'principle', 'reckless', 'stubborn', 'superior', 'self-confiden', 'self-sufficien', 'self-relian', 'dominate', 'dominates', 'dominated', 'dominating']


def most_similar_subjective(txt):
    suggestions = []
    for word in masc:
        if word in txt:
            temp = (word, [])
            for similar_word in model.most_similar(word):
                if similar_word[0] not in masc:
                    temp[1].append(similar_word[0])
            suggestions.append(temp)
    return suggestions



def hypernyms_subjective(txt):
    rm_punc = re.sub(r'[^\w\s]', '', txt)
    suggestions = []
    dictionary = {}
    tokenized = sent_tokenize(rm_punc)
    for words in tokenized:
        word_lst = nltk.word_tokenize(words)
        tagged = nltk.pos_tag(word_lst)
    for item in tagged:
        for fragment in masc:
            if fragment in item[0]:
                temp = (item[0], [])
                dictionary[item[0]] = item[1]
                if dictionary[item[0]].startswith('N'):
                     pos = 'n'
                elif dictionary[item[0]].startswith('J'):
                    pos = 'a'
                elif dictionary[item[0]].startswith('R'):
                     pos = 'r'
                elif dictionary[item[0]].startswith('V'):
                    pos = 'v'
                for sinset in wn.synsets(item[0], pos):
                    for hypernym in wn.synset(sinset.name()).hypernyms():
                        if fragment not in hypernym.name().split('.')[0]:
                            temp[1].append(hypernym.name().split('.')[0])
                suggestions.append(temp)
    return suggestions



def hyponyms_subjective(txt):
    rm_punc = re.sub(r'[^\w\s]', '', txt)
    suggestions = []
    dictionary = {}
    tokenized = sent_tokenize(rm_punc)
    for words in tokenized:
        word_lst = nltk.word_tokenize(words)
        tagged = nltk.pos_tag(word_lst)
    for item in tagged:
        for fragment in masc:
            if fragment in item[0]:
                temp = (item[0], [])
                dictionary[item[0]] = item[1]
                if dictionary[item[0]].startswith('N'):
                     pos = 'n'
                elif dictionary[item[0]].startswith('J'):
                    pos = 'a'
                elif dictionary[item[0]].startswith('R'):
                     pos = 'r'
                elif dictionary[item[0]].startswith('V'):
                    pos = 'v'
                for sinset in wn.synsets(item[0], pos):
                    for hyponym in wn.synset(sinset.name()).hyponyms():
                        if fragment not in hyponym.name().split('.')[0]:
                            temp[1].append(hyponym.name().split('.')[0])
                suggestions.append(temp)
    return suggestions

@app.route("/")
def get():
    provided_key = request.args.get('apiKey')
    if validate_key(provided_key):
        input = request.json
        results = subjective_words(input['descript'])
        return jsonify(results)
    else:
        return 'API Key Missing/Invalid'
