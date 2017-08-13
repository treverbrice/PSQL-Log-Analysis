# Installation
If you're the udacity code reviewer then all you need to do is download news.py into a vagrant directory with the news database installed. You will also need to create one view: <code>create view article_list as select articles.title, count(log.path) as views from articles, log where log.path = ('/article/' || articles.slug) group by articles.title order by views desc;</code>

# Everyone else
This code uses a database that isn't publically available. You can still look at the code and its projected output but running it is probably impossible.
