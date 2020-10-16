import stanza

def parse(f):
  res = set()
  c = 0
  for sen in f.readlines():
    print(c)
    c += 1
    doc = nlp(sen)
    s = set([word.text for sen in doc.sentences for word in sen.tokens])
    res = res.union(s)
  return res

if __name__ == "__main__":

    nlp = stanza.Pipeline('hi')
    # path_1 = '/content/drive/My Drive/BTP/Errant_for_Hindi/Hindi Word List/final_words_frq.txt'
    # path_2 = '/content/drive/My Drive/BTP/Errant_for_Hindi/Hindi Word List/final_hindi_movies_list.txt'
    # path_3 = '/content/drive/My Drive/BTP/Errant_for_Hindi/Hindi Word List/CN-MWE-Dataset-from-corpus.txt'
    # path_4 = '/content/drive/My Drive/BTP/Errant_for_Hindi/Hindi Word List/LVC-MWE-Dataset-from-corpus.txt'
    path_5 = '/content/drive/My Drive/BTP/Errant_for_Hindi/Hindi Word List/B.txt'

    # f_1 = open(path_1, "r")
    # f_2 = open(path_2, "r")
    # f_3 = open(path_3, "r")
    # f_4 = open(path_4, "r")
    f_5 = open(path_5, "r")

    # text_1 = set([sen for sen in f_1.readlines()])
    # text_2 = set([w for sen in f_2.readlines() for w in sen.split()])
    # text_3 = set([w for sen in f_3.readlines() for w in sen.split()])
    # text_4 = set([w for sen in f_4.readlines() for w in sen.split()])
    text_5 = parse(f_5)

    # vocab = text_1.union(text_2)
    # vocab = vocab.union(text_3)
    # vocab = vocab.union(text_4)
    # vocab = vocab.union(text_5)

    # f_1.close()
    # f_2.close()
    # f_3.close()
    # f_4.close()
    f_5.close()

    # vocab.remove('y')
    # vocab.remove('n')
    # print(len(vocab))

    c = 0
    f = open("vocab_B.txt", "a")
    for v in text_5:
        if (len(v) == 0):
            continue
        f.write(v)
        if v[-1] != '\n':
            f.write('\n')
        c += 1
    f.close()

