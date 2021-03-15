import stanza
from inherrant.alignment import Alignment
import inherrant
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

    annotator = inherrant.load("hi")

    # Input 1: An original text string parsed by spacy
    # Input 2: A corrected text string parsed by spacy
    # Input 3: A flag for standard Levenshtein alignment
    # Input 4: A flag for merging strategy
    # Output: A list of automatically extracted, typed Edit objects
    # s1 = "मैंने यह पुस्तक देखा हूँ।"
    # s2 = "मैंने यह पुस्तक देखी है।"


    # s1 = "सारे दिन भर वह काम करता रहा।"
    # s2 = "वह दिन भर काम करता रहा।"

    # s1 = "मैं तुम्हारा पिता तो हूँ और कभी कभी महज़ एक दोस्त ।"
    # s2 = "मैं तुम्हारा पिता तो हूँ लेकिन कभी कभी महज़ एक दोस्त ।"

    # s1 = "तुम लोगों को यह काम करने चाहिए ?"
    # s2 = "तुम लोगों को यह काम करना चाहिए ?"

    # s1 = "मंदिर में प्रशाद बट रहा है।"
    # s2 = "मंदिर में प्रसाद बट रहा है।"
    #
    # s1 = "यद्यपि वह मेहनती है, तब भी सफलता प्राप्त नहीं करता।"
    # s2 = "यद्यपि वह मेहनती है, तथापि वह सफलता प्राप्त नहीं करता।"

    # s1 = "यदि परिश्रम से पढ़ोगे तब अच्छे अंक प्राप्त करोगे।"
    # s2 = "यदि परिश्रम से पढ़ोगे तो अच्छे अंक प्राप्त करोगे।"

    # s1 = "उसने आसानीपूर्वक काम समाप्त कर लिया।"
    # s2 = "उसने आसानी से काम समाप्त कर लिया।"

    # s1 = "राम सो रही होगी |"
    # s2 = "राम सो रहा होगा |"

    # s1 = "यदि परिश्रम से पढ़ोगे तब अच्छे अंक प्राप्त करोगे।"
    # s2 = "यदि परिश्रम से पढ़ोगे तो अच्छे अंक प्राप्त करोगे।"

    # s1 = "रूपवती सुमन बहुत सुंदर हैं।"
    # s2 = "सुमन रूपवती है।"

    s1 = "आजकल खूब वर्षाएँ हो रही हैं।"
    s2 = "आजकल खूब वर्षा हो रही है।"

    # s1 = "उसका चेहरा खिल उठा |"
    # s2 = "उसका चेहरा खिल गया |"

    # s1 = "वह खूब खेल चुका |"
    # s2 = "वह खूब खेला था |"

    # s1 = "वह खेल रहा था |"
    # s2 = "वह खेल चुका था |"

    # s1 = "वे खाना खा चुके होंगे |"
    # s2 = "वे खाना खा रहे हैं |"

    # s1 = "वे खाना खा चुके होंगे |"
    # s2 = "वह खाना खा रहा होगा |"

    # s1 = "वे दारू पीके सो गए |"
    # s2 = "वह दारू पी |"

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