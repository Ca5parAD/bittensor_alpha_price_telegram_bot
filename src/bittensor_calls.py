import logging

import bittensor


logger = logging.getLogger(__name__)  # Access logger dynamically

subtensor = bittensor.subtensor(network='finney') # Setup bittensor network

# Validate each subnet is within range 0-128
def valid_subnets_check(text: str) -> list[int]:
    subnets = [int(num.strip()) for num in text.split(',') if num.strip()]
    logger.debug(f"subnets: {subnets}")

    valid_subnets = []
    invalid_subnets = []
    for num in subnets:
        if 0 <= num <= 128:
            valid_subnets.append(num)
        else:
            invalid_subnets.append(num)

    logger.debug(f"valid subnets: {valid_subnets}, invalid subnets: {invalid_subnets}")
    return valid_subnets, invalid_subnets


def get_netuid_info(netuid: int):
    subtensor = bittensor.subtensor(network='finney') # Setup bittensor network
    info = subtensor.subnet(netuid)
    logger.debug((f"{info.subnet_name} -> {info.price}"))
    subtensor.close()
    return info.subnet_name, info.price