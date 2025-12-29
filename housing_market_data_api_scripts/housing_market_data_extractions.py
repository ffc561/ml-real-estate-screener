#US housing market api data extraction
import requests
import time

class UhmdApi():
    def __init__(self, api_key, api_host, max_retries, retry_delay):
        self.api_key = api_key
        self.api_host = api_host
        self.root_url = 'https://' + api_host
        self.max_retries = max_retries
        self.retry_delay = retry_delay

    def call_api(self, request_url, request_params):
    
        request_headers = {
            "x-rapidapi-key" : self.api_key,
            "x-rapidapi-host" : self.api_host
        }

        resp = requests.get(url = request_url, headers = request_headers, params = request_params)

        if resp.status_code != 200:
        
            print("Error in API Extraction: " + str(resp.status_code))
            print(resp.reason)
            print("Retrying API call...")

            time.sleep(self.retry_delay)
            
            retries = 0
            
            while retries <= self.max_retries:
                retry_resp = requests.get(url = request_url, headers = request_headers, params = request_params)
                if retry_resp.status_code == 200:
                    break
                else:
                    retries += 1
            
            if retry_resp == 200:
                return retry_resp.json()
            else:
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
            data = self.call_api(url, params)
            all_data.append(data)
            if data["totalPages"] != 20:
                max_pages = data["totalPages"]
            i += 1
        
        return all_data

    def get_property_details_by_zpid(self, property_zpid):
        url = self.root_url + "/property"
        params = {"zpid" : property_zpid}
        return self.call_api(url, params)