from bottle import route, run, template, request, response
from neo4j.v1 import GraphDatabase, basic_auth
from random import *

driver = GraphDatabase.driver('bolt://localhost',auth=basic_auth("neo4j", "password"))

def get_db():
    return driver.session()

@route('/graph/<article>')
def get_graph(article):
	query = 'MATCH (p:Page {title:"%s"})<-[:Link]-(o:Page),(o) <-[:Link]-(q:Page) With o,count(q) as rel_count RETURN o.title as link_title, rel_count ORDER BY rel_count DESC LIMIT 10' % article.replace("_"," ")
	return query_db(query,article)

@route('/multigraph/<articles>')
def get_multigraph(articles):
    	articles = ("'" + ("','".join(articles.split(","))) + "'").replace("_"," ")
	query = 'WITH [%s] as pages MATCH ((p:Page)<-[:Link]-(o:Page)), (o) <-[:Link]-(q:Page) ' \
            'WHERE p.title in pages AND size(o.title) > 4 AND NOT (o.title IN pages) ' \
            'WITH o,count(q) as rel_count RETURN  o.title as link_title, rel_count ORDER BY rel_count DESC LIMIT 10' % articles
	return query_db(query,articles)

def query_db(query,params):
    db = get_db()
    results = db.run(query)
    nodes = []
    rels = []
    i = 0
    for record in results:
        nodes.append({"title": record["link_title"], "url": generateUrl(record["link_title"]), "rel_count": record["rel_count"],"rev_link": is_backlinking(params, record["link_title"])})
        target = i
        i += 1
    response.set_header('Access-Control-Allow-Origin', '*')
    return dict(pages=nodes)


def is_backlinking(parent, child):
	return "true"
	#the following code currently always returns true
	#db = get_db()
	#query = 'MATCH (p:Page {title:"%s"})<-[:Link]-(o:Page) Where o.title = "%s" RETURN true LIMIT 1' % (child.replace("_"," "), parent.replace("_"," "))
	#if db.run(query):
	#	return "true"
	#else:
	#	return "false"

def generateUrl(title):
    url_root = "https://en.wikipedia.org/wiki/"
    return url_root+title.replace(" ","_")

run(host='localhost', port=8080)
