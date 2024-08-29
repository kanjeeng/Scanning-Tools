import subprocess

def run_wpscan(url, user_file=None, password_file=None):
    # Menyiapkan perintah WPScan
    command = ['wpscan', '--url', url, '-U', user_file, '-P', password_file, '--no-banner']

    if not user_file or not password_file:
        raise ValueError("Both user_file and password_file are required for brute-force.")

    try:
        # Menjalankan perintah WPScan
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")
        print(e.stderr)
        return None

target_url = input("Enter the URL to scan (e.g., http://example.com): ").strip()
user_file = input("Enter the path to the file with usernames: ").strip()
password_file = input("Enter the path to the file with passwords: ").strip()
print("")
    
output = run_wpscan(target_url, user_file, password_file)
print(output)

