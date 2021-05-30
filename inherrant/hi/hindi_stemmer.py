#! /usr/bin/env python3.1
''' Lightweight Hindi stemmer
Copyright © 2010 Luís Gomes <luismsgomes@gmail.com>.

Implementation of algorithm described in

    A Lightweight Stemmer for Hindi
    Ananthakrishnan Ramanathan and Durgesh D Rao
    http://computing.open.ac.uk/Sites/EACLSouthAsia/Papers/p6-Ramanathan.pdf

    @conference{ramanathan2003lightweight,
      title={{A lightweight stemmer for Hindi}},
      author={Ramanathan, A. and Rao, D.},
      booktitle={Workshop on Computational Linguistics for South-Asian Languages, EACL},
      year={2003}
    }

Ported from HindiStemmer.java, part of of Lucene.
'''

class HindiStemmer:
    def stem(self, word,get_suf=False):
        suffixes = {
            1: ["ो", "े", "ू", "ु", "ी", "ि", "ा"],
            2: ["कर", "ाओ", "िए", "ाई", "ाए", "ने", "नी", "ना", "ते", "ीं", "ती", "ता", "ाँ", "ां", "ों",
                "ें"],
            3: ["ाकर", "ाइए", "ाईं", "ाया", "ेगी", "ेगा", "ोगी", "ोगे", "ाने", "ाना", "ाते", "ाती", "ाता",
                "तीं", "ाओं", "ाएं", "ुओं", "ुएं", "ुआं"],
            4: ["ाएगी", "ाएगा", "ाओगी", "ाओगे", "एंगी", "ेंगी", "एंगे", "ेंगे","ूँगा","ूँगी", "ूंगी", "ूंगा", "ातीं",
                "नाओं", "नाएं", "ताओं", "ताएं", "ियाँ", "ियों", "ियां"],
            5: ["ाएंगी", "ाएंगे", "ाऊंगी", "ाऊंगा", "ाइयाँ", "ाइयों", "ाइयां"],
        }
        for L in 5, 4, 3, 2, 1:
            if len(word) > L + 1:
                for suf in suffixes[L]:
                    # print type(suf),type(word),word,suf
                    if word.endswith(suf):
                        # print 'h'
                        if get_suf:
                            return word[:-L], suf
                        else:
                            return word[:-L]
        if get_suf:
            return word, ""
        else:
            return word