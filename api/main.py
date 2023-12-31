import requests
from bs4 import BeautifulSoup
import pandas as pd
from flask import Flask, render_template, send_file, redirect

app = Flask(__name__)

def scrape_title(url):
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        semua_judul_elemen = soup.find_all('h2', class_='entry-title')

        judul_list = []

        for judul_elemen in semua_judul_elemen[:3]:
            link_elemen = judul_elemen.find('a')

            if link_elemen:
                judul = link_elemen.text.strip()

                judul_list.append(judul)

        return judul_list
    else:
        return None, None

@app.route('/')
def index():
    df = pd.read_excel('hasil_scraping.xlsx') 
    hasil = df if not df.empty else None
    return render_template('index.html', hasil=hasil)

@app.route('/scrape', methods=['POST'])
def scrape():
    base_url = 'https://leravio.com/blog'
    page_number = 1

    judul_total = []

    current_url = f'{base_url}/page/1'
    print(f'Scraping {current_url}')
        
    judul = scrape_title(current_url)

    if judul:
        judul_total.extend(judul)

    # while True:
    #     current_url = f'{base_url}/page/{page_number}'
    #     print(f'Scraping {current_url}')
        
    #     judul, topic = scrape_title(current_url)

    #     if judul and topic:
    #         judul_total.extend(judul)
    #         topic_total.extend(topic)
    #     else:
    #         break

    #     next_page = page_number + 1
    #     next_page_url = f'{base_url}/page/{next_page}'
        
    #     next_page_response = requests.get(next_page_url)
    #     if next_page_response.status_code != 200:
    #         break 
        
    #     page_number += 1

    df = pd.DataFrame({'Judul': judul_total})
    df.to_excel('hasil_scraping.xlsx', index=False)

    return redirect('/')

@app.route('/download_result')
def download_result():
    return send_file('../hasil_scraping.xlsx', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
