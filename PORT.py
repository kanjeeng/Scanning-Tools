import socket # Modul ini digunakan untuk membuat dan mengelola koneksi jaringan.
from concurrent.futures import ThreadPoolExecutor 
# Menjalankan scanning port secara paralel menggunakan beberapa thread, meningkatkan kecepatan scanning.

def scan_port(host, port):
    try: # Memulai blok try untuk menangani potensi kesalahan selama melakukan scan.
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        # Membuat soket TCP(SOCK_STREAM) dengan alamat IPv4(AF_INET)
            sock.settimeout(1)
            # Mengatur waktu tunggu(timeout) untuk koneksi 1 detik, jika tidak berhasil maka dianggap gagal.
            result = sock.connect_ex((host, port))
            # Mencoba menghubungi port pada host yang ditentukan. connect_ex mengembalikan 0 jika koneksi berhasil namun jika koneksi gagal maka akan mengenbalikan kode kesalahan.
            if result == 0:
                try: # Memulai blok try kedua untuk menangani potensi kesalahan saat mengirim permintaan dan menerima banner.  
                    sock.send(b'HEAD / HTTP/1.0\r\n\r\n')
                    # Mengirimkan permintaan HTTP sederhana untuk mendapatkan banner dari layanan yang berjalan di port.
                    response = sock.recv(1024).decode() 
                    # Menerima hingga 1024 byte dari respons layanan dan mendekodekannya ke dalam string.
                    if response:
                    	service = response.split('\n')[0]
                    	# Memisahkan respons berdasarkan baris baru (\n) dan Mengambil baris pertama sebagai informasi layanan dari banner (jika ada)
                    else:
                    	service = "Unknown"
                    	# Mengatur variabel service ke "Unknown" jika ada kesalahan saat menerima banner dari respons.
                except: # Menangani kesalahan jika ada saat mengirim permintaan atau menerima respons.
                    service = "Unknown" 
                    # Mengatur variabel service ke "Unknown" jika ada kesalahan saat menerima banner.
                return (port, "open", service) 
                # Mengembalikan tuple(tipe data Python menyimpan sekumpulan item) yang menunjukkan port terbuka bersama dengan nama layanan (jika ada).
            else:
                return (port, "closed", "") 
                # Mengembalikan tuple yang menunjukkan bahwa port tertutup.
    except: # Menangani kesalahan jika ada selama proses scan.
        return (port, "closed", "") 
        # Mengembalikan tuple yang menunjukkan bahwa port tertutup jika terjadi kesalahan.

def scan_ports(host, ports):
    print(f"\nScanning {host}...\n")
    print("PORT\t\tSTATE\tSERVICE")
    # Menampilkan tulisan Scanning dengan nama host
    with ThreadPoolExecutor(max_workers=100) as executor:
    # Membuat objek ThreadPoolExecutor dengan maksimal 100 thread. Ini memungkinkan scan dilakukan secara paralel untuk mempercepat proses.
        futures = [executor.submit(scan_port, host, port) for port in ports]
	# Membuat daftar objek Future dgn mengirimkan tugas 'scan_port' utk setiap port yang diberikan. 'executor.submit' mengirimkan tugas untuk dieksekusi secara paralel.
        for future in futures: # Iterasi melalui setiap objek Future dalam daftar futures.
            port, state, service = future.result()
            # Memperoleh hasil dari setiap scanning port setelah selesai. future.result() mengembalikan tuple yang dikembalikan oleh fungsi scan_port.
            if state == "open":
            	port = f"{port}/tcp"
            	print(f"{port:<8}\t{state:<6}\t{service}")
            	# Mencetak informasi tentang port yang terbuka, termasuk nomor port, protokol, keadaan, dan layanan yang terdeteksi.
            	

target_ip = input("Enter the target IP address/Hostname: ")
# Meminta pengguna memasukkan alamat IP atau nama host target yang ingin dipindai.
r = int(input("Enter range port scanning: "))
# Rentang port yang ingin dipindai
ports = range(1, r)
# Membuat rentang objek range yang mencakup semua port dari 1 hingga r untuk dipindai.
scan_ports(target_ip, ports)
# Memanggil fungsi scan_ports dengan target IP dan rentang port yang diberikan untuk memulai scanning.
