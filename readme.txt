 
Abstract— Extracting a structured event and its actor is an interesting domain in computer sciences. The efficient approach to implement this is by using dictionaries. But the vital complication is to update the dictionaries.  Our project implements a methodology to extend the dictionary (CAMEO) which contains political actors. The framework identifies new political actors using Automatic Content Extraction. We detect a political event using PETRARCH[1] and a new actor is identified by comparisons with CAMEO[2]. We have implemented a ‘bag of words’ based ML model which verifies the political actor. In turn, our system recommends new political actors from online political news articles periodically.
Keywords— content extraction; dictionary; political actors; 
I.	INTRODUCTION 

The political event data is encoded from various news reports in real time. This is achieved using real time Spark streaming. The data is converted in the ‘who did/said what to whom’ using PETRACH. Stanford CoreNLP[3] libraries are used to extract semantic information about the actors. The actors identified are compared with the actors present in CAMEO[2]. The new actors will be  verified using naïve bayes model which uses ‘bag of words’ technique. Finally, the new verifed actors will be recommended and added to the CAMEO[2] dictionary.  

II.	BACKGROUND
Practnlptools 1.0[9] is a practical Natural Language Processing tool. These tools enable us to perform syntactic parsing, part-of-speech tagging, dependency parsing and semantic role labeling in Python.
Stanford CoreNLP [3] is used to apply various linguistic analysis tools to a piece of text. Some of the tools integrated by Stanford CoreNLP include part-of-speech (POS) tagger, the named entity recognizer (NER), the parser, the reference resolution system, sentiment analysis, bootstrapped pattern learning, and the open information extraction tools.
CAMEO[2] (Conflict and Mediation Event Observations) is an event data coding framework, mostly used for the study of political news and in general news coverage. It consists of a systematic hierarchical coding scheme for dealing with substate actors. It consists of dictionaries which consist of actors and verbs. While using CAMEO[2], initially the structure of the sentence will be parsed to get the appropriate actors and verbs. This acquired data will be searched in the corresponding dictionary. If the search is successful, the acquired data will be used further for formulating an event.   
PETRARCH[1] is a Python language event data coding software. Using Standard CoreNLP, PETRARCH performs word disambiguation to give more accurate event coding.
Apache Spark[6] is an open source cluster computing framework. It bypasses the limitations introduced by MapReduce paradigm by providing the facility of a distributed shared memory. It acts as an effective framework for data analytics.
Apache Kafka[7] is an open source stream processing framework. It can be effectively used for capturing real-time data feeds. It can be integrated into enterprise-level infrastructures in order to efficiently capture data flowing to the existent systems.

III.	FRAMEWORK
Scrapper: Scrapper collects news articles from web and extract the vital information from it. The scrapper runs periodically to collect the real time articles.   
Extraction of MetaData using CoreNLP: CoreNLP parses the data and extract metadata like parts of speech tagging, parsed tree, names entity relationship. We are using NER in our framework. NER categorises the content into name of person, organization, location, etc. We are using NER because it gives higher accuracy compare to other similar tools.
PETRARCH: It is used to deduce the political events from different articles. The actors present in those events are compared to the actors in CAMEO[2]. The actors which not present in CAMEO[2] are given as the output.
Detection of new political actors: The actors given as the new actors from Petrarch are compared with the actors given by NER. The intersection of those actors will be taken to output the final new actors. 
Bag of words(Naïve Bayes[8]): A machine learning model is created using naïve bayes. The model is trained and have been stored. The new actors from the earlier detection is passed to this model to predict the actor is a political actor or not with its probability of being a political actor. 
Naïve Bayes Model: In this module, we use the data associated with an actor available on Wikipedia as an external knowledge base. The main motive behind formulating this module is to verify and strengthen the prediction made by NER and PETRARCH[1]. We collect the information like careers, posts, organizations, political parties, etc about the actors present in CAMEO dictionary. Once we get the data, we compute a TF/IDF vector for the data received for each actor. In order to do this, we used the Bag of Word approach. Using these TF/IDF vectors as training data, we build a Naïve Bayes[8] model. Now, when we receive the predicted actor from PETRARCH[1], our purpose is to verify, based on the data available on web, whether the prediction is correct or not. Along with the prediction, we also check the accuracy with which the actor is allotted that particular label i.e. political or non-political. For the newly discovered actor, we perform the same procedure. That is, we compose a TF/IDF vector from the data acquired from Wikipedia and test it against the model we generated before. Special case to this scenario is when the newly discovered actor is not found on Wikipedia. In such a case, we consider that this module will not contribute to the overall score.

IV.	EXPERIMENTATION AND RESULTS
We have currently trained the Naïve Byes model using the data obtained from Wikipedia for 100 actors with a blend of political and non-political actors. We tested the built model using K-fold cross-validation with different K and the results were as follows:

Train/Test Split	Accuracy
90:10	100
80:20	100
70:30	96.66
60:40	97.5
Table 1: ML Classifier Accuracy Results

Taking a look at the above readings, we find that the accuracy for actors with Wikipedia page is high. But this method won’t be valid for actors who don’t have a Wikipedia page created yet. This is currently being considered as a future scope for this system.
We get the accuracy in terms of the probability of the actor being close to the positive label (i.e. political).Using this accuracy, we visualize the overall result in the form of a Bubble Chart [10]. For the purpose of plotting efficiently, we consider the accuracy as a size parameter. Following is the screenshot for one of the simulation results:

V.	CONCLUSION AND FUTURE WORKS
This system currently focuses only on the actors in the political field. It can be extended to identify actors in other fields as well. Also, in the Naïve Bayes[8] module, we may consider other knowledge base, specific to that particular field as opposed to the generalized knowledge present on Wikipedia. Further enhancement can be done on the system by choosing a different model instead of a Naïve Bayes[8] classifier in order to improve the accuracy.
VI. ACKNOWLEDGMENT
This system is considered as a partial implementation of the framework proposed in the paper ‘Discover New Actors In Politics: A Framework To Recommend Political Actors With Role In Real-time’ [4]. This system was implemented with the help of Open Event Data GitHub repository [5].

VII. REFERENCES

[1]	PETRARCH, “https://openeventdata.github.io/”
[2]	CAMEO. Con.ict and Mediation Event Observations (CAMEO) Codebook.CAMEO.”h.p://eventdata.parusanalytics.com/data.dir/cameo.html”.
[3]	Stanford. Stanford CoreNLP. ”h.p://nlp.stanford.edu/so.ware/corenlp”, “https://stanfordnlp.github.io/CoreNLP/”
[4]	Mohiuddin Solaimani1, Sayeed Salam1, Latifur Khan1,Patrick T. Brandt2 and Vito D’Orazio2, Discover New Actors In Politics: A Framework To Recommend Political Actors With Role In Real-time. 
[5]	Open Event Data, “https://openeventdata.github.io/”
[6]	Apache Spark, “https://en.wikipedia.org/wiki/Apache_Spark”
[7]	Apache Kafka,“ https://en.wikipedia.org/wiki/Apache_Kafka”
[8]	Naïve Bayes, “https://en.wikipedia.org/wiki/Naive_Bayes_classifier”
[9]	practNLPtools,  “https://pypi.python.org/pypi/practnlptools/1.0”
[10] Bubble Chart, “https://bl.ocks.org/mbostock/4063269”
































 



				
