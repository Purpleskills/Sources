import os
import re
from functools import reduce
from owlready2 import get_ontology, onto_path
from .models import *

onto_path.append(os.path.dirname(__file__))
onto = get_ontology("CSO.3.1.owl")

import re
def ireplace(old, repl, text):
    return re.sub('(?i)'+re.escape(old), lambda m: repl, text)

def generate_tags(phrase):
    # todo: optimize this function
    onto.load()
    from nltk.corpus import stopwords
    result_wordpairs = []
    previous_word = None
    tags = []
    stop_words = set(stopwords.words('english'))
    repls = ('.', ''), ('&', '')
    phrase = reduce(lambda a, kv: a.replace(*kv), repls, phrase)
    appendFile = open('filteredtext.txt', 'a')
    for word in phrase.split():
        if not word[:1].isalnum():
            previous_word = None
        else:
            word_lower = word.lower()
            if previous_word:
                result_wordpairs.append(previous_word + '_' + word_lower)  # %20
            previous_word = word_lower
    for wordpair in result_wordpairs:
        try:
            tag = CourseTag.objects.get(name=wordpair)
            tags.append(tag)
            newphrase = wordpair.replace("_", ' ')
            phrase = ireplace(newphrase, '', phrase)
        except CourseTag.DoesNotExist:
            if onto.search(iri="*" + wordpair):
                newphrase = wordpair.replace("_", ' ')
                phrase = ireplace(newphrase, '', phrase)
                newtag = CourseTag(name=wordpair)
                newtag.save()
                tags.append(newtag)
            else:
                appendFile.write(" " + wordpair)
    for word in phrase.split():
        if not word in stop_words:
            try:
                tag = CourseTag.objects.get(name=word)
                tags.append(tag)
            except CourseTag.DoesNotExist:
                if onto.search(iri="*" + word):
                    newtag = CourseTag(name=word)
                    newtag.save()
                    tags.append(newtag)
                else:
                    appendFile.write(" " + word)
    appendFile.close()
    return tags
