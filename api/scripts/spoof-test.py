# A Deprecated method of testing for spoof websites
# Still works, but is rate-limited to 100 tests a day
# Doesn't need an api key so this code is a peasant-friendly approach (all puns intended, please take all jokes with a light heart xD)
# Enjoy

from googlesearch import search
from urllib.parse import urlparse

def filter_domain(url):
    # Parse the URL
    parsed_url = urlparse(url)

    # Extract the domain name
    domain = parsed_url.netloc

    # Remove any "www." prefix from the domain name
    if domain.startswith("www."):
        domain = domain[4:]

    return domain


def filter_domain_list(url_list):
    # Initialise empty list to store parsed urls
    res = []

    # Parse all urls one-by-one
    for url in url_list: res.append(filter_domain(url))

    return res

# DRIVER CODE
test_url = "https://upon-12.web.app/"
context = "HONEY is the cryptocurrency of the Hivemapper Netw"

if filter_domain(test_url) in filter_domain_list(list(search(context,num_results=7))): print("Safe")
else: print("Unsafe")
