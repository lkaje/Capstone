from flask import Flask, request, jsonify
import os
import gensim
import re

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


def subjective_words(txt):
    masc = ['active', 'adventurous', 'aggress', 'ambitio', 'analy', 'assert', 'athlet', 'autonom', 'boast', 'challeng', 'compet', 'confident', 'courag', 'decide', 'decisive', 'decision', 'determin', 'force', 'greedy', 'headstrong', 'hierarch', 'hostil', 'impulsive', 'independen', 'individual', 'intellect', 'lead', 'logic', 'masculine', 'objective', 'opinion', 'outspoken', 'persist', 'principle', 'reckless', 'stubborn', 'superior', 'self-confiden', 'self-sufficien', 'self-relian', 'dominate', 'dominates', 'dominated', 'dominating']
    suggestions = []
    for word in masc:
        if word in txt:
            temp = (word, [])
            for similar_word in model.most_similar(word):
                if similar_word[0] not in masc:
                    temp[1].append(similar_word[0])
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
