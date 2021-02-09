# News Aggregator

### Basically Google News if Google News was good

---

Page should support various sections:
* Ireland
* US
* World
* Markets
* Sports
* Science
* Technology
* etc

---

### RSS Feeds
Financial Times - https://www.ft.com/news-feed?format=rss

Economist - https://www.economist.com/rss

The Guardian - https://www.theguardian.com/help/feeds

New York Times - https://archive.nytimes.com/www.nytimes.com/services/xml/rss/index.html

Washington Post - https://www.washingtonpost.com/discussions/2018/10/12/washington-post-rss-feeds/

Reuters - https://www.reutersagency.com/en/reutersbest/reuters-best-rss-feeds/

BBC - https://www.bbc.co.uk/news/10628494

Irish Times - https://www.irishtimes.com/cmlink/news-1.1319192

---

### Architecture

Backend
* Python script to fetch news ✔️
  * Will need site specific parsers ✔️
  * Sends parsed rss feeds to db ✔️
* Python script to delete old articles from db (run every 24 hours) ✔️
* MongoDB to store past 24 hours news ✔️
* Python API to query db (from react) ✔️
* Python control script (cron job)
  * schedules document fetch and database wipe

Frontend
* React (next.js)
  * R1
    * Homepage
  * R2
    * Sections
  * R3
    * Login
    * Preferred news feeds
  * R4
    * Tailored newsfeed
