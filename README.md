# recommend(her)

The majority of the tech industry is made up of men. Among the ‘Big Five’ (Amazon, Apple, Facebook, Google and Microsoft), only 34% of the workforce is women (Daly, 2020). Research has shown that when a job description contains subjectively masculine words, women are less likely to apply (Gaucher, 2011). Coupled with an analysis from Textio, an augmented writing platform, that shows that job descriptions in tech are not only likely to have a more masculine tone, but to have a significant more masculine tone. Gender diversity is one of the biggest issues the technology sector experiences, and making job descriptions more subconsciously inclusive is a great place to start. recommend(her) is a tool that aims to identify and flag subjectively gendered language, and provide alternative suggestions.  

To run the tool, download the project and the following file: https://drive.google.com/file/d/1rrSZJ1LpPpvsBl92XEAOpG7DIs-18hAf/view?usp=sharing. From there, pip install requirements.txt, and then open then project with the command streamlit run streamlitwebsite.py. The project will take a few minutes to get up and running.

I used three datasets for this project; a dataset of Indeed job postings, the lex.vec newscrawl corpus, and the NLTK WordNet corpus. The newscrawl and WordNet corpuses were used in the implementation of three different models to return the most similar words for each flagged words, and the hypernyms and hyponyms for each word. The Indeed job postings were utilized for testing of the models. The list of masculine coded words from Gaucher et al was used as the masculine coded words for the functions.  

Because all of the models used were black box models, it is difficult to know exactly how well the models are performing. For the NLTK function, part of speech was specified and tagged for better results; ie if the flagged word was ‘challenging’, then the hypernyms and hyponyms for the verb forms of the root word ‘challenge’ were returned, and the noun forms omitted.   

After writing the functions into python scripts, the website was created using Streamlit, a web app builder that utilizes python. Currently, the website can handle any reasonable amount of text, and displays the list of flagged words and the recommended replacements; however, for longer postings, the input and highlighted words do not display in their entirety.   

In the future, I would like to improve the website’s functionality, as well as the model accuracy. I plan to deploy the website using docker, after trying and failing to deploy it via virtual machine on Azure. I plan to expand the number of models used, particularly improving the part of speech classification and including larger training corpuses. I also plan to create a Chrome extension for recommend(her).   

https://www.linkedin.com/in/lydia-kajeckas/
