"""
Utilities for doing light scrapping of Rotten Tomatoes
to get additional movie reviews with their ratings.
"""
def get_box_office_links():
    import requests
    import lxml.html
    url = "https://www.rottentomatoes.com"
    page = requests.get(url)
    doc = lxml.html.document_fromstring(page.content)
    n = doc.cssselect("#homepage-top-box-office .movie_list")
    links = set()
    for child in n[0].cssselect("a"):
        links.add(url + child.attrib["href"])
    return links


def more_reviews_available(document, pagenumber):
    button_links = document.cssselect(".btn.btn-xs.btn-primary-rt")
    found = False
    desirata = "/reviews/?page=%d&type=user" % (pagenumber,)
    for blink in button_links:
        if desirata in blink.attrib["href"]:
            found = True
    return found


def get_reviews_for_url(url, page_num=0):
    import requests
    import lxml.html
    page = requests.get(url + "/reviews/?page=%d&type=user" % (page_num,))
    doc = lxml.html.document_fromstring(page.content)
    reviews_nodes = doc.cssselect(".user_review")
    reviews = []
    for rev in reviews_nodes:
        score_node = rev.cssselect(".scoreWrapper span")[0]
        try:
            score = float(score_node.attrib["class"]) / 50.0
        except ValueError:
            # review is a want to see it, skip
            continue
        try:
            text = "\n".join(list(rev.itertext())).strip()
            reviews.append((score, text))
        except UnicodeDecodeError:
            continue
    if more_reviews_available(doc, page_num+1):
        reviews += get_reviews_for_url(url, page_num+1)
    return reviews


def get_box_office_reviews():
    links = get_box_office_links()
    all_reviews = []
    for link in links:
        all_reviews.extend(get_reviews_for_url(link))
    return all_reviews

