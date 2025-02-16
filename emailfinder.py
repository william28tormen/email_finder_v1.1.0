from bs4 import BeautifulSoup
import re
import sys
import requests

TO_CRAWL = []
CRAWLED = set()

def request(url):
    header = {'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Mobile Safari/537.36'}
    try:
        response = requests.get(url, headers=header)
        return response.text
    except KeyboardInterrupt:
        sys.exit(0)

def get_links(html):
    links = []

    try:
        soup = BeautifulSoup(html, 'html.parser')
        tags_a = soup.find_all('a', href=True)

        for tag in tags_a:
            link = tag['href']

            if link.startswith('http'):
                links.append(link)

        return links
    except:
        pass

def get_emails(html):
     emails = re.findall(r'\w[\w\.]+\w@\w[\w\.]+\w', html)
     return emails

def crawl():

    while 1:
        if TO_CRAWL:
            url = TO_CRAWL.pop()

            html = request(url)
            if html:
                links = get_links(html)
                if links:
                    for link in links:
                        if link not in CRAWLED and link not in TO_CRAWL:
                            TO_CRAWL.append(link)

                    emails = get_emails(html)
                    for email in emails:
                        print('E-mail -> {}'.format(email))

                CRAWLED.add(url)
            else:
                CRAWLED.add(url)

                print('---------------------------------------------------------')
                print('Finalizado.')
                break

if __name__ == '__main__':
    url = sys.argv[1]
    TO_CRAWL.append(url)
    crawl()