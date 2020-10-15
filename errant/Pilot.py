import stanza
from errant.alignment import Alignment

def align(orig, cor, lev=False):
    a = orig.tokens
    print(a)
    return Alignment(orig, cor, lev)

if __name__ == '__main__':
    # stanza.download('hi')
    nlp = stanza.Pipeline('hi')
    doc = nlp("आप से मिलकर बहुत ख़ुशी हुई")
    print(doc)

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
        lev = True
        alignment = align(orig, cor, lev)
        print(alignment)

