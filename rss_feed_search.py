from datetime import datetime, timedelta, timezone
from logs import logger, log_exception
import feedparser
import json
import pytz


@log_exception
def start_search_feed(keywords, rss_feed, days):
        
    matched_entries = {}
    matched_entry_counter = 0
    keyword_found = False  # Initialize keyword_found flag
    
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
                keyword_found = True 
                matched_entry_counter += 1
                matched_entries[f"Entry {matched_entry_counter}"] = {
                    'id': str(matched_entry_counter),
                    'published': entry.published[:-7],
                    'title': entry.title,
                    'link': entry.link,
                    
                }
                break

    filename = f'{matched_entry_counter}-{keyword}-entries.json'

    if keyword_found:
        with open(filename, 'w') as f:
            json.dump(matched_entries, f, indent=4)
            logger.info(f"- Found matching entries. Entries saved to file in current directory: {filename}")
    else:
        logger.info(f"No entries found for any of the keywords {keywords} within the date range.")
