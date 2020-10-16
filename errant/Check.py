import stanza
import spacy.symbols as POS


if __name__ == '__main__':
    stanza.download('en')
    nlp = stanza.Pipeline(lang='en')
    doc = nlp('Barack Obama was born in Hawaii.')
    # print(*[f'word: {word.text}\tupos: {word.upos}\txpos: {word.xpos}\tfeats: {word.feats if word.feats else "_"}' for
    #         sent in doc.sentences for word in sent.words], sep='\n')
    for sentence in doc.sentences:
        for word in sentence.words:
            print(word.text,word.pos,word.pos== POS.AUX)