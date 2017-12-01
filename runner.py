from bottle import route, run, template
from neo4j.v1 import GraphDatabase, basic_auth
from random import *

driver = GraphDatabase.driver('bolt://localhost',auth=basic_auth("neo4j", "password"))

def get_db():
    return driver.session()

@route('/graph/<article>')
def get_graph(article):
    db = get_db()
    query = 'MATCH (p:Page {title:"%s"})<-[:Link]-(o:Page),(o) <-[:Link]-(q:Page) With o,count(q) as rel_count RETURN o.title as link_title, rel_count' % article.replace("_"," ")
#    query = 'MATCH (p:Page {title:"%s"})<-[:Link]-(o:Page) RETURN o.title as link' % article.replace("_"," ")
    results = db.run(query)
    nodes = []
    rels = []
    i = 0
    for record in results:
        nodes.append({"title": record["link_title"], "url": generateUrl(record["link_title"]), "rel_count": record["rel_count"],"rev_link": "true"})
#        nodes.append({"title": record["link"], "url": generateUrl(record["link"]), "rel_count": randint(1, 100), "rev_link": "true"})
        target = i
        i += 1
    return dict(pages=nodes)

def get_links_count(article):
    db = get_db()
    query = 'MATCH (p:Page {title:"%s"})<-[:Link]-(o:Page) RETURN count(o)' % article.replace("_"," ")
    result = db.run(query)
    return result


def generateUrl(title):
    url_root = "https://en.wikipedia.org/wiki/"
    return url_root+title.replace(" ","_")

run(host='localhost', port=8080)
