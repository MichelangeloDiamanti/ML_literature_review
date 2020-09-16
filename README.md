The aim of this tool is to help researchers perform literature reviews. A literature review summarizes the existing research in a chosen field, condensing state-of-the-art knowledge into a single analysis. Unfortunately, literature reviews are highly time consuming. In particular, a researcher’s first pass over an entire research corpus can take an enormous amount of time. To mitigate this limitation, we propose a semi-automatic method for classifying paper titles based on how interesting they should be to the researcher. Our method involves selecting keywords, searching databases of papers, preparing training data for a machine learning model, and then finally training, optimizing, and deploying the model to help classify papers.

- The ./method folder contains an example of keyword extraction and the relative query for the scopus database (https://www.scopus.com/)  
- scopus_search_results.csv contains the results of the scopus query, basically papers information (title, authors, etc...)  
- binary_decision_tree.ipynb is the jupyter nootbook with the code for training and using the model  
- scopus_search.py is a GUI application that helps reading titles and abstracts, and classifying them in "interesting" or "not interesting"  

![GUI Description](/gui_description.png)