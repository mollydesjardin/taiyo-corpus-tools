
# coding: utf-8

# In[77]:

import os, sys, MeCab, glob


# In[78]:

m = MeCab.Tagger("-Owakati")


# In[79]:

for input_filename in glob.iglob("*.txt"):
    with open(input_filename, 'r', encoding='utf-8') as input_file:
        text = input_file.read()
        parsed = m.parse (text)
        output_filename = 'p_{}'.format(input_filename)
        with open(output_filename, 'w', encoding='utf-8') as output_file:
            output_file.write(parsed)


# In[76]:




# In[ ]:



