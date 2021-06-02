import Levenshtein
from inherrant.hi.hindi_stemmer import HindiStemmer
import stanza
import inherrant

# nlp = stanza.Pipeline('hi',use_gpu=True)
# stemmer = HindiStemmer()
# set_lemma = set()
# set_stem = set()
# exceptions = (('हुआ', 'हुई', 'हुए', 'हुईं'), ('था', 'थे', 'थी', 'थीं'), ('चुका', 'चुके', 'चुकी', 'चुकीं'),
#               ('लिया', 'लिए', 'ली', 'लीं'), ('आया', 'आयी', 'आयीं', 'आए', 'आई', 'आईं'),
#               ('पाया', 'पाए', 'पायी', 'पायीं'), ('गया', 'गयी', 'गई', 'गए', 'गये', 'गयीं', 'गईं'),
#               ('जाता', 'जाती', 'जाते', 'जातीं'), ('सका', 'सकी', 'सके', 'सकीं'),
#               ('रहा', 'रहे', 'रही', 'रहीं', 'रहें', 'रहो'), ('है', 'हैं'), ('ले', 'लो'),('दी','दिया'), ('लाएँगे','पाएँगे','दिया','देना'),
#               ('सकता', 'सकती', 'सकते', 'सकतीं'), ('पाएँ', 'पाओ'), ('जा', 'जाएँ', 'जाओ'), ('कर', 'करें', 'कीजिए'),
#               ('करता', 'करते', 'करती', 'करतीं'), ('की', 'किया', 'किए'),('होता','होगा','होगी','होंगी','होंगे'),('जाएगा','जाएगी','जाएँगी','जाएँगे'),
#               ('लगा','लगाया','लगाएँगे','लगाएँगी','लगाऊँ','लगी','लगीं','लगे','लगेंगे'),('जाना','जाने'),('देता','देती'),('चाहिए','चाहिएँ'),('सकूँगी','सकेंगी'),
#               ('पड़े','पड़ना','पड़ी','पड़ीं','पड़ेंगे','पड़ेगा'),('खायी','खाना','खायीं','खाए'),('लाया','लायी','लाए','लाना','लाएँगी','लायेंगी'),('चला','चले','चलेंगे','चलो'))

# exceptions = (('चाहिएँ','चाहिए'),)
# exceptions = (('चाहिए','चाहिएँ'),('सकूँगी','सकेंगी'),)

# {'जा', 'आ', 'रह', 'कर', 'गय', 'था', 'सक', 'है', 'ले', 'चुक', 'पा', 'हो','दे', 'पा', 'ला'}

# exceptions = (('लाएँगे','पाएँगे','दिया','देना'),)


# for x in exceptions:
#     for s1 in x:
#         doc1 = nlp(s1)
#         target_iterator1 = iter(doc1.sentences)
#         # for i, orig in enumerate(doc1.sentences):
#         #     print(orig.words)
#         orig1_lemma = doc1.sentences[0].words[0].lemma
#         orig1_stem = stemmer.stem(doc1.sentences[0].words[0].text)
#         print(orig1_stem)
#         # print(doc1.sentences[0].words[0])
#         # exit()
#         try:
#             set_lemma.add(orig1_lemma)
#             set_stem.add(orig1_stem)
#         except Exception as e:
#             print(e)
#             print(orig1_lemma)
#             exit()
# print("set_lemma",set_lemma)
# print("set_stem",set_stem)
# print("orig1",orig1)
# orig2 = doc2.sentences[0].words
# print("orig2",orig2)
# a = 'गिरूँगा'
# a = 'गिरूँगी'
# a = 'टूटेंगे'
# print(a[3:],len(a[3:]))
# x = 'पी'
# x = 'रेखांकित'
# x = 'व्यथित'
# a = x[4:]
# print(len(a))
# print(a)
#
# b = 'चिंता'
# print(b.endswith("ा"))
# print(b[-1])
#

# words = ['पी','पिय']
# for word in words:
#     print([i for i in word])
# print(words[1][-2:])
# # s1 = stemmer.stem('पी')
# # s2 = stemmer.stem('पियूँगा')
# # s1 = stemmer.stem('खिसकूँगा')
# # s2 = stemmer.stem('खिसक')
# # s1 = stemmer.stem('शर्माई')
# # s2 = stemmer.stem('शर्माएगी')
# s1 = stemmer.stem('मुस्कुरायी')
# s2 = stemmer.stem('मुस्कुराऊँगी')
# # s1 = ""
# # s2 = ""
# print(s1,s2)
# print(len('ी'),len('िय'))
# dist = Levenshtein.distance(s1,s2)
# print(dist,Levenshtein.ratio(s1,s2))
# # print(''.endswith('िय'))
# # d1 = "खेल"
# # d2 = "रो"
# # print(Levenshtein.ratio(d1,d2))
# a = "बढ़ते"
# b = "बढ़ते"
# x = a.encode('UTF-16')
# y = b.encode('UTF-16')
#
# print(x,y)
# print(x==y)

def expand(w):
    print("w",w)
    print([i for i in w])
    pass

def contract_char(token):
    ''' returns token after changing expanded characters with dot to single character'''
    expanded1 = 'ड' + '़'
    token = token.replace(expanded1, 'ड़')
    expanded2 = 'ढ' + '़'
    token = token.replace(expanded2, 'ढ़')
    return token
# def process_padhai(token):
#
#     return token

l = ('छोड़ा','छोड़ा','बढ़ते','बढ़ते')
# for w in l:
#     print([x for x in w])
#
#
#     w.replace('ड़',)
a = 'ड'+'़'
print(a)
expand(a)
for x in l:
    x = contract_char(x)
    expand(x)
