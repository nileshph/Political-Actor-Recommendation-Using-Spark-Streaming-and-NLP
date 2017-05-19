package drew.corenlp;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;
import java.util.Properties;
import java.util.concurrent.BlockingQueue;
import java.util.concurrent.LinkedBlockingQueue;

import org.json.simple.parser.ParseException;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.google.common.collect.Lists;
import kafka.producer.KeyedMessage;
import kafka.producer.ProducerConfig;
import scala.actors.scheduler.DaemonScheduler;

/**
 * 
 * @author nikitakothari
 *
 */
public class generateData {

	private static final String topic = "news-article";

	public void run() throws InterruptedException, ParseException {

		Properties properties = new Properties();
		properties.put("metadata.broker.list", "localhost:9092");
		properties.put("serializer.class", "kafka.serializer.StringEncoder");
		properties.put("client.id", "camus");
		ProducerConfig producerConfig = new ProducerConfig(properties);
		kafka.javaapi.producer.Producer<String, String> producer = new kafka.javaapi.producer.Producer<String, String>(
				producerConfig);

		BlockingQueue<String> queue = new LinkedBlockingQueue<String>(10000);
		/*
		 * RSSFeedParser parser = new RSSFeedParser(
		 * "http://feeds.reuters.com/Reuters/PoliticsNews"); Feed feed =
		 * parser.readFeed(); String text = feed.getDescription(); for
		 * (FeedMessage message : feed.getMessages()) { text += message.title; }
		 * long docId = new Date().getTime(); List<Sentence> sentences = new
		 * ArrayList<Sentence>(); sentences = CoreNLP.process(text); Document
		 * document = new Document(); document.setType(feed.getLanguage());
		 * document.setDoc_id("" + docId);
		 * document.setHead_line(feed.getTitle());
		 * document.setDate_line(feed.getPubDate());
		 * document.setSentences(sentences); document.setCorref("");
		 * ObjectMapper mapper = new ObjectMapper();
		 */
		try {
			// String jsonInString = mapper.writeValueAsString(document);
			for (int i = 1; i <= 9; i++) {
				FileReader in = new FileReader(i + ".txt");
				BufferedReader br = new BufferedReader(in);

				String line;
				while ((line = br.readLine()) != null) {
					System.out.println(line);
					producer.send(new KeyedMessage<String, String>(topic, line));
				}
			}
		} catch (IOException e) {
			e.printStackTrace();
		}

	}

	public static void main(String[] args) {
		generateData generateData = new generateData();
		try {
			generateData.run();
		} catch (InterruptedException e) {
			e.printStackTrace();
		} catch (ParseException e) {
			e.printStackTrace();
		}
	}
}
