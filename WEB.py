import socket  # Mengimpor modul socket untuk operasi jaringan seperti mendapatkan alamat IP dan melakukan pencarian DNS terbalik
import requests  # Mengimpor modul requests untuk mengirim permintaan HTTP
from bs4 import BeautifulSoup  # Mengimpor BeautifulSoup dari bs4 untuk mem-parsing HTML
from urllib.parse import urlparse  # Mengimpor urlparse dari urllib.parse untuk mem-parsing URL
from requests.exceptions import RequestException  # Mengimpor RequestException untuk menangani pengecualian permintaan HTTP

def get_technology_info(url):  # Mendefinisikan fungsi get_technology_info yang menerima URL sebagai parameter
    try:
        # Mengirim permintaan HTTP GET
        response = requests.get(url, timeout=5)  # Mengirim permintaan GET ke URL dengan batas waktu 5 detik
        response.raise_for_status()  # Memeriksa apakah ada kesalahan HTTP; jika ada, akan mengangkat pengecualian
        
        # Menggunakan BeautifulSoup untuk memeriksa tag meta dan title
        soup = BeautifulSoup(response.text, 'html.parser')  # Menguraikan konten HTML dari respons menggunakan BeautifulSoup
        
        # Mendapatkan judul situs
        title = soup.title.string if soup.title else 'Unknown'  # Mengambil judul halaman jika ada, jika tidak, mengembalikan 'Unknown'
        print(f"Site Title: {title}")  # Mencetak judul situs
        
        # Mem-parsing URL
        parsed_url = urlparse(url)  # Mem-parsing URL untuk mendapatkan komponen seperti netloc (domain)
        url = parsed_url.netloc  # Mengambil domain dari URL yang telah di-parse
        
        # Mendapatkan alamat IP
        ip_address = socket.gethostbyname(url)  # Mendapatkan alamat IP dari domain
        print(f"IP Address: {ip_address}")  # Mencetak alamat IP
        
        try:
            # Mencoba mendapatkan domain melalui pencarian DNS terbalik
            domain = socket.gethostbyaddr(ip_address)  # Mendapatkan domain melalui pencarian DNS terbalik menggunakan alamat IP
            print(f"Domain    : {domain[0]}")  # Mencetak domain yang ditemukan
        except socket.herror:
            # Menangani kasus di mana pencarian DNS terbalik gagal
            print(f"Domain    : {url}")  # Jika pencarian DNS terbalik gagal, mencetak domain yang digunakan dalam URL
        
        # Menampilkan header untuk mendeteksi info server
        server = response.headers.get('Server', 'Unknown')  # Mendapatkan informasi server dari header respons
        print(f"Web Server: {server}")  # Mencetak informasi server
        
        # Mengidentifikasi CMS dari meta generator
        generator = soup.find('meta', attrs={'name': 'generator'})  # Mencari tag meta dengan atribut name="generator" untuk mendeteksi CMS
        if generator:
            print(f"CMS       : {generator.get('content')}")  # Jika tag meta ditemukan, mencetak konten yang menunjukkan CMS
        
        # Mendeteksi keberadaan Cloudflare dari header
        if 'CF-RAY' in response.headers or 'Server' in response.headers and 'cloudflare' in response.headers['Server'].lower():
            # Jika header CF-RAY ada atau server menyebutkan 'cloudflare', Cloudflare terdeteksi
            print("Cloudflare: Detected")  # Mencetak bahwa Cloudflare terdeteksi
        else:
            print("Cloudflare: Not detected")  # Jika tidak, mencetak bahwa Cloudflare tidak terdeteksi
        
        # Memeriksa robots.txt
        #robots_url = f"{url}/robots.txt"  # Membentuk URL untuk robots.txt
        #try:
        #    robots_response = requests.get(robots_url, timeout=5)  # Mengirim permintaan GET untuk robots.txt dengan batas waktu 5 detik
        #    if robots_response.status_code == 200:
        #        print("robots.txt: Found")  # Jika respons adalah 200 OK, mencetak bahwa robots.txt ditemukan
        #    else:
        #        print("robots.txt: Not found")  # Jika tidak, mencetak bahwa robots.txt tidak ditemukan
        #except RequestException:
        #    print("robots.txt: Not found")  # Jika permintaan gagal, mencetak bahwa robots.txt tidak ditemukan
        
    except RequestException as e:
        print(f"Error: {e}")  # Menangani pengecualian permintaan HTTP dan mencetak pesan kesalahan

# Mengganti dengan URL yang ingin Anda periksa
print("Use the following format http://example.com or https://example.com\n")
url = input("Insert URL: ")  # Meminta pengguna untuk memasukkan URL
get_technology_info(url)  # Memanggil fungsi get_technology_info dengan URL yang dimasukkan pengguna

