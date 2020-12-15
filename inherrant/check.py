import stanza
from inherrant.alignment import Alignment
import inherrant
import Levenshtein


if __name__ == '__main__':
    # stanza.download('hi')
    nlp = stanza.Pipeline('hi')
    s1 = "दो लड़की चित्र बना रही हैं।"
    s2 = "दो लड़कियाँ चित्र बना रही हैं।"

    # print(doc)
    annotator = inherrant.load("hi")
    doc1 = nlp(s1)
    doc2 = nlp(s2)
    target_iterator1 = iter(doc1.sentences)
    target_iterator12 = iter(doc2.sentences)

    # for i, orig in enumerate(doc1.sentences):
    #     print(orig.words)
    orig1 = doc1.sentences[0].words
    print("orig1",orig1)
    orig2 = doc2.sentences[0].words
    print("orig2",orig2)
    # print(orig2[0].text,type(orig2[0].feats))
    #
    # Feats = orig2[-1].feats
    # Feats = Feats.replace("feats: ","")
    # Feats = Feats.split('|')
    # feats = {}
    # for pair in Feats:
    #     feat,val = pair.split("=")
    #     feats[feat] = val
    # print(feats)

