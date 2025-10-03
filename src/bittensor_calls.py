import requests

from config import TAO_STATS_API_KEY


# Validate each subnet is within range 0-128
def valid_netuids_check(text: str) -> list[int]:
    try:
        # Creates list of numbers if valid response format (numbers seperated by ',')
        subnets = [int(num.strip()) for num in text.split(',') if num.strip()]
    except Exception:
        return

    valid_subnets = []
    invalid_subnets = []
    for num in subnets: # Create lists of valid and invalid netuids
        if 0 <= num <= 128:
            valid_subnets.append(num)
        else:
            invalid_subnets.append(num)

    return valid_subnets, invalid_subnets


class GetNetuidInfoObj:
    def __init__(self):
        # Create bittensor connection
        url = "https://api.taostats.io/api/dtao/pool/latest/v1?page=1"
        headers = {
            "accept": "application/json",
            "Authorization": TAO_STATS_API_KEY
        }

        response = requests.get(url, headers=headers)
        self.info = response.json()['data']

    def get_netuid_info(self, netuid: int):
        # Fetches subnet object containing subnet info
        for info in self.info:
            if info['netuid'] == netuid:
                return info['name'], info['price']
    
    def close(self):
        pass