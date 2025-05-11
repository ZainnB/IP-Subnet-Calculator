import ipaddress
import pandas as pd
from io import StringIO

def validate_ip(ip: str):
    try:
        ip_obj = ipaddress.ip_address(ip)
        return isinstance(ip_obj, (ipaddress.IPv4Address, ipaddress.IPv6Address))
    except ValueError:
        return False

def calculate_subnet_details(ip: str, mask: str):
    network = ipaddress.IPv4Network(f"{ip}/{mask}", strict=False)

    first_usable_ip = str(list(network.hosts())[0]) if network.num_addresses > 2 else str(network.network_address)
    last_usable_ip = str(list(network.hosts())[-1]) if network.num_addresses > 2 else str(network.broadcast_address)
    total_usable_hosts = network.num_addresses - 2 if network.num_addresses > 2 else network.num_addresses

    wildcard_mask = ".".join([str(255 - int(octet)) for octet in str(network.netmask).split(".")])
    
    ip_class = get_ip_class(ip)
    is_private = network.is_private

    return {
        "network_id": str(network.network_address),
        "broadcast_address": str(network.broadcast_address),
        "first_usable_ip": first_usable_ip,
        "last_usable_ip": last_usable_ip,
        "total_usable_hosts": total_usable_hosts,
        "wildcard_mask": wildcard_mask,
        "ip_class": ip_class,
        "is_private": is_private
    }

def get_ip_class(ip: str):
    first_octet = int(ip.split('.')[0])
    if first_octet < 128:
        return 'A'
    elif first_octet < 192:
        return 'B'
    elif first_octet < 224:
        return 'C'
    elif first_octet < 240:
        return 'D'
    else:
        return 'E'

def split_subnets(ip: str, mask: str, required_subnets: int):
    original_network = ipaddress.IPv4Network(f"{ip}/{mask}", strict=False)

    # Calculate how many subnets needed (round to next power of 2)
    needed_new_prefix = original_network.prefixlen
    max_prefix = 30  # Avoid /31 and /32
    while needed_new_prefix < max_prefix and (2 ** (needed_new_prefix - original_network.prefixlen)) < required_subnets:
        needed_new_prefix += 1
    if (2 ** (needed_new_prefix - original_network.prefixlen)) < required_subnets:
        raise ValueError("Cannot generate the required number of subnets.")


    subnets = list(original_network.subnets(new_prefix=needed_new_prefix))

    results = []
    for subnet in subnets[:required_subnets]:
        first_usable_ip = str(list(subnet.hosts())[0]) if subnet.num_addresses > 2 else str(subnet.network_address)
        last_usable_ip = str(list(subnet.hosts())[-1]) if subnet.num_addresses > 2 else str(subnet.broadcast_address)
        total_usable_hosts = subnet.num_addresses - 2 if subnet.num_addresses > 2 else subnet.num_addresses

        wildcard_mask = ".".join([str(255 - int(octet)) for octet in str(subnet.netmask).split(".")])

        results.append({
            "network_id": str(subnet.network_address),
            "broadcast_address": str(subnet.broadcast_address),
            "first_usable_ip": first_usable_ip,
            "last_usable_ip": last_usable_ip,
            "total_usable_hosts": total_usable_hosts,
            "wildcard_mask": wildcard_mask,
            "ip_class": get_ip_class(str(subnet.network_address)),
            "is_private": subnet.is_private
        })

    return results


def generate_csv(subnet_results: list):
    df = pd.DataFrame(subnet_results)
    csv_buffer = StringIO()
    df.to_csv(csv_buffer, index=False)
    return csv_buffer.getvalue()



def calculate_ipv6_subnet_details(ip: str, cidr: int):
    network = ipaddress.IPv6Network(f"{ip}/{cidr}", strict=False)
    ip_obj = ipaddress.IPv6Address(ip)

    # Avoid listing all hosts. Calculate mathematically.
    total_ips = 2 ** (128 - cidr)
    first_ip = network.network_address + 1
    last_ip = network.network_address + total_ips - 2

    return {
        "ip_address": str(ip_obj.compressed),
        "full_ip_address": str(ip_obj.exploded),
        "total_addresses": f"2^{128 - cidr}",
        "network_id": str(network.network_address),
        "ip_range": f"{first_ip} - {last_ip}",
        "first_usable_ip": str(first_ip),
        "last_usable_ip": str(last_ip),
        "is_private": network.is_private
    }


def split_ipv6_subnet(ip: str, prefix: int, required_subnets: int):
    original_network = ipaddress.IPv6Network(f"{ip}/{prefix}", strict=False)

    new_prefix = prefix
    while (2 ** (new_prefix - prefix)) < required_subnets:
        new_prefix += 1
        if new_prefix > 128:
            raise ValueError("Cannot generate that many subnets with IPv6")

    subnets = list(original_network.subnets(new_prefix=new_prefix))
    results = []

    for subnet in subnets[:required_subnets]:
        total_ips = 2 ** (128 - subnet.prefixlen)
        first_ip = subnet.network_address + 1
        last_ip = subnet.network_address + total_ips - 2

        results.append({
            "network_id": str(subnet.network_address),
            "prefix_length": subnet.prefixlen,
            "ip_range": f"{first_ip} - {last_ip}",
            "first_usable_ip": str(first_ip),
            "last_usable_ip": str(last_ip),
            "total_addresses": f"2^{128 - subnet.prefixlen}",
            "is_private": subnet.is_private
        })

    return results


def suggest_subnet_mask(host_count: int):
    if host_count <= 0 or host_count > (2**32 - 2):
        raise ValueError("Host count must be between 1 and 2^32 - 2.")

    for cidr in range(32, 0, -1):
        usable = 2 ** (32 - cidr) - 2
        if usable >= host_count:
            subnet = ipaddress.IPv4Network(f"0.0.0.0/{cidr}")
            netmask = str(subnet.netmask)
            wildcard = ".".join([str(255 - int(octet)) for octet in netmask.split(".")])
            return {
                "suggested_cidr": f"/{cidr}",
                "subnet_mask": netmask,
                "usable_hosts": usable,
                "wildcard_mask": wildcard
            }

    raise ValueError("Could not calculate subnet mask.")
