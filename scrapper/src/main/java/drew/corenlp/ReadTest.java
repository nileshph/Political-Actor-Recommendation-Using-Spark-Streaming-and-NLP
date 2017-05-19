package drew.corenlp;

public class ReadTest {
	public static void main(String[] args) {
		RSSFeedParser parser = new RSSFeedParser(
				"http://feeds.reuters.com/Reuters/PoliticsNews");
		Feed feed = parser.readFeed();
		
		for (FeedMessage message : feed.getMessages()) {
			System.out.println(message.title);
		}

	}
}