from bottle import route, run, template

@route('/hack17/<article_name>')
def returnLinks(article_name):
    articles = fetchLinks(article_name)
    return dict(data=articles)

def fetchLinks(article_name):
    titles = queryGraph(article_name)
    title = titles[0]
    return [{ "id": 1, "title": titles[0], "url": generateUrl(titles[0]) }, { "id": 2, "name": titles[1], "url": generateUrl(titles[1]) }]

def queryGraph(article_name):
    root_title = article_name.replace("_"," ")    
    titles = ["Perl","Python","Java","C++","Whitespace","OS/2 Warp"]
    return titles

def generateUrl(title):
    url_root = "https://en.wikipedia.org/wiki/"
    return url_root+title.replace(" ","_")

run(host='localhost', port=8080)
