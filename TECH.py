import requests
from bs4 import BeautifulSoup
from requests.exceptions import RequestException

def get_technology_info(url):
    try:
        # Kirim permintaan HTTP GET
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        
        # Menampilkan header respons untuk mendeteksi teknologi
        print("Headers:")
        for key, value in response.headers.items():
            print(f"{key}: {value}")
        
        # Menggunakan BeautifulSoup untuk memeriksa tag meta dan script
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Mengidentifikasi CMS dari meta generator
        generator = soup.find('meta', attrs={'name': 'generator'})
        if generator:
            print(f"CMS: {generator.get('content')}")
        
        # Mengidentifikasi JavaScript libraries dari tag script
        scripts = soup.find_all('script')
        for script in scripts:
            if script.get('src'):
                src = script.get('src')
                if 'jquery' in src:
                    print(f"JavaScript libraries: jQuery found in {src}")
        
        # Mengidentifikasi Font APIs dari link stylesheet
        links = soup.find_all('link')
        for link in links:
            if link.get('href') and 'googleapis' in link.get('href'):
                print(f"Font scripts: Google Font API found in {link.get('href')}")
        
    except Exception as e:
        print(f"Error: {e}")

# Ganti dengan URL yang ingin Anda periksa
print("Use the following format http://example.com or https://example.com\n")
url = input("Insert URL: ")  # Meminta pengguna untuk memasukkan URL
get_technology_info(url)

