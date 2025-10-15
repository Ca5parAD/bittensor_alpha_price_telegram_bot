import requests

from config import TAO_STATS_API_KEY


def valid_netuids_check(text: str) -> list[int]:
    """Validate each subnet is within range 0-128"""
    try:
        # Creates list of numbers if valid response format (numbers seperated by ',')
        netuids = [int(num.strip()) for num in text.split(',') if num.strip()]
    except Exception:
        return

    valid_netuids = []
    invalid_netuids = []
    for num in netuids: # Create lists of valid and invalid netuids
        if 0 <= num <= 128:
            valid_netuids.append(num)
        else:
            invalid_netuids.append(num)

    return valid_netuids, invalid_netuids


# TODO: Impliment caching and time logic to not go over api limit
def get_subnets_info(netuids: list[int]):
    '''Returns netuid and subnet info Dict from taostats'''
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

    ordered_subnets_info = dict(sorted(subnets_info.items()))
    return ordered_subnets_info

def get_total_subnets_value():
    '''Returns total subnet value rounded to 3 dp'''
    url = "https://api.taostats.io/api/dtao/pool/total_price/latest/v1"
    headers = {
        "accept": "application/json",
        "Authorization": TAO_STATS_API_KEY
    }

    response = requests.get(url, headers=headers)
    data = response.json()['data']
    return round(float(data[0]['price']), 3)

def get_subnets_info_text(netuids: list[int]):
    '''Format info into body of text'''
    subnets_info = get_subnets_info(netuids)

    info_text = f"Total subnet value: {get_total_subnets_value()}\n"

    for info in subnets_info.values():
        info_text += f"------------------------------\n"
        info_text += f"(<b>{info['netuid']}</b>) <b>{info['name']}</b>: <b>{round(float(info['price']), 6)}</b>\n"

        time_changes = dict()
        time_changes['1H'] = round(float(info['price_change_1_hour']), 2)
        time_changes['24H'] = round(float(info['price_change_1_day']), 2)
        time_changes['1W'] = round(float(info['price_change_1_week']), 2)
        time_changes['1M'] = round(float(info['price_change_1_month']), 2)

        for time, change in time_changes.items():
            if change > 0:
                info_text += f"🟢 <b>{time}</b>: +{change}%\n"
            elif change < 0:
                info_text += f"🔴 <b>{time}</b>: {change}%\n"
            else:
                info_text += f"⚪️ <b>{time}</b>: {change}%\n"

    return info_text
