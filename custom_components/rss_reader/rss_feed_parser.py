import feedparser

def fetch_feed_sync(feed_url):
    feed = feedparser.parse(feed_url)
    if feed.entries:
        entry = feed.entries[0]
        return {
            "title": entry.title,
            "summary": entry.summary,
            "link": entry.link,
            "published": entry.published
        }
    return None