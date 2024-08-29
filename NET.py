import scapy.all as scapy  # Mengimpor seluruh modul Scapy yang digunakan untuk melakukan scan jaringan, khususnya untuk mengirim paket ARP 
# ARP (Address Resolution Protocol) = protokol jaringan yang digunakan untuk menemukan alamat fisik (MAC address) dari perangkat dijaringan lokal (LAN) berdasarkan alamat IP-nya.
# API ((Application Programming Interface) ) memungkinkan interaksi antara perangkat lunak melalui permintaan dan respons dalam jaringan, seringkali menggunakan protokol standar seperti HTTP/HTTPS.
import re  # Mengimpor modul regular expression (regex) untuk memvalidasi input IP address range.
import requests  # Mengimpor modul requests yang digunakan untuk melakukan permintaan HTTP, digunakan di sini untuk mendapatkan informasi vendor MAC.
import time  # Mengimpor modul time yang digunakan untuk menambahkan delay antara permintaan API, guna mencegah pembatasan rate API.
from requests.exceptions import RequestException # Mengimpor RequestException, pengecualian umum untuk menangani kesalahan HTTP di pustaka requests.

# Pola Ekspresi Reguler untuk mengenali alamat IPv4.
ip_add_range_pattern = re.compile("^(?:[0-9]{1,3}\.){3}[0-9]{1,3}/[0-9]*$")  
# Membuat pola regex untuk mengenali rentang alamat IPv4. Pola ini memvalidasi bahwa alamat IP mengikuti format IPv4 standar dengan subnet mask (CIDR).

def get_vendor(mac):  # Mendefinisikan fungsi untuk mendapatkan informasi vendor berdasarkan alamat MAC.
    
    # Ambil informasi vendor dari API eksternal
    try:
        response = requests.get(f"https://api.macvendors.com/{mac}")  
        # Melakukan permintaan HTTP GET ke API macvendors.com untuk mendapatkan informasi vendor dari alamat MAC yang diberikan.
        if response.status_code == 200:  
            # Memeriksa apakah status kode HTTP adalah 200 (OK), menunjukkan bahwa permintaan berhasil dan respons API valid.  
            vendor = response.text.strip()  
            # Mengambil teks dari respons API dan menghapus spasi kosong di sekitarnya untuk mendapatkan nama vendor.
            if vendor:  
                # Memeriksa apakah teks respons tidak kosong.
                return vendor  
                # Mengembalikan nama vendor jika tersedia.
            else:
                return "Unknown Vendor"  
                # Jika teks respons kosong, mengembalikan "Unknown Vendor" sebagai informasi vendor yang tidak diketahui.
        else:
            return "Unknown Vendor"  
            # Jika status kode HTTP bukan 200, mengembalikan "Unknown Vendor" karena permintaan gagal atau API tidak dapat memberikan informasi yang diinginkan.
    except RequestException as e:  
        # Menangani pengecualian yang mungkin terjadi selama permintaan API.
        print(f"Error occurred: {e}")  
        # Mencetak pesan kesalahan untuk debugging jika terjadi masalah saat melakukan permintaan API.
        return "Unknown Vendor"  
        # Mengembalikan "Unknown Vendor" jika terjadi pengecualian selama permintaan API.


def scan_network(ip_range):  # Mendefinisikan fungsi untuk memindai jaringan pada rentang IP tertentu menggunakan ARP.
    print(f"\nScanning {ip_range}...")  
    # Menampilkan pesan ke layar yang menunjukkan rentang IP yang sedang dipindai.
    
    # Menekan output Scapy dengan mengatur verbose ke 0
    scapy.conf.verb = 0  
    # Mengatur verbose Scapy ke 0 untuk menekan output verbose.
    arp_result = scapy.arping(ip_range)  
    # Melakukan scan ARP pada rentang IP yang diberikan. `arping` mengirimkan paket ARP dan mengumpulkan respons.
    return arp_result  
    # Mengembalikan hasil scan ARP.

def display_results(results):  # Mendefinisikan fungsi untuk menampilkan hasil scan ARP.
    print(f"\n{'IP Address':<20} {'MAC Address':<20} {'Vendor':<30}")  
    # Menampilkan header tabel dengan kolom untuk alamat IP, alamat MAC, dan vendor.
    print("-" * 67)  
    # Menampilkan garis pemisah untuk tabel.
    for _, response in results[0]:  # Mengiterasi melalui setiap respons ARP. `results[0]` adalah daftar dari tuple yang berisi hasil scan ARP.
        ip = response.psrc  # Mendapatkan alamat IP sumber dari respons ARP.
        mac = response.hwsrc  # Mendapatkan alamat MAC sumber dari respons ARP.
        vendor = get_vendor(mac)  # Memanggil fungsi `get_vendor` untuk mendapatkan nama vendor berdasarkan alamat MAC.
        print(f"{ip:<20} {mac:<20} {vendor:<30}") # Menampilkan informasi IP, MAC, dan vendor
        
        # Tambahkan delay antar permintaan untuk mencegah tercapainya batas kecepatan API
        time.sleep(1)  
        # Menambahkan delay 1 detik antara permintaan untuk mencegah pembatasan rate API.

# Dapatkan range alamat ke ARP
while True:  # Memulai loop untuk mendapatkan input pengguna sampai rentang IP yang valid dimasukkan.
    ip_add_range_entered = input("Please enter an IP address range \n(e.g., 192.168.1.0/24): ")  
    # Meminta pengguna untuk memasukkan rentang alamat IP yang ingin dipindai.
    if ip_add_range_pattern.search(ip_add_range_entered):  
        # Memeriksa apakah input pengguna cocok dengan pola regex untuk rentang alamat IP.
        print(f"{ip_add_range_entered} is a valid IP address range")  
        # Jika valid, menampilkan pesan bahwa rentang alamat IP valid.
        break  # Keluar dari loop.
    else:
        print("Invalid IP address range. Please try again.")  
        # Jika input tidak valid, menampilkan pesan kesalahan dan meminta pengguna untuk mencoba lagi.

# Lakukan scan dan tampilkan hasilnya
arp_results = scan_network(ip_add_range_entered)  
# Memanggil fungsi `scan_network` dengan rentang alamat IP yang dimasukkan pengguna dan menyimpan hasilnya ke `arp_results`.
display_results(arp_results)  
# Memanggil fungsi `display_results` untuk menampilkan hasil scan ARP.

