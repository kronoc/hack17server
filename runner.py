from bottle import route, run, template

def fetchLinks(article_name):
    #fetch from neo4j here
    return [{ "id": 1, "name": "Test Item 1" }, { "id": 2, "name": "Test Item 2" }]

@route('/hack17/<article_name>')
def returnLinks(article_name):
    articles = fetchLinks(article_name)
    return dict(data=articles)

run(host='localhost', port=8080)
