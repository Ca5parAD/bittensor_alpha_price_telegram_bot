import logging

import bittensor


logger = logging.getLogger(__name__)  # Access logger dynamically

# Validate each subnet is within range 0-128
def valid_netuids_check(text: str) -> list[int]:
    try:
        subnets = [int(num.strip()) for num in text.split(',') if num.strip()]
    except Exception:
        return

    valid_subnets = []
    invalid_subnets = []
    for num in subnets:
        if 0 <= num <= 128:
            valid_subnets.append(num)
        else:
            invalid_subnets.append(num)

    return valid_subnets, invalid_subnets


def get_netuid_info(netuid: int):
    with bittensor.subtensor(network='finney') as subtensor:
        info = subtensor.subnet(netuid)
    return info.subnet_name, info.price


""" Options for more efficient info:
    establish subtensor instance at start of loop, pass as arg to get_netuid function
    use class, init at start of loop, use self.subtensor to pass through - just need to figure how to close and clean up after loop

    implimenting this could also use async to send out all requests concurrently

    unsure if the method approuch could be effectively closed like the with approuch

    """