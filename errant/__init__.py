from importlib import import_module
import stanza
from errant.annotator import Annotator

# ERRANT version
__version__ = '1.0.0'

# Load an ERRANT Annotator object for a given language
def load(lang, nlp=None):
    # Make sure the language is supported
    supported = {"hi"}
    if lang not in supported:
        raise Exception("%s is an unsupported or unknown language" % lang)

    # Load stanza
    nlp = nlp or stanza.Pipeline('hi')

    # Load language edit merger
    merger = import_module("errant.%s.merger" % lang)

    # Load language edit classifier
    print("Location: errant.%s.classifier" % lang)
    classifier = import_module("errant.%s.classifier" % lang)

    # The Hindi classifier needs stanza
    if lang == "hi": classifier.nlp = nlp

    # Return a configured ERRANT annotator
    return Annotator(lang, nlp, merger, classifier)