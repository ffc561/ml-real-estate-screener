#zillow-api data extraction script
import requests

class ZillowAPI():
    def __init__(self, zillow_api_key, zillow_api_host, max_retries, retry_delay):
        self.api_key = zillow_api_key
        self.api_host = zillow_api_host
        self.root_url = 'https://' + zillow_api_host
        self.max_retries = max_retries
        self.retry_delay = retry_delay

    def call_zillow_api(self, request_url, request_params):
    
        request_headers = {
            "x-rapidapi-key" : self.api_key,
            "x-rapidapi-host" : self.api_host
        }

        resp = requests.get(url = request_url, headers = request_headers, params = request_params)

        # Expand this to handle different error codes in different ways (i.e. retry after delay on 429)
        if resp.status_code != 200:
            print("Error in API Extraction: " + str(resp.status_code))
            print(resp.reason)
            return None
        else:
            print("API call successful!")
            return resp.json()

    def get_property_extended_search(self, query_location, status_type, home_type):
        """
        Calls the zillow property extended search API
        """
        url = self.root_url + "/propertyExtendedSearch"

        params = {"location" : query_location}
        
        if status_type is not None:
            params["status_type"] = status_type
        if home_type is not None:
            params["home_type"] = home_type

        all_data = []
        i = 1
        max_pages = 20

        while i <= max_pages:
            params["page"] = i
            data = self.call_zillow_api(url, params)
            all_data.append(data)
            if data["totalPages"] != 20:
                max_pages = data["totalPages"]
            i += 1
        
        return all_data

    def get_property_details_by_zpid(self, property_zpid):
        url = self.root_url + "/property"
        params = {"zpid" : property_zpid}
        return self.call_zillow_api(url, params)