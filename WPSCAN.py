import subprocess

def run_wpscan(url, api_token=None, enumerate_users=False):
    # Menyiapkan perintah WPScan dengan opsi --no-banner untuk menghilangkan header
    command = ['wpscan', '--url', url, '--no-banner']

    if api_token:
        command.extend(['--api-token', api_token])
    
    if enumerate_users:
        command.extend(['--enumerate', 'u'])

    try:
        # Menjalankan perintah WPScan
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")
        print(e.stderr)
        return None

target_url = input("Enter the URL to scan (e.g., http://example.com): ").strip()
api_token = input("Enter API Token (leave empty if not needed): ").strip() or None
enumerate_users = input("Do you want to enumerate users? (yes/no): ").strip().lower() == 'yes'
print("")

output = run_wpscan(target_url, api_token, enumerate_users)
print(output)

