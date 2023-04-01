
from datetime import datetime, timedelta, timezone
import feedparser
import pytz


def start_search_feed(keywords, rss_feed, days):

    try:
        
        matched_entries = {}
        matched_entry_counter = 0
        
        current_date = datetime.now(timezone.utc)
        one_month_ago = current_date - timedelta(days=days)
        
        feed = feedparser.parse(rss_feed)
        
        for entry in feed.entries:
            entry_date_str = entry.published
            try:
                entry_date = datetime.strptime(entry_date_str, '%a, %d %b %Y %H:%M:%S %z')
            except ValueError:
                entry_date = datetime.strptime(entry_date_str, '%a, %d %b %Y %H:%M:%S %Z')
                entry_date = pytz.utc.localize(entry_date).astimezone(pytz.utc)

            if entry_date < one_month_ago:
                continue

            for keyword in keywords:
                if keyword in entry.title:
                    matched_entry_counter += 1
                    matched_entries[f"Entry {matched_entry_counter}"] = {
                        'published': entry.published,
                        'title': entry.title,
                        'link': entry.link,
                        
                    }
                    break
        
        not_found_keywords = set(keywords) - set([keyword for keyword in keywords for entry in feed.entries if keyword in entry.title])
        for keyword in not_found_keywords:
            print(f"No entries found for keyword: {keyword}\n")
    
    
        for entry_num, entry in matched_entries.items():
            print(f"\nEntry {entry_num}:")
            print(f"title: {entry['title']}")
            print(f"link: {entry['link']}")
            print(f"published: {entry['published']}\n")

        return matched_entries
        
    
    except Exception as e:
        print(f"\nERROR - An error occurred in search_feed(): \n{e}")