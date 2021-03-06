# CHILDES XML Corpus Reader

# Copyright (C) 2001-2012 NLTK Project
# Author: Tomonori Nagano <tnagano@gc.cuny.edu>
#         Alexis Dimitriadis <A.Dimitriadis@uu.nl>
# URL: <http://www.nltk.org/>
# For license information, see LICENSE.TXT

"""
Corpus reader for the XML version of the CHILDES corpus.
"""
__docformat__ = 'epytext en'

import re
from collections import defaultdict

from nltk.util import flatten

from nltk.corpus.reader.util import concat
from nltk.corpus.reader.xmldocs import XMLCorpusReader, ElementTree

# to resolve the namespace issue
NS = 'http://www.talkbank.org/ns/talkbank'

class CHILDESCorpusReader(XMLCorpusReader):
    """
    Corpus reader for the XML version of the CHILDES corpus.
    The CHILDES corpus is available at ``http://childes.psy.cmu.edu/``. The XML
    version of CHILDES is located at ``http://childes.psy.cmu.edu/data-xml/``.
    Copy the needed parts of the CHILDES XML corpus into the NLTK data directory
    (``nltk_data/corpora/CHILDES/``).

    For access to the file text use the usual nltk functions,
    ``words()``, ``sents()``, ``tagged_words()`` and ``tagged_sents()``.
    """
    def __init__(self, root, fileids, lazy=True):
        XMLCorpusReader.__init__(self, root, fileids)
        self._lazy = lazy

    def test(self):
        return 12

    def words(self, fileids=None, speaker='ALL', stem=False,
            relation=False, strip_space=True, replace=False):
        """
        :return: the given file(s) as a list of words
        :rtype: list(str)

        :param speaker: If specified, select specific speaker(s) defined
            in the corpus. Default is 'ALL' (all participants). Common choices
            are 'CHI' (the child), 'MOT' (mother), ['CHI','MOT'] (exclude
            researchers)
        :param stem: If true, then use word stems instead of word strings.
        :param relation: If true, then return tuples of (stem, index,
            dependent_index)
        :param strip_space: If true, then strip trailing spaces from word
            tokens. Otherwise, leave the spaces on the tokens.
        :param replace: If true, then use the replaced (intended) word instead
            of the original word (e.g., 'wat' will be replaced with 'watch')
        """
        sent=None
        pos=False
        return concat([self._get_words(fileid, speaker, sent, stem, relation,
            pos, strip_space, replace) for fileid in self.abspaths(fileids)])

    def tagged_words(self, fileids=None, speaker='ALL', stem=False,
            relation=False, strip_space=True, replace=False):
        """
        :return: the given file(s) as a list of tagged
            words and punctuation symbols, encoded as tuples
            ``(word,tag)``.
        :rtype: list(tuple(str,str))

        :param speaker: If specified, select specific speaker(s) defined
            in the corpus. Default is 'ALL' (all participants). Common choices
            are 'CHI' (the child), 'MOT' (mother), ['CHI','MOT'] (exclude
            researchers)
        :param stem: If true, then use word stems instead of word strings.
        :param relation: If true, then return tuples of (stem, index,
            dependent_index)
        :param strip_space: If true, then strip trailing spaces from word
            tokens. Otherwise, leave the spaces on the tokens.
        :param replace: If true, then use the replaced (intended) word instead
            of the original word (e.g., 'wat' will be replaced with 'watch')
        """
        sent=None
        pos=True
        return concat([self._get_words(fileid, speaker, sent, stem, relation,
            pos, strip_space, replace) for fileid in self.abspaths(fileids)])

    def sents(self, fileids=None, speaker='ALL', stem=False,
            relation=None, strip_space=True, replace=False):
        """
        :return: the given file(s) as a list of sentences or utterances, each
            encoded as a list of word strings.
        :rtype: list(list(str))

        :param speaker: If specified, select specific speaker(s) defined
            in the corpus. Default is 'ALL' (all participants). Common choices
            are 'CHI' (the child), 'MOT' (mother), ['CHI','MOT'] (exclude
            researchers)
        :param stem: If true, then use word stems instead of word strings.
        :param relation: If true, then return tuples of ``(str,pos,relation_list)``.
            If there is manually-annotated relation info, it will return
            tuples of ``(str,pos,test_relation_list,str,pos,gold_relation_list)``
        :param strip_space: If true, then strip trailing spaces from word
            tokens. Otherwise, leave the spaces on the tokens.
        :param replace: If true, then use the replaced (intended) word instead
            of the original word (e.g., 'wat' will be replaced with 'watch')
        """
        sent=True
        pos=False
        return concat([self._get_words(fileid, speaker, sent, stem, relation,
            pos, strip_space, replace) for fileid in self.abspaths(fileids)])

    def tagged_sents(self, fileids=None, speaker='ALL', stem=False,
            relation=None, strip_space=True, replace=False):
        """
        :return: the given file(s) as a list of
            sentences, each encoded as a list of ``(word,tag)`` tuples.
        :rtype: list(list(tuple(str,str)))

        :param speaker: If specified, select specific speaker(s) defined
            in the corpus. Default is 'ALL' (all participants). Common choices
            are 'CHI' (the child), 'MOT' (mother), ['CHI','MOT'] (exclude
            researchers)
        :param stem: If true, then use word stems instead of word strings.
        :param relation: If true, then return tuples of ``(str,pos,relation_list)``.
            If there is manually-annotated relation info, it will return
            tuples of ``(str,pos,test_relation_list,str,pos,gold_relation_list)``
        :param strip_space: If true, then strip trailing spaces from word
            tokens. Otherwise, leave the spaces on the tokens.
        :param replace: If true, then use the replaced (intended) word instead
            of the original word (e.g., 'wat' will be replaced with 'watch')
        """
        sent=True
        pos=True
        return concat([self._get_words(fileid, speaker, sent, stem, relation,
            pos, strip_space, replace) for fileid in self.abspaths(fileids)])

    def corpus(self, fileids=None):
        """
        :return: the given file(s) as a dict of ``(corpus_property_key, value)``
        :rtype: list(dict)
        """
        return [self._get_corpus(fileid) for fileid in self.abspaths(fileids)]

    def _get_corpus(self, fileid):
        results = dict()
        xmldoc = ElementTree.parse(fileid).getroot()
        for key, value in xmldoc.items():
            results[key] = value
        return results

    def participants(self, fileids=None):
        """
        :return: the given file(s) as a dict of
            ``(participant_property_key, value)``
        :rtype: list(dict)
        """
        return [self._get_participants(fileid)
                            for fileid in self.abspaths(fileids)]

    def _get_participants(self, fileid):
        # multidimensional dicts
        def dictOfDicts():
            return defaultdict(dictOfDicts)

        xmldoc = ElementTree.parse(fileid).getroot()
        # getting participants' data
        pat = dictOfDicts()
        for participant in xmldoc.findall('.//{%s}Participants/{%s}participant'
                                          % (NS,NS)):
            for (key,value) in participant.items():
                pat[participant.get('id')][key] = value
        return pat

    def age(self, fileids=None, speaker='CHI', month=False):
        """
        :return: the given file(s) as string or int
        :rtype: list or int

        :param month: If true, return months instead of year-month-date
        """
        return [self._get_age(fileid, speaker, month)
                for fileid in self.abspaths(fileids)]

    def _get_age(self, fileid, speaker, month):
        xmldoc = ElementTree.parse(fileid).getroot()
        for pat in xmldoc.findall('.//{%s}Participants/{%s}participant'
                                  % (NS,NS)):
            try:
                if pat.get('id') == speaker:
                    age = pat.get('age')
                    if month:
                        age = self.convert_age(age)
                    return age
            # some files don't have age data
            except (TypeError, AttributeError), e:
                return None

    def sex(self, fileids=None, speaker='CHI'):
        """
        :return: the given file(s) as string or int
        :rtype: list or int

        :param month: If true, return months instead of year-month-date
        """
        return [self._get_sex(fileid, speaker)
                for fileid in self.abspaths(fileids)]

    def _get_sex(self, fileid, speaker):
        xmldoc = ElementTree.parse(fileid).getroot()
        for pat in xmldoc.findall('.//{%s}Participants/{%s}participant'
                                  % (NS,NS)):
            try:
                if pat.get('id') == speaker:
                    sex = pat.get('sex')
                    return sex
            # some files don't have age data
            except (TypeError, AttributeError), e:
                return None

    def convert_age(self, age_year):
        "Caclculate age in months from a string in CHILDES format"
        m = re.match("P(\d+)Y(\d+)M?(\d?\d?)D?",age_year)
        age_month = int(m.group(1))*12 + int(m.group(2))
        try:
            if int(m.group(3)) > 15:
                age_month += 1
        # some corpora don't have age information?
        except ValueError, e:
            pass
        return age_month

    def MLU(self, fileids=None, speaker='CHI'):
        """
        :return: the given file(s) as a floating number
        :rtype: list(float)
        """
        return [self._getMLU(fileid, speaker=speaker)
                for fileid in self.abspaths(fileids)]

    def _getMLU(self, fileid, speaker):
        sents = self._get_words(fileid, speaker=speaker, sent=True, stem=True,
                    relation=False, pos=True, strip_space=True, replace=True)
        results = []
        lastSent = []
        numFillers = 0
        sentDiscount = 0
        for sent in sents:
            posList = [pos for (word,pos) in sent]
            # if any part of the sentence is intelligible
            if any(pos == 'unk' for pos in posList):
                next
            # if the sentence is null
            elif sent == []:
                next
            # if the sentence is the same as the last sent
            elif sent == lastSent:
                next
            else:
                results.append([word for (word,pos) in sent])
                # count number of fillers
                if len(set(['co',None]).intersection(posList)) > 0:
                    numFillers += posList.count('co')
                    numFillers += posList.count(None)
                    sentDiscount += 1
            lastSent = sent
        try:
            thisWordList = flatten(results)
            # count number of morphemes
            # (e.g., 'read' = 1 morpheme but 'read-PAST' is 2 morphemes)
            numWords = float(len(flatten([word.split('-')
                                          for word in thisWordList]))) - numFillers
            numSents = float(len(results)) - sentDiscount
            mlu = numWords/numSents
        except ZeroDivisionError:
            mlu = 0
        # return {'mlu':mlu,'wordNum':numWords,'sentNum':numSents}
        return mlu

    def _get_relation(self, xmlword):
        # relational
        # the gold standard is stored in
        # <mor></mor><mor type="trn"><gra type="grt">
        # original: if relation == True:
        relation = ''
        for xmlstem_rel in xmlword.findall('.//{%s}mor/{%s}gra'
                                                   % (NS, NS)):
            if not xmlstem_rel.get('type') == 'grt':
                # word = (word[0], word[1],
                #         xmlstem_rel.get('index')
                #         + "|" + xmlstem_rel.get('head')
                #         + "|" + xmlstem_rel.get('relation'))

                # store relation in token map
                relation = xmlstem_rel.get('index') \
                                    + "|" + xmlstem_rel.get('head') \
                                    + "|" + xmlstem_rel.get('relation')

                # ignore gold standard for now
                # else:
                #     word = (word[0], word[1], word[2],
                #             word[0], word[1],
                #             xmlstem_rel.get('index')
                #             + "|" + xmlstem_rel.get('head')
                #             + "|" + xmlstem_rel.get('relation'))
        try:  # what is this?
            for xmlpost_rel in xmlword.findall('.//{%s}mor/{%s}mor-post/{%s}gra'
                                                       % (NS, NS, NS)):
                if not xmlpost_rel.get('type') == 'grt':
                    # suffixStem = (suffixStem[0],
                    #               suffixStem[1],
                    #               xmlpost_rel.get('index')
                    #               + "|" + xmlpost_rel.get('head')
                    #               + "|" + xmlpost_rel.get('relation'))

                    # add suffix relation to normal relation
                    relation += ' ' + xmlpost_rel.get('index') \
                                         + "|" + xmlpost_rel.get('head') \
                                         + "|" + xmlpost_rel.get('relation')
                    # else:
                    #     suffixStem = (suffixStem[0], suffixStem[1],
                    #                   suffixStem[2], suffixStem[0],
                    #                   suffixStem[1],
                    #                   xmlpost_rel.get('index')
                    #                   + "|" + xmlpost_rel.get('head')
                    #                   + "|" + xmlpost_rel.get('relation'))
        except:
            pass

        return relation

    def _get_pos(self, xmlword, suffixStem):
        # pos
        # original if relation or pos:
        pos = ''
        try:
            xmlpos = xmlword.findall(".//{%s}c" % NS)
            # word = (word, xmlpos[0].text)
            # add pos to map
            pos = xmlpos[0].text
            if len(xmlpos) != 1 and suffixStem:
                suffixStem = (suffixStem, xmlpos[1].text)
                pos += ' ' + xmlpos[1].text  # POS of suffix
        except (AttributeError, IndexError), e:
            pass
            # we don't really do anyting with below vars...
            # word = (word, None)
            # if suffixStem:
            #     suffixStem = (suffixStem, None)
        return pos

    def _get_stem(self, xmlword):
        # stem
        stem = ''
        # original if relation or stem
        try:
            xmlstem = xmlword.find('.//{%s}stem' % NS)
            # word = xmlstem.text
            # replaces word with stem, instead add to map
            stem = xmlstem.text
        except AttributeError, e:
            pass
        # if there is an inflection
        try:
            xmlinfl = xmlword.find('.//{%s}mor/{%s}mw/{%s}mk'
                                   % (NS, NS, NS))
            # word += '-' + xmlinfl.text
            stem += '-' + xmlinfl.text
        except:
            pass
        # if there is a suffix
        try:
            xmlsuffix = xmlword.find('.//{%s}mor/{%s}mor-post/{%s}mw/{%s}stem'
                                     % (NS, NS, NS, NS))
            suffixStem = xmlsuffix.text
            stem += ' ' + suffixStem
        except AttributeError:
            suffixStem = ""
        return stem

    def get_custom_sents(self, fileid):  # speaker, sent, stem, relation, pos, strip_space, replace):
        fileid = self.abspaths([fileid])[0]
        tree = ElementTree.parse(fileid)
        xmldoc = tree.getroot()
        # processing each xml doc
        # results = []
        results2 = []
        for xmlsent in xmldoc.findall('.//{%s}u' % NS):

            utt = ()

            sentID = xmlsent.get('uID')
            sents = []
            # place this in map
            speaker = xmlsent.get('who') # ME

            utt += (sentID, speaker)

            tokens = []

            token_order = 0

            skip_replacement_counter = 0

            for xmlword in xmlsent.findall('.//{%s}w' % NS):

                # skip the replacements of a word - they've already been considered
                if skip_replacement_counter > 0:
                    skip_replacement_counter -= 1
                    continue

                token = {}

                if xmlword.get('type') == 'omission':
                    continue

                suffixStem = None

                xstr = lambda s: "" if s is None else unicode(s)

                if xmlword.find('.//{%s}langs' % (NS)):
                    xmlword.text = xmlword.find('.//{%s}langs' % (NS)).tail

                # handles compounds and ignores shortenings (?)
                text_tags = ["{%s}wk" % NS, "{%s}p" % NS, "{%s}shortening" % NS]
                if xmlword.findall('*'):
                    word_tags = xmlword.findall('*')
                    text = xstr(xmlword.text)
                    for word_tag in word_tags:
                        if word_tag.tag in text_tags:
                            if word_tag.tag == "{%s}wk" % NS:
                                text += "+"
                            text += xstr(word_tag.text) + xstr(word_tag.tail)
                    xmlword.text = text

                if xmlword.text:
                    word = xmlword.text
                    token['gloss'] = xmlword.text.strip()
                else:
                    print 'empty word in sentence %s' % sentID
                    word = ''
                    token['gloss'] = ''


                # check if this is a replacement, and then build rep, stem, etc from children
                if xmlword.find('.//{%s}replacement' % (NS)):
                    # save children in replacement field
                    # iterate over children
                    replacements = []
                    stems = []
                    pos = []
                    relations = []
                    children = xmlword.findall('.//{%s}w' % NS)
                    for child in children:
                        replacements.append(child.text)
                        stems.append(self._get_stem(child))
                        pos.append(self._get_pos(child, None))
                        relations.append(self._get_relation(child))
                    token['replacement'] = ' '.join(replacements)
                    token['stem'] = ' '.join(stems)
                    token['pos'] = ' '.join(pos)
                    token['relation'] = ' '.join(relations)

                    skip_replacement_counter = len(children)
                else: # else get stem and pos for this word
                    # word = word.strip()
                    token['stem'] = self._get_stem(xmlword)  # if suffix, should be in same column
                    token['pos'] = self._get_pos(xmlword, suffixStem)
                    token['relation'] = self._get_relation(xmlword)
                    # replacement_elems = filter(lambda x: x.tag == '{%s}w' % NS, [e for e in xmlword.iter() if e is not xmlword])
                    # replacements = [r.text for r in replacement_elems]
                    # replacement_str = ' '.join(replacements)
                    # if replacement_str:
                    #     token['replacement'] = replacement_str
                    #     skip_replacement_counter = len(replacements)
                # parent_map = dict((c, p) for p in tree.getiterator() for c in p)
                #
                # if parent_map.get(xmlword) and parent_map.get(xmlword).tag == '{%s}replacement' % NS:
                #     last_token = tokens[len(tokens) - 1]
                #     last_token['replacement'] = token['gloss']
                #     continue # don't save this token in tokens array

                        # strip tailing space
                token_order += 1
                token['order'] = token_order

                # sents.append(word)
                tokens.append(token)
                # if suffixStem:
                #     sents.append(suffixStem)
            results2.append(utt + (tokens,))
        return results2

    def _get_words(self, fileid, speaker, sent, stem, relation, pos,
            strip_space, replace):
        if isinstance(speaker, str) and speaker != 'ALL':  # ensure we have a list of speakers
            speaker = [ speaker ]
        xmldoc = ElementTree.parse(fileid).getroot()
        # processing each xml doc
        results = []
        for xmlsent in xmldoc.findall('.//{%s}u' % NS):
            sentID  = xmlsent.get('uID')
            sents = []
            # select speakers
            if speaker == 'ALL' or xmlsent.get('who') in speaker:
                for xmlword in xmlsent.findall('.//{%s}w' % NS):

                    if xmlword.get('type') == 'omission':
                        continue

                    infl = None ; suffixStem = None

                    # getting replaced words
                    xstr = lambda s: "" if s is None else unicode(s)
                    if replace and xmlword.find('.//{%s}replacement' % (NS)):
                        continue

                    if xmlword.find('.//{%s}langs' % (NS)):
                        xmlword.text = xmlword.find('.//{%s}langs' % (NS)).tail

                    text_tags = ["{%s}wk" % NS, "{%s}p" % NS, "{%s}shortening" % NS]
                    if xmlword.findall('*'):
                        word_tags = xmlword.findall('*')
                        text = xstr(xmlword.text)
                        for word_tag in word_tags:
                            if word_tag.tag in text_tags:
                                if word_tag.tag == "{%s}wk" % NS:
                                    text += "+"
                                text += xstr(word_tag.text) + xstr(word_tag.tail)
                        xmlword.text = text

                    if xmlword.text:
                        word = xmlword.text
                    else:
                        print 'empty word in sentence %s' % sentID
                        word = ''

                    # strip tailing space
                    if strip_space:
                        word = word.strip()

                    # stem
                    if relation or stem:
                        try:
                            xmlstem = xmlword.find('.//{%s}stem' % NS)
                            word = xmlstem.text
                        except AttributeError, e:
                            pass
                        # if there is an inflection
                        try:
                            xmlinfl = xmlword.find('.//{%s}mor/{%s}mw/{%s}mk'
                                                   % (NS,NS,NS))
                            word += '-' + xmlinfl.text
                        except:
                            pass
                        # if there is a suffix
                        try:
                            xmlsuffix = xmlword.find('.//{%s}mor/{%s}mor-post/{%s}mw/{%s}stem'
                                                     % (NS,NS,NS,NS))
                            suffixStem = xmlsuffix.text
                        except AttributeError:
                            suffixStem = ""
                    # pos
                    if relation or pos:
                        try:
                            xmlpos = xmlword.findall(".//{%s}c" % NS)
                            word = (word,xmlpos[0].text)
                            if len(xmlpos) != 1 and suffixStem:
                                suffixStem = (suffixStem,xmlpos[1].text)
                        except (AttributeError,IndexError), e:
                            word = (word,None)
                            if suffixStem:
                                suffixStem = (suffixStem,None)
                    # relational
                    # the gold standard is stored in
                    # <mor></mor><mor type="trn"><gra type="grt">
                    if relation == True:
                        for xmlstem_rel in xmlword.findall('.//{%s}mor/{%s}gra'
                                                           % (NS,NS)):
                            if not xmlstem_rel.get('type') == 'grt':
                                word = (word[0], word[1],
                                        xmlstem_rel.get('index')
                                        + "|" + xmlstem_rel.get('head')
                                        + "|" + xmlstem_rel.get('relation'))
                            else:
                                word = (word[0], word[1], word[2],
                                        word[0], word[1],
                                        xmlstem_rel.get('index')
                                        + "|" + xmlstem_rel.get('head')
                                        + "|" + xmlstem_rel.get('relation'))
                        try:
                            for xmlpost_rel in xmlword.findall('.//{%s}mor/{%s}mor-post/{%s}gra'
                                                               % (NS,NS,NS)):
                                if not xmlpost_rel.get('type') == 'grt':
                                    suffixStem = (suffixStem[0],
                                                  suffixStem[1],
                                                  xmlpost_rel.get('index')
                                                  + "|" + xmlpost_rel.get('head')
                                                  + "|" + xmlpost_rel.get('relation'))
                                else:
                                    suffixStem = (suffixStem[0], suffixStem[1],
                                                  suffixStem[2], suffixStem[0],
                                                  suffixStem[1],
                                                  xmlpost_rel.get('index')
                                                  + "|" + xmlpost_rel.get('head')
                                                  + "|" + xmlpost_rel.get('relation'))
                        except:
                            pass
                    sents.append(word)
                    if suffixStem:
                        sents.append(suffixStem)
                if sent or relation:
                    results.append(sents)
                else:
                    results.extend(sents)
        return results


    # Ready-to-use browser opener

    """
    The base URL for viewing files on the childes website. This
    shouldn't need to be changed, unless CHILDES changes the configuration
    of their server or unless the user sets up their own corpus webserver.
    """
    childes_url_base = r'http://childes.psy.cmu.edu/browser/index.php?url='


    def webview_file(self, fileid, urlbase=None):
        """Map a corpus file to its web version on the CHILDES website,
        and open it in a web browser.

        The complete URL to be used is:
            childes.childes_url_base + urlbase + fileid.replace('.xml', '.cha')

        If no urlbase is passed, we try to calculate it.  This
        requires that the childes corpus was set up to mirror the
        folder hierarchy under childes.psy.cmu.edu/data-xml/, e.g.:
        nltk_data/corpora/childes/Eng-USA/Cornell/??? or
        nltk_data/corpora/childes/Romance/Spanish/Aguirre/???

        The function first looks (as a special case) if "Eng-USA" is
        on the path consisting of <corpus root>+fileid; then if
        "childes", possibly followed by "data-xml", appears. If neither
        one is found, we use the unmodified fileid and hope for the best.
        If this is not right, specify urlbase explicitly, e.g., if the
        corpus root points to the Cornell folder, urlbase='Eng-USA/Cornell'.
        """

        import webbrowser, re

        if urlbase:
            path = urlbase+"/"+fileid
        else:
            full = self.root + "/" + fileid
            full = re.sub(r'\\', '/', full)
            if '/childes/' in full.lower():
                # Discard /data-xml/ if present
                path = re.findall(r'(?i)/childes(?:/data-xml)?/(.*)\.xml', full)[0]
            elif 'eng-usa' in full.lower():
                path = 'Eng-USA/' + re.findall(r'/(?i)Eng-USA/(.*)\.xml', full)[0]
            else:
                path = fileid

        # Strip ".xml" and add ".cha", as necessary:
        if path.endswith('.xml'):
            path = path[:-4]

        if not path.endswith('.cha'):
            path = path+'.cha'

        url = self.childes_url_base + path

        webbrowser.open_new_tab(url)
        print "Opening in browser:", url
        # Pausing is a good idea, but it's up to the user...
        # raw_input("Hit Return to continue")



def demo(corpus_root=None):
    """
    The CHILDES corpus should be manually downloaded and saved
    to ``[NLTK_Data_Dir]/corpora/childes/``
    """
    if not corpus_root:
        from nltk.data import find
        corpus_root = find('corpora/childes/data-xml/Eng-USA/')

    try:
        childes = CHILDESCorpusReader(corpus_root, u'.*.xml')
        # describe all corpus
        for file in childes.fileids()[:5]:
            corpus = ''
            corpus_id = ''
            for (key,value) in childes.corpus(file)[0].items():
                if key == "Corpus": corpus = value
                if key == "Id": corpus_id = value
            print 'Reading', corpus,corpus_id,' .....'
            print "words:", childes.words(file)[:7],"..."
            print "words with replaced words:", childes.words(file, replace=True)[:7]," ..."
            print "words with pos tags:", childes.tagged_words(file)[:7]," ..."
            print "words (only MOT):", childes.words(file, speaker='MOT')[:7], "..."
            print "words (only CHI):", childes.words(file, speaker='CHI')[:7], "..."
            print "stemmed words:", childes.words(file, stem=True)[:7]," ..."
            print "words with relations and pos-tag:", childes.words(file, relation=True)[:5]," ..."
            print "sentence:", childes.sents(file)[:2]," ..."
            for (participant, values) in childes.participants(file)[0].items():
                    for (key, value) in values.items():
                        print "\tparticipant", participant, key, ":", value
            print "num of sent:", len(childes.sents(file))
            print "num of morphemes:", len(childes.words(file, stem=True))
            print "age:", childes.age(file)
            print "age in month:", childes.age(file, month=True)
            print "MLU:", childes.MLU(file)
            print

    except LookupError, e:
        print """The CHILDES corpus, or the parts you need, should be manually
        downloaded from http://childes.psy.cmu.edu/data-xml/ and saved at
        [NLTK_Data_Dir]/corpora/childes/
            Alternately, you can call the demo with the path to a portion of the CHILDES corpus, e.g.:
        demo('/path/to/childes/data-xml/Eng-USA/")
        """
        #corpus_root_http = urllib2.urlopen('http://childes.psy.cmu.edu/data-xml/Eng-USA/Bates.zip')
        #corpus_root_http_bates = zipfile.ZipFile(cStringIO.StringIO(corpus_root_http.read()))
        ##this fails
        #childes = CHILDESCorpusReader(corpus_root_http_bates,corpus_root_http_bates.namelist())


if __name__ == "__main__":
    demo()
