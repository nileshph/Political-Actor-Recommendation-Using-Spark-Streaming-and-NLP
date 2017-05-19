package drew.corenlp;

import java.io.Serializable;
import java.util.List;
/**
 * News Article
 * @author nikitakothari
 *
 */
public class Document implements Serializable{

	private static final long serialVersionUID = 1L;
	private String type;
	private String doc_id;
	private String head_line;
	private String date_line;
	List<Sentence> sentences;
	private String corref;
	public String getType() {
		return type;
	}
	public void setType(String type) {
		this.type = type;
	}
	public String getDoc_id() {
		return doc_id;
	}
	public void setDoc_id(String doc_id) {
		this.doc_id = doc_id;
	}
	public String getHead_line() {
		return head_line;
	}
	public void setHead_line(String head_line) {
		this.head_line = head_line;
	}
	public String getDate_line() {
		return date_line;
	}
	public void setDate_line(String date_line) {
		this.date_line = date_line;
	}
	public List<Sentence> getSentences() {
		return sentences;
	}
	public void setSentences(List<Sentence> sentences) {
		this.sentences = sentences;
	}
	public String getCorref() {
		return corref;
	}
	public void setCorref(String corref) {
		this.corref = corref;
	}
	
}
