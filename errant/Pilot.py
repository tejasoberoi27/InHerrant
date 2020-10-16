import stanza
from errant.alignment import Alignment
<<<<<<< HEAD
import errant
=======
import Levenshtein
>>>>>>> 81cfc336dbe27fb80f005d985e9d73b010384ed1

def align(orig, cor, lev=False):
    return Alignment(orig, cor, lev)

def char_cost(a, b):
    return Levenshtein.ratio(a.text, b.text)

if __name__ == '__main__':
    # stanza.download('hi')
    nlp = stanza.Pipeline('hi')
    doc = nlp("आप से मिलकर बहुत ख़ुशी हुई")
    # print(doc)

    annotator = errant.load("hi")

    # Input 1: An original text string parsed by spacy
    # Input 2: A corrected text string parsed by spacy
    # Input 3: A flag for standard Levenshtein alignment
    # Input 4: A flag for merging strategy
    # Output: A list of automatically extracted, typed Edit objects
    s1 = "मैंने यह पुस्तक देखा हूँ।"
    s2 = "मैंने यह पुस्तक देखी है।"
    doc1 = nlp(s1)
    doc2 = nlp(s2)
    target_iterator = iter(doc2.sentences)
    for i, orig in enumerate(doc1.sentences):
        cor = next(target_iterator)
        # print(orig,cor)
        o_low = orig.tokens
        c_low = cor.tokens
        cur = char_cost(o_low[3], c_low[3])
        print(o_low[3],c_low[3],"cost: "+str(cur))
    #     cor = next(target_iterator)
    #     lev = True
    #     alignment = align(orig, cor, lev)
    #     print(alignment)


