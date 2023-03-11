from flask import Flask, request, jsonify, render_template
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def scrape():
    url = request.json['url']
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    title = soup.find('title').get_text()

    description = soup.find('meta', attrs={'name': 'description'})
    if description is not None:
        site_describe = description['content']
    else:
        site_describe = None
    scrape_text = soup.get_text()
    lines = [line.strip()
             for line in scrape_text.split('\n')]
    print(lines)
    page_text = '\n'.join\
        (line for line in lines
            if len(line) > 20)
    print(page_text)
    return jsonify({'title': title, 'description': site_describe, 'page_text': page_text})


if __name__ == '__main__':
    app.run(debug=True)
