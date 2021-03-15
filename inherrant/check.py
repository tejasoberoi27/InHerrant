import stanza
from inherrant.alignment import Alignment
import inherrant
import Levenshtein


if __name__ == '__main__':
    # stanza.download('hi')
    nlp = stanza.Pipeline('hi')
    # s1 = "अब में बिल्कुल थक चुका हूँ।"
    # s2 = "अब में थक चुका हूँ।"



    # s1 = "मैं तुम्हारा पिता तो हूँ और कभी कभी महज़ एक दोस्त ।"
    # s2 = "मैं तुम्हारा पिता तो हूँ लेकिन कभी कभी महज़ एक दोस्त ।"

    # s1 = "वह जल्दी सोया | "
    # s2 = "वह जल्दी सो गया था | "

    # s1 = "प्रस्तुत पंक्तियाँ सरोज स्मृति से ली हैं।"
    # s2 = "प्रस्तुत पंक्तियाँ 'सरोज स्मृति' से ली गयी हैं।"

    s1 = "रूपवती सुमन बहुत सुंदर हैं।"
    s2 = "सुमन रूपवती है।"
    #
    # s1 = "करन की माँ भारी दुखी है।"
    # s2 = "करन की माँ बहुत दुखी है।"

    # s1 = "हैं! तुम क्या कर रहे हो ?"
    # s2 = "अरे! पीछे हो जाओ, गिर जाओगे ।  "
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

