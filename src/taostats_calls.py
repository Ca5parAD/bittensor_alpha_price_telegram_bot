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

def get_subnets_info(netuids: list[int]):
    '''Returns dict of netuid key and subnet info value from taostats'''

    # Impliment caching and time logic to not go over api limit

    url = "https://api.taostats.io/api/dtao/pool/latest/v1?page=1"
    headers = {
        "accept": "application/json",
        "Authorization": TAO_STATS_API_KEY
    }

    response = requests.get(url, headers=headers)
    data = response.json()['data']

    netuids_set = set(netuids)
    subnets_info = dict()
    for subnet in data:
        if subnet['netuid'] in netuids_set:
            subnets_info[int(subnet['netuid'])] = subnet

    return subnets_info


def get_subnets_info_text(netuids: list[int]):
    subnets_info = get_subnets_info(netuids)
    ordered_subnets_info = dict(sorted(subnets_info.items()))

    # Format info into body of text
    info_text = str()
    for info in ordered_subnets_info.values():
        info_text += f"({info['netuid']}) {info['name']}: {round(float(info['price']), 6)}\n"

    return info_text
