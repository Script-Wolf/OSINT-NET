import requests
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import re

print("     ███████")
print("   ▄█▌ ▄ ▄ ▐█▄")
print("   ██▌▀▀▄▀▀▐██")
print("   ██▌ ▄▄▄ ▐██")
print("   ▀██▌▐█▌▐██▀")
print("▄██████ ▀ ██████▄")
print("Henrique S")


def fetch_subdomains(domain):
    """
    Fetch subdomains for a given domain using CRT.sh.
    
    :param domain: The domain to query
    :return: A list of discovered subdomains
    """
    url = f"https://crt.sh/?q=%.{domain}&output=json"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            subdomains = set()
            for entry in data:
                subdomain = entry['name_value']
                subdomains.update(subdomain.split("\n"))
            return sorted(subdomains)
        else:
            print(f"Error: Unable to fetch data from CRT.sh (Status code: {response.status_code})")
            return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

def main():
    # Ask the user for a domain
    domain = input("Enter the domain to scan for subdomains (e.g., example.com): ").strip()
    
    print(f"\nFetching subdomains for: {domain}")
    
    # Fetch subdomains
    subdomains = fetch_subdomains(domain)
    
    if subdomains:
        print("\n--- Discovered Subdomains ---")
        for subdomain in subdomains:
            print(subdomain)
    else:
        print("No subdomains found or an error occurred.")

if __name__ == "__main__":
    main()


def is_external_link(base_url, link):
    """
    Determines if a link is external to the base URL.
    
    :param base_url: The base URL of the site
    :param link: The URL to check
    :return: True if the link is external, False otherwise
    """
    base_netloc = urlparse(base_url).netloc
    link_netloc = urlparse(link).netloc
    return base_netloc != link_netloc and bool(link_netloc)

def find_links(url, visited=None):
    """
    Finds all external links and sublinks on a webpage.
    
    :param url: The URL of the page to analyze
    :param visited: A set to keep track of visited URLs
    :return: A dictionary with external links and sublinks
    """
    if visited is None:
        visited = set()

    links = {
        "external": set(),
        "sublinks": set()
    }

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        for a_tag in soup.find_all("a", href=True):
            link = urljoin(url, a_tag["href"])
            if link not in visited:
                visited.add(link)
                if is_external_link(url, link):
                    links["external"].add(link)
                else:
                    links["sublinks"].add(link)
    except Exception as e:
        print(f"Error fetching {url}: {e}")
    
    return links

def main():
    # Input the base URL
    base_url = input("Enter the URL to scan (e.g., https://example.com): ").strip()
    print(f"\nScanning {base_url}...")

    visited = set()
    results = find_links(base_url, visited)

    # Display results
    print("\n--- External Links ---")
    for link in sorted(results["external"]):
        print(link)

    print("\n--- Sublinks ---")
    for link in sorted(results["sublinks"]):
        print(link)

if __name__ == "__main__":
    main()

print("OSINT Complete ...")