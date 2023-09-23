### IMPORTS ###
from flask import Flask, jsonify, request
from googlesearch import search
from urllib.parse import urlparse
from flask_cors import CORS
import requests

### SECRETS ###
# Use your own keys you peasant 
GOOGLE_API_KEY = "<YOUR GOOGLE CSE API HERE>"
SEARCH_ENGINE_ID = "<YOUR SEARCH ENGINE KEY>"
BLOWFISH_API_KEY = "<YOUR BLOWFISH KEY>"

### UTILITY FUNCTIONS ###
# Filters a specific domain name
def filter_domain(url):
    # Parse the URL
    parsed_url = urlparse(url)

    # Extract the domain name
    domain = parsed_url.netloc

    # Remove any "www." prefix from the domain name
    if domain.startswith("www."):
        domain = domain[4:]

    return domain


# Filters a bunch of urls together using lists as input and output
def filter_domain_list(url_list):
    # Initialise empty list to store parsed urls
    res = []

    # Parse all urls one-by-one
    for url in url_list: res.append(filter_domain(url))

    return res


# Runs Google Custom Search Engine Query and returns list of top 7 google results
def perform_google_search(query, num_results=7):
    # Calculate the start parameter based on the number of results per page
    start = 1
    urls = []

    while len(urls) < num_results:
        # Construct the API URL
        url = f"https://www.googleapis.com/customsearch/v1?key={GOOGLE_API_KEY}&cx={SEARCH_ENGINE_ID}&q={query}&start={start}"

        # Make the API request
        response = requests.get(url)
        data = response.json()

        # Extract the URLs from the search results
        search_items = data.get("items")
        for search_item in search_items:
            link = search_item.get("link")
            if link:
                urls.append(link)

        # Increment the start parameter for the next page of results
        start += 10

    # Return the top num_results URLs
    return urls[:num_results]


### FLASK APP API ###
app = Flask(__name__)
CORS(app)  # This allows cross origin resource sharing for all routes to the walletshield api

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/api/spooftest',methods=['POST'])
def spoof_test():

        try:
            if request.method=='POST':
                data = request.json
                url = data['url']
                context = data['context'].get("result")
                print("CONTEXT IS :",context)
                if filter_domain(url) in filter_domain_list(perform_google_search(context,num_results=7)):
                    response = {'message': 'SAFE'}
                    status_code = 200
                else:
                    response = {'message': 'UNSAFE'}
                    status_code = 200

        # Return back error statement if this thingy crashes
        except Exception as e:
            response = {'message': 'Error in Spooftest :'+str(e)}
            status_code = 500

        return jsonify(response), status_code

# TODO: Make API route for Blowfish api

if __name__ == '__main__':
    app.run(debug=True)
