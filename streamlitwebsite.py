import streamlit as st
from htbuilder import annotated_text
import re

masc = ['active', 'adventurous', 'aggress', 'ambitio', 'analy', 'assert', 'athlet', 'autonom',
'boast', 'challeng', 'compet', 'confident', 'courag', 'dominant', 'domina', 'decide', 'decisive', 'decision',
'determin', 'force', 'greedy', 'headstrong', 'hierarch', 'hostil', 'impulsive',
'independen', 'individual', 'intellect', 'lead', 'logic', 'masculine', 'objective', 'opinion', 'outspoken',
'persist', 'principle', 'reckless', 'stubborn', 'superior', 'self-confiden', 'self-sufficien', 'self-relian']

user_input = st.text_area("Job Description", value='')


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
            working_list.append((word, '', '#faa'))
        else:
            working_list.append(word)
    return tuple(working_list)


highlighted = highlight(user_input)
annotated_text(highlighted)

if st.button('Review'):
    col1, col2 = st.beta_columns(2)

    with col1:
        st.header('Input')
        st.write(annotated_text(highlighted), use_column_width=True)

    with col2:
        st.header('Recommendations')
        st(annotated_text( "This ", ("is", "verb", "#8ef"), " some ", ("annotated", "adj", "#faa"), ("text", "noun", "#afa"), " for those of ", ("you", "pronoun", "#fea"), " who ", ("like", "verb", "#8ef"), " this sort of ", ("thing", "noun", "#afa")), use_column_width=True)
