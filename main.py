import bs4
import requests
import yaml


def validator(link):
    r = requests.get(link)
    if r.status_code == 200:
        return True
    else:
        return False


def page_getter():
    pages = ["http://www.shakedos.co.il/tag/שאלת-בגרות/"]
    num = 2
    con = True
    while con:
        link = "http://www.shakedos.co.il/tag/שאלת-בגרות/page/%s" % (str(num))
        con = validator(link)
        if con:
            pages.append(link)
        num = num + 1
    return pages


def link_getter(web_page):
    web_page = bs4.BeautifulSoup(web_page, "html.parser")
    link_class = {"class": "media-heading entry-title"}
    links = web_page.find_all("h3", link_class)
    links = bs4.BeautifulSoup(str(links), "html.parser")
    list_of_links = []
    for link in links.find_all("a"):
        link = bs4.BeautifulSoup(str(link), "html.parser")
        list_of_links.append(str(link).split('"')[1])
    return list_of_links


def question_content(link):
    q = bs4.BeautifulSoup(((requests.get(link)).text), "html.parser")
    title = q.find("h1", {"class": "entry-title"}).text
    content = q.find("div", {"class", "entry-content"}).text
    question = {"title": str(title), "content": str(content)}
    return question


def all_pages_link_getter():
    links = []
    list_of_pages = page_getter()
    for item in list_of_pages:
        links.extend(link_getter(requests.get(item).text))
    return links


def tagger(link):
    webpage = requests.get(link)
    page = bs4.BeautifulSoup(webpage.text, "html.parser")
    page = (page.find_all("a", {"rel": "tag"}))
    tags = []
    for item in page:
        tags.append(str(item.text))
    return {link: {**question_content(link), "tags":tags}}


def main():
    out = {}
    links = all_pages_link_getter()
    for item in links:
        tags = tagger(item)
        out = {**out, **tags}
    file=open("output.yaml","w",encoding='utf8')
    yaml.dump(out,file,encoding='utf-8',allow_unicode=True,sort_keys=False)
    return out


main()
