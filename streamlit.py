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
    rm_punc = re.sub(r'[^\w\s]', ' ', user_input) #remove punctuation and replace it with a space
    txt_list = rm_punc.split() #split on the white space
    for word in txt_list: #for each word in the user input
        for fragment in masc: #and for each fragment/word in the list of subjectively masculine words
            if fragment in word: #if the word contains a fragment
                return annotated_text((word, '', '#faa'))






if st.button('Review'):
    col1, col2 = st.beta_columns(2)

    with col1:
        st.header('Input')
        st.write(user_input, use_column_width=True)

    with col2:
        st.header('Recommendations')
        st.write('is this thing working', use_column_width=True)
