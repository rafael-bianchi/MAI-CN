import requests
from lxml import etree

def get_content(url):
    response = requests.get(url)
    if (not response.ok and (response.reason == 'Not Found' or response.reason == 'Bad Request')):
        print (f'Error: {response.text}')
        return []

    data = response.content
    tree = etree.fromstring(data)

    return tree