import json
import pprint
import re
import sys
import os
from wiki import wikidata
import pandas as pd


from ActorDictionaryCopy import ActorDictionary
reload(sys)
#sys.setdefaultencoding('utf8')

pp = pprint.PrettyPrinter(indent=2)

discard_words_set = set(['THE', 'A', 'AN', 'OF', 'IN', 'AT', 'OUT', '', ' '])


from EventCoder import EventCoder

coder = EventCoder(petrGlobal={})

another_coder = EventCoder(petrGlobal=coder.get_PETRGlobals())
N = 10
new_actor_over_time = dict()



#input_file = open('/root/Desktop/core_nlp_out_large.txt') #open('/root/test_pet')
#input_file = open('/root/test_pet2')

from StringIO import StringIO


#folder_name = '/root/Desktop/files/'
#folder_name = '/root/Desktop/dataset/'
#folder_name = '/Users/nikitakothari/Downloads/dataset_new/'

actor_dict = ActorDictionary()

class DiscoverActor:
    
    def checkprocactor(self,data,name):
        for item in data:
            if name == item:
                return 1
        return 0
    def discoverActor(self, line):

        total_new_actor_list = []
        word_dic = dict()
        processed_new_actor_list = []


        print line
        print '==================='

        if not line.startswith('{'): #skip the null entries
            print 'Not a useful line'
            return
        #pp.pprint(another_coder.encode(line))
        new_actor_count = 0
        dict_event = another_coder.encode(line)
        if dict_event is None:
            return

        new_actor_meta = dict()
        nouns = []


        for k in dict_event.keys():
            new_actor_meta['doc_id'] = k
            if 'sents' in dict_event[k]:
                if (dict_event[k]['sents'] is not None):
                    keys = dict_event[k]['sents'].keys()
                    if keys is not None:
                        for l in keys:
                            if 'meta' in dict_event[k]['sents'][l]:
                                nouns += dict_event[k]['sents'][l]['meta']['nouns_not_matched']


        new_actor_meta['new_actor'] = list(set(nouns))



        #print new_actor_meta

        new_actor_freq = dict()
        #new_actor_freq['doc_id'] = new_actor_meta['doc_id']


        total_count = 0
        for item in new_actor_meta['new_actor']:
            sentences = json.load(StringIO(line), encoding='utf-8')

            count = 0
            ner = set()
            for s in sentences['sentences']:
                #"(MONEY,$|48|million),(ORGANIZATION,United|Nations),(DATE,30|August|2016|today),(NUMBER,1.3|million),(LOCATION,Central|Africa|West|Central|Africa),(PERSON,WFP/Daouda|Guirou)"

                ner_text_list = ''

                if len(s['ner']) > 0:
                    for ner_item in s['ner'].replace('),(', ':').split(':'):
                        ner_item_list = ner_item.replace('(', '').replace(')', '').split(',')

                        if len(ner_item_list) != 2:
                            continue


                        if ner_item_list[0] == 'PERSON': # or ner_item_list[0] == 'MISC' or ner_item_list[0] == 'ORGANIZATION':
                            ner_text_list = ner_item_list[1]
                            ner = ner | set([x.strip().upper() for x in ner_text_list.split('|')])
                            ner = ner - discard_words_set




                            #ner = ner | set([x.strip().upper() for x in s['ner'].replace('ORGANIZATION', '').replace('LOCATION', '').replace('PERSON', '').replace('MISC', '').replace('DATE', '').replace('(', '').replace(')', '').replace('|', ',').split(',')])
                            #ner = ner | set([x.strip().upper() for x in ner_text_list.split('|')])
                            #ner = ner - discard_words_set

            #print ner
            new_actor_count=0
            for s in sentences['sentences']:
                #if item in ner:
                content = s['sentence']
                if item in ner:
                    count += len(re.findall(item, content.upper()))

                    if actor_dict.contains(item):
                        continue

                        #TO_DO: find NP from tree: findNP(NPParseTreeHashMap, item)
                    new_actor_freq[item] = count
                    if(count > 0):
                        new_actor_count+= 1


                        #print new_actor_freq

            new_actor = dict()
            new_actor['doc_id'] = new_actor_meta['doc_id']
            new_actor['new_actor'] = new_actor_freq

            #print  new_actor
            if (new_actor_count > 0):
                total_new_actor_list.append(new_actor)


        with open('/Users/nikitakothari/Downloads/dataset_new/new_actor.txt', 'w') as outfile:
            json.dump(total_new_actor_list, outfile)


        word_dict = dict()
        word_dict_count = dict()

        total_document = 0.0

        for item in total_new_actor_list:
            #{"new_actor": {"DHUBULIA": 2, "PRIMARY": 11, "NADIA\u00c2": 1}, "doc_id": "india_telegraph_bengal20160922.0001"}
            total_count = 0.0
            if 'new_actor' in item and 'doc_id' in item:
                total_document += 1
                for k in item['new_actor'].keys():
                    total_count += item['new_actor'][k]

                for k in item['new_actor'].keys():
                    tf = 1.00 * (item['new_actor'][k]/total_count)
                    if k not in word_dic:
                        word_dic[k] = tf
                        word_dict_count[k] = 1
                    else:
                        word_dic[k] += tf
                        word_dict_count[k] += 1



        for k in word_dic.keys():
            word_dic[k] = word_dic[k] * (word_dict_count[k]/total_document)


        word_dic_sorted = sorted(word_dic.items(), key=lambda x : (-x[1], x[0]))[:N]

        #with open('/root/Desktop/new_actor_td_df.txt', 'w') as outfile:
        #    json.dump(word_dic_sorted, outfile)

        for actor_item in  word_dic_sorted:
            actor_noun = actor_item[0]
            if actor_noun in new_actor_over_time:
                new_actor_over_time[actor_noun] += 1
            else:
                new_actor_over_time[actor_noun] = 1




        print "Start"
        print new_actor_over_time.items()
        print "end"

        for actor_name in new_actor_over_time:
            
            op=str(actor_name)
           
            if self.checkprocactor(processed_new_actor_list,op) == 0:
            #if op not in processed_new_actor_list:
                ww = wikidata()
                pob=str(ww.getProbability(actor_name))
                print "data printed by nilesh"
                print op
                print pob
                print "data printed by nilesh done"
                processed_new_actor_list.append(op)


                df = pd.read_csv('/Users/nikitakothari/Documents/angular-seed-master/app/view1/new_actor_list.csv', sep=',', names = ['id', 'value'])
                isPresent = 0
                for index, row in df.iterrows():
                    if(row['id'] == op):
                        isPresent = 1
                        break

                if(isPresent == 0):
                    with open('/Users/nikitakothari/Documents/angular-seed-master/app/view1/new_actor_list.csv', 'a') as outfile1:
                        outfile1.write("\n" + str(op) + "," + str(pob))
                        outfile1.close()

        with open('/Users/nikitakothari/Downloads/dataset_new/new_actor_td_df.txt', 'w') as outfile:
            json.dump(sorted(new_actor_over_time.items(), key=lambda x : (-x[1], x[0])), outfile)







            # from dateutil import parser
            # from datetime import datetime
            #
            # dateObject = parser.parse("")
            #
            # article_date = datetime.strftime(dateObject, '%Y%m%d')
            #
            #
            # print article_date