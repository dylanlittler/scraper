# These modules are required for web scraping

from bs4 import BeautifulSoup
import requests


# Function name shows that only one site reliably works right now
def search_stackoverflow(url, tag, attribute, return_url=None):

    links_dict = {}
    links = []
    link_title = []

    r = requests.get(url)

    soup = BeautifulSoup(r.text, "lxml")

    # class_ allows user to specify which 'a' tags are required
    for link in soup.find_all(tag, class_=attribute):
        # user may specify whether a url should be appended to the link provided
        # in case a relative path is used on the site
        # return_url will only be appended if relative path is used.
        if return_url and link.get('href')[0:4] != "http":
            links.append(return_url + link.get('href'))
        else:
            links.append(link.get('href'))


    
    for link in links:
        # Based on stackoverflow url, the subdirectory is stripped and formatted
        # to make a clean title

        # index number must be set in case the last character of `link` is `/`
        # which would cause the last element after splitting to be an empty string
        if link[-1] == "/":
            index = -2
        else:
            index = -1
        link_title.append(link.split("/")[index].replace("-", " ").capitalize())

    for i in range(len(links)):
        # Dict consists of the title and link for each entry, to be formatted in HTML
        links_dict[link_title[i]] = links[i]
    return links_dict


if __name__ == "__main__":
    # Tests to be deleted once the scraper works more reliably with other sites
    print(search_stackoverflow("http://stackoverflow.com/unanswered/tagged/python", "a", "question-hyperlink"))

    r = requests.get("https://duckduckgo.com/?q=stackoverflow&t=hy&atb=v102-3&ia=about")
    soup = BeautifulSoup(r.text, "lxml")

    for link in soup.find_all("div", class_="results"):
        print(link)
