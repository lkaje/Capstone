import streamlit as st
from annotated_text import annotated_text
import re
import streamlit.components.v1 as components
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import wordnet as wn
from subject_sim_model import model

#model = None
#print('creating model')
#if __name__ == '__main__':
#    model = gensim.models.KeyedVectors.load_word2vec_format('./lexvec.enwiki+newscrawl.300d.W.pos.vectors')
#print('model created')

masc = ['active', 'adventurous', 'aggress', 'ambitio', 'analy', 'assert', 'athlet', 'autonom',
'boast', 'challeng', 'compet', 'confident', 'courag', 'dominant', 'domina', 'decide', 'decisive', 'decision',
'determin', 'force', 'greedy', 'headstrong', 'hierarch', 'hostil', 'impulsive',
'independen', 'individual', 'intellect', 'lead', 'logic', 'masculine', 'objective', 'opinion', 'outspoken',
'persist', 'principle', 'reckless', 'stubborn', 'superior', 'self-confiden', 'self-sufficien', 'self-relian']



def most_similar_subjective(txt):
    rm_punc = re.sub(r'[^\w\s]', ' ', txt)
    txt_list = rm_punc.split()
    suggestions = []
    for word in txt_list:
        for fragment in masc:
            if fragment in word:
                temp = (word, [])
                for similar_word in model.most_similar(word):
                    if fragment not in similar_word[0]:
                        temp[1].append(similar_word[0])
                suggestions.append(temp)
    return suggestions

def hyper_hypo_nyms(txt):
    rm_punc = re.sub(r'[^\w\s]', ' ', txt)
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
                        for hyponym in wn.synset(sinset.name()).hyponyms():
                            if fragment not in hyponym.name().split('.')[0]:
                                temp[1].append(hyponym.name().split('.')[0])
                    suggestions.append(temp)
    return suggestions



def combine_results(txt):
    similar_results = most_similar_subjective(txt)
    hyper_hypo_results = hyper_hypo_nyms(txt)
    combined = []
    for result in similar_results:
        full_list = result[1]
        for h_result in hyper_hypo_results:
            if result[0] == h_result[0]:
                for new_result in h_result[1]:
                    if new_result not in full_list:
                        full_list.append(new_result)
                temp = (result[0], full_list)
        combined.append(temp)
    return [word for words, word in enumerate(combined) if word not in combined[:words]]

def output_dict(input_results):
    return_dict = {}
    for each_tuple in input_results:
        return_dict[each_tuple[0]] = each_tuple[1]
    return return_dict






def highlight(user_input):
    rm_punc = re.sub(r'[^\w\s]', ' ', user_input)
    txt_list = rm_punc.split()
    working_list = []
    for word in txt_list:
        frag_found = False
        for fragment in masc:
            if fragment in word:
                frag_found = True
        if frag_found == True:
            working_list.append((word, "", "#faa"))
        else:
            working_list.append(word+' ')
    return tuple(working_list)


st.title("recommend{her}")
st.subheader("a tool to identify and adjust gendered language in job descriptions")
user_input = st.text_area("Job Description", value='', height = 300)

highlighted = highlight(user_input)

for_dict_transformation = combine_results(user_input)
for_widget = output_dict(for_dict_transformation)

if st.button('Review'):
    col1, col2 = st.beta_columns(2)

    with col1:
        st.header('Input')
        annotated_text(*highlighted)

    with col2:
        st.header('Recommendations')
        st.write(for_widget)
