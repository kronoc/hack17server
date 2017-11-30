from bottle import route, run, template
from neo4j.v1 import GraphDatabase, basic_auth

driver = GraphDatabase.driver('bolt://localhost',auth=basic_auth("neo4j", "password"))

def get_db():
    return driver.session()

@route('/graph/<article>')
def get_graph(article):
    db = get_db()
#    query = 'MATCH (p:Page {title:{0}})<-[:Link]-(o:Page) RETURN o.title as link_title LIMIT {1}'.format(article, 100)
    query = 'MATCH (p:Page {title:"Ireland"})<-[:Link]-(o:Page) RETURN o.title as link'
    results = db.run(query)
    nodes = []
    rels = []
    i = 0
    for record in results:
        nodes.append({"title": record["link"], "url": generateUrl(record["link"])})
        target = i
        i += 1
    return dict(pages=nodes)

def generateUrl(title):
    url_root = "https://en.wikipedia.org/wiki/"
    return url_root+title.replace(" ","_")

run(host='localhost', port=8080)
