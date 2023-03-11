import nltk
import pandas as pd
import requests
from bs4 import BeautifulSoup
from flask import Flask, request, jsonify, render_template, Response, make_response
import json
import io
import xlsxwriter

nltk.download('punkt')

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
    page_text = '\n'.join \
        (line for line in lines
         if len(line) > 20)
    print(page_text)
    return jsonify({'title': title, 'description': site_describe, 'page_text': page_text})


@app.route('/export', methods=['POST'])
def export():
    scraped_data = request.json['data']
    export_format = request.json['format']
    df = pd.DataFrame(scraped_data)
    print(export_format)

    if export_format == 'csv':
        sentences = []
        for text in df['page_text']:
            sentences.extend(nltk.sent_tokenize(text))

        data = [{'id': i, 'text': sentence} for i, sentence in enumerate(sentences, 1)]

        new_df = pd.DataFrame(columns=['id', 'text'])

        for d in data:
            new_df = new_df.append(d, ignore_index=True)

        # Write DataFrame
        output = io.BytesIO()
        writer = pd.ExcelWriter(output, engine='xlsxwriter')
        new_df.to_excel(writer, index=False)
        writer.save()
        output.seek(0)

        response = make_response(output.getvalue())
        response.headers['Content-Disposition'] = 'attachment; filename=data.xlsx'
        response.headers['Content-Type'] = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'

        return response

    elif export_format == 'txt':
        df.to_csv('scraped_data.txt', sep='\t', index=False)

        with open('scraped_data.txt', 'rb') as file:
            file_content = file.read()

        response = Response(file_content, mimetype='text/plain')
        response.headers.set('Content-Disposition', 'attachment', filename='scraped_data.txt')

        return response

    elif export_format == 'json':
        sentences = []
        for text in df['page_text']:
            sentences.extend(nltk.sent_tokenize(text))

        data = [{'id': i, 'text': sentence} for i, sentence in enumerate(sentences, 1)]

        json_data = json.dumps(data)

        response = make_response(json_data)
        response.headers['Content-Disposition'] = 'attachment; filename=data.json'
        response.headers['Content-Type'] = 'application/json'
        return response

    else:
        return "None!"


@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    df = pd.read_excel(file)
    data = []
    for i, row in df.iterrows():
        data.append({'id': row['id'], 'text': row['text']})

    # Convert the list of dictionaries to JSON format
    json_data = json.dumps(data)

    # Create a response with the JSON data and appropriate headers
    response = make_response(json_data)
    response.headers['Content-Disposition'] = 'attachment; filename=data.json'
    response.headers['Content-Type'] = 'application/json'
    return response


if __name__ == '__main__':
    app.run(debug=True)
