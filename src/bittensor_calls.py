import logging

import bittensor


logger = logging.getLogger(__name__)  # Access logger dynamically

subtensor = bittensor.subtensor(network='finney') # Setup bittensor network

def get_netuid_info(netuid: int):
    info = subtensor.subnet(netuid)
    logger.debug((f"{info.subnet_name} -> {info.price}"))
    return info.subnet_name, info.price