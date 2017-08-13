'''This code uses a view, here it is: create view article_list as
select articles.title, count(log.path) as views from articles, log
where log.path = ('/article/' || articles.slug)
group by articles.title order by views desc;'''

import psycopg2

DBNAME = "news"


def top_three():
    """Returns the three most popular articles of all time."""
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("select articles.title, count(log.path) as views from articles, "
              "log where log.path = ('/article/' || articles.slug) "
              "group by articles.title order by views desc limit 3")
    '''select articles.title, count(log.path) as views from articles, log where log.path = ('/article/' || articles.slug) group by articles.title order by views desc limit 3'''  # noqa
    return c.fetchall()
    db.close()


def best_author():
    """Lists all of the site authors in order of total page views."""
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("select authors.name, sum(article_list.views) as total "
              "from authors, articles , article_list "
              "where article_list.title = articles.title and "
              "articles.author = authors.id group by authors.name "
              "order by total desc;")
    '''select authors.name, sum(article_list.views) as total from authors, articles , article_list where article_list.title = articles.title and articles.author = authors.id group by authors.name order by total desc;'''  # noqa
    return c.fetchall()
    db.close()


def error_rate():
    """Returns the date and error rate of all days with above
            a 1-percent error rate"""
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("""select not_list.date, not_list.num/ok_list.num::float*100
              as "error rate" from (select date(time) as date, status,
              count(status) as num from log group by date(time), status
              order by status limit 31) as ok_list join
              (select date(time) as date, status, count(status) as num
              from log group by date(time), status
              order by status desc limit 31) as not_list on ok_list.date
               = not_list.date group by not_list.date, not_list.num,
              ok_list.num having (not_list.num/ok_list.num::float) > 0.01;""")
    return c.fetchall()
    db.close()

print (top_three())
print '\n'
print (best_author())
print '\n'
print (error_rate())
