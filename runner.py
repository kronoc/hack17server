from bottle import route, run, template

def fetchLinks(article_name):
    #fetch from neo4j here
    url_root = "https://en.wikipedia.org/wiki/"
    title = "This Is A Test"
    return [{ "id": 1, "title": title, "url": generateUrl(title) }, { "id": 2, "name": "Test Item 2" }]

@route('/hack17/<article_name>')
def returnLinks(article_name):
    articles = fetchLinks(article_name)
    return dict(data=articles)

def generateUrl(title):
    url_root = "https://en.wikipedia.org/wiki/"
    return url_root+title.replace(" ","_")

run(host='localhost', port=8080)
