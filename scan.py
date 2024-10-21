import socket
import whois
from colorama import Fore, Style
import signal
import concurrent.futures

gr = Fore.GREEN
rd = Fore.RED
rst = Style.RESET_ALL

def is_nxdomain(domain):
    try:
        socket.gethostbyname(domain)
        return False
    except socket.gaierror as e:
        if e.errno == socket.EAI_NONAME:
            return True
        else:
            return None

def get_domain_info(domain_name):
    try:
        # Mendapatkan informasi whois domain
        domain_info = whois.whois(domain_name)
        
        return domain_info
    except Exception as e:
        return None

def handle_sigint(signum, frame):
    print("\nReceived SIGINT. Exiting...")
    exit(0)

def process_domain(url):
    result = is_nxdomain(url)
    if result is True:
        print(f"{gr}Domain {url} is NXDOMAIN.{rst}")
    elif result is False:
        print(f"{gr}Domain {url} valid.{rst}")
    elif result is None:
        print(f"{rd}Possible TakeOver: {url}{rst}")
        domain_info = get_domain_info(url)
        if domain_info:
            print(f"{gr}DNS for {url}:{rst}")
            for i, dns in enumerate(domain_info.name_servers, start=1):
                print(f"{i}. {dns}")
        with open("postakeover.txt", "a") as f:
            f.write(f"{url}\n")
            f.write("DNS:\n")
            for i, dns in enumerate(domain_info.name_servers, start=1):
                f.write(f"{i}. {dns}\n")
                f.write("\n")

def main():
    # Menangani sinyal SIGINT
    signal.signal(signal.SIGINT, handle_sigint)

    urls = []
    aalistaa = input("Give Me Domain List: ")
    with open(aalistaa, "r") as file:
        for line in file:
            urls.append(line.strip())

    # Menggunakan ThreadPoolExecutor
    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        # Menjalankan proses domain untuk setiap URL
        executor.map(process_domain, urls)

if __name__ == "__main__":
    main()
