import stanza
from errant.alignment import Alignment
import errant
import Levenshtein


def align(orig, cor, lev=False):
    return Alignment(orig, cor, lev)


def char_cost(a, b):
    return Levenshtein.ratio(a.text, b.text)


def all_split(orig, cor):
    print("ALL SPLIT")
    edits = annotator.annotate(orig, cor, lev=False, merging="all-split")  # lev = True, merging strategy = all_split
    print("Number of edits: %d" % len(edits))
    for x in edits:
        print(x)
    print("All split ends")


if __name__ == '__main__':
    # stanza.download('hi')
    nlp = stanza.Pipeline('hi')
    # doc = nlp("आप से मिलकर बहुत ख़ुशी हुई")
    # print(doc)

    annotator = errant.load("hi")

    # Input 1: An original text string parsed by spacy
    # Input 2: A corrected text string parsed by spacy
    # Input 3: A flag for standard Levenshtein alignment
    # Input 4: A flag for merging strategy
    # Output: A list of automatically extracted, typed Edit objects
    # s1 = "मैंने यह पुस्तक देखा हूँ।"
    # s2 = "मैंने यह पुस्तक देखी है।"
    
    s1 = "हम हैं अच्छे  ।"
    s2 = " अच्छे हम हैं।"
    # s1 = "सारे दिन भर वह काम करता रहा।"
    # s2 = "वह दिन भर काम करता रहा।"
    doc1 = nlp(s1)
    doc2 = nlp(s2)
    target_iterator = iter(doc2.sentences)

    for i, orig in enumerate(doc1.sentences):
        cor = next(target_iterator)
        # print("type",type(orig))#type of orig = Sentence
        # print(orig,cor)
        # o_low = orig.tokens
        # c_low = cor.tokens
        # cur = char_cost(o_low[3], c_low[3])
        # print(o_low[3],c_low[3],"cost: "+str(cur))
        # cor = next(target_iterator)
        # alignment = align(orig, cor, lev)
        # print(alignment)
        # all_split(orig,cor)
        edits = annotator.annotate(orig, cor, lev= False ,merging= "rules") # lev = True, merging strategy = all_split
        print("Number of edits: %d" % len(edits))
        for x in edits:
            print(x)
            # print(type(x.o_toks[-1])) # type is token
    print(s1)
    print(s2)
    # print("Doc1",doc1)
    # print("Doc2",doc2)
