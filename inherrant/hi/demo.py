import Levenshtein
from inherrant.hi.hindi_stemmer import HindiStemmer
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
# stemmer = HindiStemmer()
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
a = "बढ़ते"
b = "बढ़ते"
x = a.encode('UTF-16')
y = b.encode('UTF-16')

print(x,y)
print(x==y)