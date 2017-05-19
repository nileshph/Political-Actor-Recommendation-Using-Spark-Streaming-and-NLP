package drew.corenlp;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.Properties;

import edu.stanford.nlp.dcoref.CorefChain;
import edu.stanford.nlp.dcoref.CorefCoreAnnotations.CorefChainAnnotation;
import edu.stanford.nlp.ling.CoreAnnotations.LemmaAnnotation;
import edu.stanford.nlp.ling.CoreAnnotations.NERIDAnnotation;
import edu.stanford.nlp.ling.CoreAnnotations.NamedEntityTagAnnotation;
import edu.stanford.nlp.ling.CoreAnnotations.PartOfSpeechAnnotation;
import edu.stanford.nlp.ling.CoreAnnotations.SentencesAnnotation;
import edu.stanford.nlp.ling.CoreAnnotations.TextAnnotation;
import edu.stanford.nlp.ling.CoreAnnotations.TokensAnnotation;
import edu.stanford.nlp.ling.CoreLabel;
import edu.stanford.nlp.pipeline.Annotation;
import edu.stanford.nlp.pipeline.StanfordCoreNLP;
import edu.stanford.nlp.semgraph.SemanticGraph;
import edu.stanford.nlp.semgraph.SemanticGraphCoreAnnotations.CollapsedCCProcessedDependenciesAnnotation;
import edu.stanford.nlp.trees.Tree;
import edu.stanford.nlp.trees.TreeCoreAnnotations.TreeAnnotation;
import edu.stanford.nlp.util.CoreMap;
import edu.stanford.nlp.util.TypesafeMap.Key;

/**
 * 
 * @author nikitakothari
 *
 */
public class CoreNLP {

	static public List<Sentence> process(String text) {
		Properties props = new Properties();
		props.put("annotators", "tokenize, ssplit, pos, lemma, ner, parse, dcoref");
		StanfordCoreNLP pipeline = new StanfordCoreNLP(props);
		Annotation document = new Annotation(text);
		pipeline.annotate(document);

		List<CoreMap> sentences = document.get(SentencesAnnotation.class);
		List<Sentence> sentences2 = new ArrayList<Sentence>();
		int id = 1;
		for (CoreMap sentence : sentences) {
			Tree tree = sentence.get(TreeAnnotation.class);
			SemanticGraph dependencies = sentence.get(CollapsedCCProcessedDependenciesAnnotation.class);
			String word = "";
			String lemma = "";
			String ner = "";
			for (CoreLabel token : sentence.get(TokensAnnotation.class)) {
				word += token.get(TextAnnotation.class) + ",";
				lemma += token.get(LemmaAnnotation.class) + ",";
				String ne = token.get(NamedEntityTagAnnotation.class);
				if (!ne.equals("O")) {
					ner += "(" + ne + "," + token.get(TextAnnotation.class) + ")";
				}
			}
			
			try{
			Sentence sen = new Sentence();
			sen.setSentence_id("" + id);
			sen.setParse_sentence(tree.toString());
			sen.setDependency_tree(dependencies.toString());
			sen.setToken(word);
			sen.setLemma(lemma);
			sen.setNer(ner);
			sen.setSentiment(-1);
			sen.setRelation("");
			sentences2.add(sen);
			sen.setSentence(sentence.get(TextAnnotation.class));
			}catch(NullPointerException e){
				sentences2.add(new Sentence());
			}
			
			id++;
		}
		return sentences2;
	}

	public static void main(String[] args) throws IOException {
		Properties props = new Properties();
		props.put("annotators", "tokenize, ssplit, pos, lemma, ner, parse, dcoref");
		StanfordCoreNLP pipeline = new StanfordCoreNLP(props);

		String text = "In this day and age, getting elected president of the United States is kind of like winning a golden ticket that brings you immeasurable wealth if you can make it through one or two hellish terms in office. It has become standard practice over the past few decades for presidents to cash in that golden ticket after leaving the White House.";
		Annotation document = new Annotation(text);
		pipeline.annotate(document);
		List<CoreMap> sentences = document.get(SentencesAnnotation.class);
		String word = "";
		String lemma = "";
		String ner = "";
		for (CoreMap sentence : sentences) {
			for (CoreLabel token : sentence.get(TokensAnnotation.class)) {
				String pos = token.get(PartOfSpeechAnnotation.class);
				String ne = token.get(NamedEntityTagAnnotation.class);
				word += token.get(TextAnnotation.class) + ",";
				lemma += token.get(LemmaAnnotation.class) + ",";
				if (!ne.equals("O")) {
					ner += "(" + ne + "," + token.get(TextAnnotation.class) + ")";
				}
			}
			System.out.println(sentence.get(TextAnnotation.class));
			System.out.println(word);
			System.out.println(lemma);
			System.out.println(ner);
		}
		Map<Integer, CorefChain> graph = document.get(CorefChainAnnotation.class);
	}

}
