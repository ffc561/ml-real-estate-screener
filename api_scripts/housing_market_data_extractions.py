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
        
            print(f"Error in API Extraction: {resp.status_code}")
            print(resp.reason)
            print("Retrying API call...")

            time.sleep(self.retry_delay)
            
            retries = 1
            
            while retries <= self.max_retries:
                retry_resp = requests.get(url = request_url, headers = request_headers, params = request_params)
                if retry_resp.status_code == 200:
                    print("Retry successful.")
                    return retry_resp.json()
                else:
                    print(f"Error in API Extraction: {resp.status_code}")
                    print(resp.reason)
                    print("Retrying API call...")
                    print(f"Retry count: {retries}")
                    time.sleep(self.retry_delay)
                    retries += 1
            

            print("Retries unsuccessful.")
            return None
        
        else:
            print("API call successful!")
            return resp.json()

    def get_property_extended_search(self, query_location, status_type, home_type, page_call_delay=5):
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
            print(i)
            print(data)
            all_data.append(data)
            if data == []:
                max_pages = 1
            elif data["totalPages"] != 20:
                max_pages = data["totalPages"]
            i += 1
        
        return all_data

    def get_property_details_by_zpid(self, property_zpid):
        url = self.root_url + "/property"
        params = {"zpid" : property_zpid}
        return self.call_api(url, params)

    def get_transit_scores_by_zpid(self, property_zpid):
        url = self.root_url + "/walkAndTransitScore"
        params = {"zpid" : property_zpid}
        return self.call_api(url, params)
    
    def get_building_details(self, building_id):
        url = self.root_url + "/building"
        params = {"buildingId" : building_id}
        return self.call_api(url, params)

    def get_property_comps(self, zpid):
        url = self.root_url + "/propertyComps"
        params = {"zpid" : zpid}
        return self.call_api(url, params)
    
    def get_property_similar_sales(self, zpid):
        url = self.root_url + "/similarSales"
        params = {"zpid" : zpid}
        return self.call_api(url, params)

    def get_monthly_inventory(self, zipcode):
        url = self.root_url + "/residentialData/monthlyInventory"
        params = {"zip" : zipcode}

        data = self.call_api(url, params)
        
        results_list = []

        if data is not None:
            if data["totalCount"] != 0:
                total_pages = int(data["totalCount"] / 100) + 1
                if total_pages > 1:
                    results_list.extend(data["records"])
                    page_num = 2
                    while page_num <= total_pages:
                        params["page"] = page_num
                        data=self.call_api(url, params)
                        results_list.extend(data["records"])
                        page_num += 1
                else:
                    results_list = data["records"]
                    
        return results_list
    
    def get_off_market_listings(self, zipcode):
        url = self.root_url + "/offMarket"
        params = {"zip" : zipcode}
        return self.call_api(url, params)