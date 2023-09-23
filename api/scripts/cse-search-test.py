import requests

# Replace with your API Key and Search Engine ID
API_KEY = "<insert key here>"
SEARCH_ENGINE_ID = "<insert whatever you want dude>"

def perform_google_search(query, num_results=7):
    # Calculate the start parameter based on the number of results per page
    start = 1
    urls = []

    while len(urls) < num_results:
        # Construct the API URL
        url = f"https://www.googleapis.com/customsearch/v1?key={API_KEY}&cx={SEARCH_ENGINE_ID}&q={query}&start={start}"

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

# Example usage:
query = "google"
top_7_urls = perform_google_search(query, num_results=7)
print(top_7_urls)
for i, url in enumerate(top_7_urls, start=1):
    print(f"Result #{i}: {url}")
