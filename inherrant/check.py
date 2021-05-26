import stanza
from inherrant.alignment import Alignment
import inherrant
import Levenshtein


if __name__ == '__main__':
    # stanza.download('hi')
    nlp = stanza.Pipeline('hi',use_gpu=True)

    # s1 = "अब में बिल्कुल थक चुका हूँ।"
    # s2 = "अब में थक चुका हूँ।"



    # s1 = "मैं तुम्हारा पिता तो हूँ और कभी कभी महज़ एक दोस्त ।"
    # s2 = "मैं तुम्हारा पिता तो हूँ लेकिन कभी कभी महज़ एक दोस्त ।"

    # s1 = "वह जल्दी सोया | "
    # s2 = "वह जल्दी सो गया था | "

    # s1 = "प्रस्तुत पंक्तियाँ सरोज स्मृति से ली हैं।"
    # s2 = "प्रस्तुत पंक्तियाँ 'सरोज स्मृति' से ली गयी हैं।"

    # s1 = "मुर्गी बांग दे रही है ।"
    # s2 = "मुर्गा बांग दे रहा है ।"

    # s1 = "इन्होंने"
    # s1 = "वे खेल रहे है"
    # s2 = "वह"
    # s1 = "भेड़ बकरी पालन करना इस समुदाय का प्रमुख कार्य है"
    # s2 = "भेड़ बकरी पालन करना इस समुदाय का प्रमुख कार्य था"
    #
    # s1 = "करन की माँ भारी दुखी है।"
    # s2 = "करन की माँ बहुत दुखी है।"
    # s1 = "चाय की दुकान से लेकर वाहनों और दिवारों तक हर जगह विज्ञापन ही विज्ञापन दिखाई देते है"
    # s2 = "चाय की दुकान से लेकर वाहनों और दिवारों तक हर जगह विज्ञापन ही विज्ञापन दिखाई देते हैं"
    # s1 = "भेड़ बकरी पालन करना इस समुदाय का प्रमुख कार्य है"
    # s2 = "भेड़ बकरी पालन करना इस समुदाय का प्रमुख कार्य था"

    # s1= "स्क्रैपबुक मोज़िला फायरफॉक्स वेब ब्राउजर हेतु एक ऍक्सटेंशन है जो कि संवर्धित , पेज सेविंग , बुकमार्किंग तथा नोटटेकिंग आदि फंक्शनैलिटी जोड़ती है ."
    # s1 = "स्\u200dपीती"
    # # s1 = "हैं! तुम क्या कर रहे हो ?"
    # s2 = "अरे! पीछे हो जाओ, गिर जाओगे ।  "

    s1 = "15 जनवरी 2019 को एयरटेल भारत के अंडमान व निकोबार का पहला 4 नेटवर्क बना ।"
    s2 = "15 जनवरी 2019 को एयरटेल भारत के अंडमान और निकोबार का पहला 4 नेटवर्क बना ।"

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

