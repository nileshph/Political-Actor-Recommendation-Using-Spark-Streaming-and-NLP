package drew.corenlp;

import java.io.Serializable;
/**
 * 
 * @author nikitakothari
 *
 */
public class Sentence implements Serializable{
	
	private static final long serialVersionUID = 1L;
	private String sentence_id;
	private String sentence;
	private String parse_sentence;
	private String dependency_tree;
	private String token;
	private String lemma;
	private String ner;
	private String relation;
	private int sentiment;
	public String getSentence_id() {
		return sentence_id;
	}
	public void setSentence_id(String sentence_id) {
		this.sentence_id = sentence_id;
	}
	public String getSentence() {
		return sentence;
	}
	public void setSentence(String sentence) {
		this.sentence = sentence;
	}
	public String getParse_sentence() {
		return parse_sentence;
	}
	public void setParse_sentence(String parse_sentence) {
		this.parse_sentence = parse_sentence;
	}
	public String getDependency_tree() {
		return dependency_tree;
	}
	public void setDependency_tree(String dependency_tree) {
		this.dependency_tree = dependency_tree;
	}
	public String getToken() {
		return token;
	}
	public void setToken(String token) {
		this.token = token;
	}
	public String getLemma() {
		return lemma;
	}
	public void setLemma(String lemma) {
		this.lemma = lemma;
	}
	public String getNer() {
		return ner;
	}
	public void setNer(String ner) {
		this.ner = ner;
	}
	public String getRelation() {
		return relation;
	}
	public void setRelation(String relation) {
		this.relation = relation;
	}
	public int getSentiment() {
		return sentiment;
	}
	public void setSentiment(int sentiment) {
		this.sentiment = sentiment;
	}
	
}
