#!/usr/bin/env python2
'''This code uses a view, here it is: create view article_list as
select articles.title, count(log.path) as views from articles, log
where log.path = ('/article/' || articles.slug)
group by articles.title order by views desc;'''

import psycopg2


def connect():
    """conect to the psql database"""
    try:
        db = psycopg2.connect(database="news")
        c = db.cursor()
        return db, c
    except psycopg2.Error as e:
        print "can't connect to database"
        sys.exit(1)


def get_query(query):
    """takes a query and returns its result"""
    db, c = connect()
    c.execute(query)
    to_return = c.fetchall()
    db.close()
    return to_return


def print_top_three():
    """Returns the three most popular articles of all time."""
    top_three = get_query("""select articles.title, count(log.path) as views
                          from articles, log where log.path =
                          ('/article/' || articles.slug) group by
                          articles.title order by views desc limit 3""")
    '''select articles.title, count(log.path) as views from articles, log where log.path = ('/article/' || articles.slug) group by articles.title order by views desc limit 3'''  # noqa
    list_order = 1
    print '\n' + "Top Three Articles"
    for list_item in top_three:
        print (str(list_order) + '. ' + str(list_item)[1:-2] + ' views')
        list_order += 1


def print_best_author():
    """Lists all of the site authors in order of total page views."""
    best_author = get_query("""select authors.name, sum(article_list.views)
                            as total from authors, articles , article_list
                            where article_list.title = articles.title and
                            articles.author = authors.id group by authors.name
                            order by total desc;""")
    '''select authors.name, sum(article_list.views) as total from authors, articles , article_list where article_list.title = articles.title and articles.author = authors.id group by authors.name order by total desc;'''  # noqa
    list_order = 1
    print '\n' + "Best Authors"
    for list_item in best_author:
        phrase_order = 0
        for phrase in list_item:
            if phrase_order == 0:
                name = phrase
                phrase_order = 1
            else:
                view_count = str(phrase)
                print (str(list_order) + '. ' + name + ': ' +
                       view_count + ' total views')
                list_order += 1


def print_error_rate():
    """Returns the date and error rate of all days with above
        a 1-percent error rate"""
    error_rate = get_query("""select not_list.date, not_list.num/ok_list.num::float*100
              as "error rate" from (select date(time) as date, status,
              count(status) as num from log group by date(time), status
              order by status limit 31) as ok_list join
              (select date(time) as date, status, count(status) as num
              from log group by date(time), status
              order by status desc limit 31) as not_list on ok_list.date
               = not_list.date group by not_list.date, not_list.num,
              ok_list.num having (not_list.num/ok_list.num::float) > 0.01;""")
    list_order = 1
    print '\n' + "Days With Error Rate > 1%"
    for list_item in error_rate:
        phrase_order = 0
        for phrase in list_item:
            if phrase_order == 0:
                name = str(phrase)
                phrase_order = 1
            else:
                view_count = str(phrase)[:4]
                print (str(list_order) + '. ' + name + ': ' + view_count + '%')
                list_order += 1

if __name__ == '__main__':
    print_top_three()
    print_best_author()
    print_error_rate()
