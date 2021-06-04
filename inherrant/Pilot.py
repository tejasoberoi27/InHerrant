import stanza
from inherrant.alignment import Alignment
import inherrant
import Levenshtein


def normalise_char(token):
    ''' returns token after changing expanded characters with dot to single character'''
    expanded1 = 'ड' + '़'
    token = token.replace(expanded1, 'ड़')
    expanded2 = 'ढ' + '़'
    token = token.replace(expanded2, 'ढ़')
    matra1 = 'ॊ'
    token = token.replace(matra1, 'ो')
    matra2 = 'ॆ'
    token = token.replace(matra2, 'े')
    return token


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

    # s1 = "आजकल खूब वर्षाएँ हो रही हैं।"
    # s2 = "आजकल खूब वर्षा हो रही है।"

    # s1 = "उसका चेहरा खिल उठा |"
    # s2 = "उसका चेहरा खिल गया |"

    # s1 = "वह खूब खेल चुका |"
    # s2 = "वह खूब खेला था |"

    # s1 = "मुर्गी बांग दे रही है ।"
    # s2 = "मुर्गा बांग दे रहा है ।"

    # s1 = "मुझे यह घड़ी मिल चुकी है।"
    # s1 = "भेड़ बकरी पालन करना इस समुदाय का प्रमुख कार्य है"
    # s2 = "भेड़ बकरी पालन करना इस समुदाय का प्रमुख कार्य था"

    # s1 = "चाय की दुकान से लेकर वाहनों और दिवारों तक हर जगह विज्ञापन ही विज्ञापन दिखाई देते है"
    # s2 = "चाय की दुकान से लेकर वाहनों और दिवारों तक हर जगह विज्ञापन ही विज्ञापन दिखाई देते हैं"

    # s1 = "चाय की दुकान से लेकर वाहनों और दिवारों तक हर जगह विज्ञापन ही विज्ञापन दिखाई देते गया"
    # s2 = "चाय की दुकान से लेकर वाहनों और दिवारों तक हर जगह विज्ञापन ही विज्ञापन दिखाई देते गये"
    # s2 = "मुझे यह घड़ी मिली।"

    # s1 = "वह खेल रहा था |"
    # s2 = "वह खेल चुका था |"

    # s1 = "वह घर पर नाचता होगी "
    # s2 = "वह घर पर नाचता होगा "

    # s1 = "वह घर से निकल चुकी "
    # s2 = "वह घर से गिरेगी"


    # s1 = "वह खेला है "
    # s2 = "वह खेलता रहता है "
    # s1 = "वे खाना खा चुके होंगे |"
    # s2 = "वे खाना खा रहे हैं |"

    # s1 = "वे खाना खाते रहते हैं "
    # s2 = "वे दारू अक्सर पीते हैं "
    # s1 = "वे खाना खा चुके होंगे |"
    # s2 = "वह खाना खा रहा होगा |"

    # s1 = "वे दारू पीके सो गए |"
    # s2 = "वह दारू पी |"

    # s1 = "भेड़ बकरी पालन करना इस समुदाय का प्रमुख कार्य है"
    # s2 = "भेड़ बकरी पालन करना इस समुदाय का प्रमुख कार्य था"

    # s1 = "आज हम विज्ञापन युग के सीमान्त पर आ खड़े हुए है ."
    # s2 = "आज हम विज्ञापन युग के सीमान्त पर आ खड़े हुए हैं ."

    # s1 = "15 जनवरी 2019 को एयरटेल भारत के अंडमान व निकोबार का पहला 4 नेटवर्क बना ।"
    # s2 = "15 जनवरी 2019 को एयरटेल भारत के अंडमान और निकोबार का पहला 4 नेटवर्क बना ।"

    # s1 = "एक दूध का गिलास दो ।"
    # s2 = "दूध का एक गिलास दो ।"

    # s1 = "भेड़ बकरी पालन करना इस समुदाय का प्रमुख कार्य है"
    # s2 = "भेड़ बकरी पालन करना इस समुदाय का प्रमुख कार्य था"
    # s1 = "वह गिरा था"
    # s2 = "वह गिरेगा"

    # s1 = "वह kal "
    # s2 = "वह अभी गिरा"

    # s1 = "मैं गिरेगा"
    # s2 = "मैं गिरूँगा"

    # s1 = "मैंने पानी पिया"
    # s2 = "मैं पानी पियूँगा"

    # s1 = "घूंगरू टूट गए"
    # s2 = "घूंगरू टूट जाएँगे"

    # s1 = "अखरोट टूटे थे"
    # s2 = "अखरोट टूट जाएँगे"

    # Nice
    # s1 = "मैं पानी पी रहा हूँ"
    # s2 = "मैं पानी पियूँगा"

    # s1 = "मैं पानी पी रहा हूँ"
    # s2 = "मैं जीवन जियूँगा"

    # s1 = "मैं पीऐनो सीख रहा हूँ"
    # s2 = 'मैं पीऐनो देखूँगा'

    # s1 = "मैं दिया जला रहा हूँ"
    # s2 = "मैं दिया जलाता रहूँगा"

    # s1 = "मैं सब्ज़ी ख़रीदने जा रही हूँ"
    # s2 = "मैं सब्ज़ी ख़रीदने जाऊँगी"

    # s1 = "मैंने जोखिम उठाया है"
    # s2 = "मैं जोखिम उठाऊँगा"

    # s1 = "मैंने वादा नहीं तोड़ा था"
    # s2 = "मैं वादा नहीं तोड़ूँगा"

    # s1 = "वह फ़ुट्बॉल खेलता रहा"
    # s2 = "वह फ़ुट्बॉल खेलता रहेगा"

    # s1 = "वह हँसता रहा"
    # s2 = "वह हँसता रहेगा"

    # s1 = "उसने प्राप्त कर लिया"
    # s2 = "वह प्राप्त कर लेगा"

    # s1 = "उसने कर दिखाया था"
    # s2 = "वह कर दिखाएगा"

    # s1 = "उसने कर दिखाया"
    # s2 = "वह कर दिखाएगा"

    # s1 = "वह कर दिखाता है"
    # s2 = "उसने कर दिखाया"

    # s1 = "उसने टेलेफ़ोन वापस कर दिया"
    # s2 = "वह टेलेफ़ोन वापस कर देगा"

    # s1 = "वह गले लगा था"
    # s2 = "वह गले लग जाएगा"

    # s1 = "मैं अच्छा जीवन बिताता हूँ"
    # s2 = "मैं अच्छा जीवन व्यतीत करता हूँ"

    # s1 = "सबको शिक्षित करो"
    # s2 = "सबको शिक्षित करना चाहिए था"

    # s1 = "सबको शिक्षित करो"
    # s2 = "सबको शिक्षित करना ज़रूरी है"

    # s1 = "वह 1992 में पैदा हुआ था"
    # s2 = "वह 2005 में पैदा होगा "

    # s1 = "वह बदला ले चुका"
    # s2 = "वह बदला लेगा"

    # Nice
    # s1 = "वह दवाई लेना चाहता है"
    # s2 = "वह दवाई ले चुका है"

    # s1 = "शब्द को रेखांकित करो"
    # # s2 = "शब्द को रेखांकित  करो"
    # s2 = "शब्द की रेखा खींचो"

    # s1 = "वह व्यथित था"
    # s2 = "उसकी व्यथा दिख रही थी"

    # s1 = "वह व्यथित दिख रहा था"
    # s2 = "उसकी व्यथा दिख रहा है"

    # s1 = "वह चिंतित था"
    # s2 = "उसको चिंता थी"

    # s1 = "उसके संस्कार अच्छे हैं "
    # s2 = "वह संस्कारी है"

    # s1 = "और विदाई के वक्त इंद्र कंवर से वादी किया की एक दिन वह उसे जरूर मुगल बादशाह से मुक्त कराऐंगे ."
    # s2 = "और विदाई के वक्त इंद्र कंवर से वादा किया की एक दिन वह उसे जरूर मुगल बादशाह से मुक्त कराऐंगे ."

    # s1 = "राधा मेरी परम प्रिय स्नेही है "
    # s2 = "राधा मेरी परम प्रिय स्नेहा है "
    # s1 = "१५ जनवरी २०१२ की स्थित तक इस विकिपीडिया पर लेखों की सँख्या है"
    # s2 = "१५ जनवरी २०१२ की स्थिति तक इस विकिपीडिया पर लेखों की सँख्या है"

    # s1 = "२५ नवम्बर , २००७ तक इसमें कुल ४ , ९०० लेख थे जो इसे विकिपीडिया का ९६ वां सबसे बड़ा संस्करण बनता है"
    # s2 = "२५ नवम्बर , २००७ तक इसमें कुल ४ , ९०० लेख थे जो इसे विकिपीडिया का ९६ वां सबसे बड़ा संस्करण बनाता है"

    # s1 = "मैं मुस्कुराती रहूँगी"
    # s2 = "मैं मुस्कुरा रही हूँ"
    # s1 = "यह हिन्दू धर्म की एक देवता हैं ."
    # s2 = "यह हिन्दू धर्म की एक देवी हैं ."

    # s1 = "2006 में उन्होंने वेस्सेलिन तोपालोव को पराजित करके 1993 के बाद से पहली निर्विवाद चैंपियन बन गए"
    # s2 = "2006 में उन्होंने वेस्सेलिन तोपालोव को पराजित करके 1993 के बाद से पहले निर्विवाद चैंपियन बन गए ."

    # s1 = "वाम मोर्चा पार्टियां दोनों सरकारों और मुख्यधारा के विपक्षी दलों की नीतियों की आलोचना करते हुए संसद में एक स्वतंत्र गुट बने रहती हैं ."
    # s2 = "वाम मोर्चा पार्टियां दोनों सरकारों और मुख्यधारा के विपक्षी दलों की नीतियों की आलोचना करते हुए संसद में एक स्वतंत्र गुट बनाए रहती हैं ."

    # s1 = "वह मुझे प्रेरणा करती है"
    # s2 = "वह मुझे प्रेरित करती है"

    # s1 = "वो है मेरी हमसफ़र"
    # s2 = "वही है मेरी हमसफ़र"

    # s1 = "वह अभिनेता बनने चला "
    # s2 = "वह अभिनेता बनने गया था"

    # s1 = "इस जल्ला के पूर्व में चितवन और गोरखा उत्तर में कास्क और लम जुंग पश्चिम मे सांजस्य दक्षिण मे अल्पाल्प और नवल परासी जिलाएँ हैं ."
    # s2 = "इस जिला के पूर्व में चितवन और गोरखा उत्तर में कास्की और लमजुंग पश्चिम मे स्यांजा दक्षिण मे पाल्पा और नवलपरासी जिलाएं हैं ."
    # s2 = "इस जल्ला के पूर्व में चितवन और गोरखा उत्तर में कास्क और लम जुंग पश्चिम मे सांजस्य दक्षिण मे अल्पाल्प और नवल परासी जिलाएं हैं ."

    # s1 = "मुख्य चुनाव आयुक्त को संसद द्वारा महाभियोग पर राष्ट्रपति द्वारा हटाया जा सक़ता हैं"
    # s2 = "मुख्य चुनाव आयुक्त को संसद द्वारा महाभियोग पर राष्ट्रपति द्वारा हटाया जा सकता हैं ."

    # s1 = "मुख्य चुनाव आयुक्त को संसद द्वारा महाभियोग पर राष्ट्रपति द्वारा हटाया जा सक़ता हैं"
    # s2 = "मुख्य चुनाव आयुक्त को संसद द्वारा महाभियोग पर राष्ट्रपति द्वारा हटाया जा सकता हैं ."

    # s1 = "पूर्वोत्तर क्षेत्र में कोई और इलाका नही तय किया जा कसा"
    # s2 = "पूर्वोत्तर क्षेत्र में कोई और इलाका नहीं तय किया जा सका"

    # s1 = "मुझे खाना बनाना बहुत पसंद है और अपने खाली समय के दौरान नए नए व्यंजन बनाती है ."
    # s2 = "मुझे खाना बनाना बहुत पसंद है और अपने खाली समय के दौरान नए नए व्यंजन बनाती हूँ ."

    # s1 = "यहां से जय सिंह 2020 में विधायक होंगे यह तय है ."
    # s2 = "यहां से जय सिंह 2020 में विधायक होंगे यह तय ह ."

    # s1 = "इंदु सोनाली का जन्म 7 नवंबर 1978 को भागलपुर , ( बिहार ) ‌‌ में हुआ था ."
    # s2 = "इंदु सोनाली का जन्म 7 नवंबर 1978 को भागलपुर , ( बिहार ) ‌‌ में हुआ हैं ."

    # s1 = "राजनीति से जुड़ने के कुछ समय पूर्व उनका विवाह विजयलक्ष्मी देवी से ही गया ."
    # s2 = "राजनीति से जुड़ने के कुछ समय पूर्व उनका विवाह विजयलक्ष्मी देवी से हो गया ."

    # s1 = "उन्होंने पार्श्व गायिका के रूप में कई पंजाबी फिल्में कीं और कुछ ने साइड एक्ट्रेस के रूप में भी कार्य किया हैं ."
    # s2 = "उन्होंने पार्श्व गायिका के रूप में कई पंजाबी फिल्में कीं और कुछ ने साइड एक्ट्रेस के रूप में भी कार्य किये हैं ."

    # s1 ="इसके प्रकाशन के साथ नेमेड तेजी से अपनी पीढ़ी के प्रतिनिधि लेखक माने जाने लगे |"
    # s2 ="इसके प्रकाशन के साथ नेमेड तेजी से अपनी पीढ़ी के प्रतिनिधि लेखक माना जाने लगे |"

    # s1 = "ओड़ीसा के आदिवासी क्षेत्रों के बच्चे तब तक गमछा पहनते हैम जब वे बड़े होकर धोती न पहनना शुरू कर दें ."
    # s2 = "ओड़ीसा के आदिवासी क्षेत्रों के बच्चे तब तक गमछा पहनते हैं जब वे बड़े होकर धोती न पहनना शुरू कर दें ."
    # s2 = "यहां से जय सिंह 2020 में विधायक होंगे यह तय है ."
    # s1 = "यहां से जय सिंह 2020 में विधायक होंगे यह तय ह ."
    # s1 = "बाद में बढ़ते बढ़ते सन ज़ अक्तूबर १९६८ में ब्रह्मलीन ज्योतिष-शास्त्रज्योतिष जगद्गुरु शंकराचार्य कृष्णांबरधारी जी महाराज ने नवीन मंदिर का शिलान्यास किया"
    # s2 = "बाद में बढ़ते बढ़ते सन ज़ अक्तूबर १९६८ में ब्रह्मलीन ज्योतिष-शास्त्रज्योतिष जगद्गुरु शंकराचार्य कृष्णांबरधारी जी महाराज ने नवीन मंदिर का शिलान्यास किया"

    # s1 = "वह उससे मिलता है "
    # s2 = "वह उससे मिलने केलिए जाता है"

    # s1 = "वह उससे मिलता था "
    # s2 = "वह उससे मिलता रहता था"

    # s1 = "वह काम बन "
    # s2 = "वह काम बना"

    # s1 = "सिपाही पर घड़ों पानी गिर पड़ा।"
    # s2 = "सिपाही पर घड़ों पानी पड़ गया।"

    # s1 = "उसका प्राण निकल रहा है।"
    # s2 = "उसके प्राण निकल रहे हैं।"

    # s1 = "जय नारायण व्यास विद्यालय में लगभग 1600 विद्यार्थी विभिन्न विषयों पर पढ़ाई कर रेह है ."
    # s2 = "जय नारायण व्यास विद्यालय में लगभग 1600 विद्यार्थी विभिन्न विषयों पर पढ़ाई कर रहे हैं ."

    # s1 = "अलाउद्दीन बंदी बना लिया गया किंतु संजर ने कुछ समय उपरात उसे मुक्त कर गोर का राज्य उसे वापस कर दिया . "
    # s2 = "अलाउद्दीन बंदी बना लिया गया किंतु संजर ने कुछ समय उपरांत उसे मुक्त कर गोर का राज्य उसे वापस कर दिया ."

    # s1 = "यद्यपि यज्ञ को वातावरण प्रदुषण लिये समाधान माना जाता है पर ईस बात के कॉई अधिकारिक वैज्ञानिक प्रमाण उपलब्ध नही है ."
    # s2 = "यद्यपी यज्ञ कॊ वातावरण प्रदुषणकॆ लियॆ समाधान माना जाता है पर इस बात कॆ कॊई अधिकारिक वैज्ञानिक प्रमाण ऊपलब्ध नही है ."

    # s1 = "उस गाड़ी के एंजिन ख़राब है "
    # s2 = "उस गाड़ी का एंजिन ख़राब है "

    # s1 = "गड़रिया नाम पुराने हिंदी शब्द गदर से लिया गया है ज़ जिसका अर्थ है भेड़ ."
    # s2 = "गड़रिया नाम पुराने हिंदी शब्द गाडर से लिया गया है , जिसका अर्थ है भेड़ ."

    # s1 = "वहाँ से अनुमति मिलने पर आप परीक्षा हिन्दी मे दे सकेंगे ."
    # s2 = "वहाँ से अनुमति मिलने पर आप परीक्षा हिन्दी में दे सकेंगे ."

    # s1 = "स्वभाव के अनुरूप तुम्हें यह कार्य करना चाहिए।"
    # s2 = "स्वभाव के अनुकूल तुम्हें यह कार्य करना चाहिए।"

    # s1 = "वह तेज़ी नाचती है "
    # s2 = "वह तेज़ नाचती है "

    # s1 = "संख्या १२ को सरकार का प्रतिनिधित्व करने के लिए महत्वपूर्ण समझा जाता है और ज़ बारह दर्शाता है सरकारी पूर्णता ज़ ."
    # s2 = "संख्या १२ को सरकार का प्रतिनिधित्व करने के लिए महत्त्वपूर्ण समझा जाता है और \" बारह दर्शाता है सरकारी पूर्णता \" ."

    # s1 = "वह खेल पाया था"
    # s2 = "वह खेल चुका था"

    # s1 = "इनमें विश्व की 26 सभ्यताओं के विकास , ह्रास ओर पतन का गवेषणात्मक विवेचन किया गया है ।"
    # s2 = "इनमें विश्व की 26 सभ्यताओं के विकास , ह्रास और पतन का गवेषणात्मक विवेचन किया गया है ।"

    # s1 = "उनका जन्म चेन्नई में हा था ."
    # s2 = "उनका जन्म चेन्नई में हुआ था ."

    # s1 = "बहुत से पड़ोसी देशों द्वारा खोज और बचाव के लिए सैन्य लकडियां भेजीं गयीं ."
    # s2 = "बहुत से पड़ोसी देशों द्वारा खोज और बचाव के लिए सैन्य टुकडियां भेजीं गईं ."


    # s1 = "उसको दुर्जन कहकर पुकारना अनुचित है।"
    # s2 = "उसको दुर्जन कहना अनुचित है।"

    # s1 = "विशवास"
    # s1 = "अराधना"
    # s2 = "आराधना"

    # s1 = "वह खेल चुका है "
    # s2 = "वह खेल रहा है"

    # s1 = "पोशाक इस्तरी करनी चाहिए "
    # s2 = "पोशाक पर इस्तरी लगनी चाहिए"

    s1 = normalise_char(s1)
    s2 = normalise_char(s2)

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
        # print("orig",orig,"cor",cor)
        edits = annotator.annotate(orig, cor, lev=False, merging="rules")  # lev = True, merging strategy = all_split
        print("Number of edits: %d" % len(edits))
        for x in edits:
            print(x)
            # print(type(x.o_toks[-1])) # type is token
    print(s1)
    print(s2)
    # print("Doc1",doc1)
    # print("Doc2",doc2)
