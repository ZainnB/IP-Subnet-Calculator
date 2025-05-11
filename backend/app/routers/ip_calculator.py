from fastapi import APIRouter, HTTPException
from typing import List, Literal, Union
from fastapi.responses import StreamingResponse
from app.models import IPInput, SubnetResult, IPInputV6, SubnetResultV6, IPv6SplitInput, IPv6SubnetResult,  MaskSuggestionInput, MaskSuggestionResult
from app.services import split_ipv6_subnet, split_subnets, generate_csv, calculate_subnet_details, validate_ip, calculate_ipv6_subnet_details, suggest_subnet_mask

router = APIRouter()

@router.post("/calculate", response_model=SubnetResult)
def calculate_ip_subnet(input_data: IPInput):
    ip = str(input_data.ip_address)
    mask = input_data.subnet_mask

    if not validate_ip(ip):
        raise HTTPException(status_code=400, detail="Invalid IP address.")

    if mask is None:
        mask = "24"  # default to /24 if not provided

    result = calculate_subnet_details(ip, mask)
    return SubnetResult(**result)

from app.models import SubnetSplitInput

@router.post("/split", response_model=List[SubnetResult])
def split_ip_subnet(input_data: SubnetSplitInput):
    ip = str(input_data.ip_address)
    mask = input_data.subnet_mask
    required_subnets = input_data.required_subnets

    if not validate_ip(ip):
        raise HTTPException(status_code=400, detail="Invalid IP address.")

    if required_subnets <= 0:
        raise HTTPException(status_code=400, detail="Number of subnets must be positive.")

    results = split_subnets(ip, mask, required_subnets)
    return [SubnetResult(**res) for res in results]


@router.post("/export")
def export_subnet_data(
    input_data: Union[SubnetSplitInput, IPv6SplitInput],
    export_format: Literal["csv", "json"] = "csv"
):
    ip = str(input_data.ip_address)

    # Detect IPv6 or IPv4
    is_ipv6 = ":" in ip

    if not validate_ip(ip):
        raise HTTPException(status_code=400, detail="Invalid IP address.")

    if input_data.required_subnets <= 0:
        raise HTTPException(status_code=400, detail="Number of subnets must be positive.")

    try:
        if is_ipv6:
            results = split_ipv6_subnet(ip, input_data.cidr, input_data.required_subnets)
        else:
            results = split_subnets(ip, input_data.subnet_mask, input_data.required_subnets)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    if export_format == "csv":
        csv_data = generate_csv(results)
        response = StreamingResponse(
            iter([csv_data]),
            media_type="text/csv"
        )
        response.headers["Content-Disposition"] = "attachment; filename=subnet_data.csv"
        return response
    else:
        return results



@router.post("/calculate-v6", response_model=SubnetResultV6)
def calculate_ipv6(input_data: IPInputV6):
    ip = str(input_data.ip_address)
    cidr = input_data.cidr

    if not validate_ip(ip):
        raise HTTPException(status_code=400, detail="Invalid IPv6 address.")

    if not (1 <= cidr <= 128):
        raise HTTPException(status_code=400, detail="CIDR must be between 1 and 128.")

    result = calculate_ipv6_subnet_details(ip, cidr)
    return SubnetResultV6(**result)


@router.post("/split-v6", response_model=List[IPv6SubnetResult])
def split_ipv6(input_data: IPv6SplitInput):
    ip = str(input_data.ip_address)
    prefix = input_data.cidr
    count = input_data.required_subnets

    if not (1 <= prefix <= 128):
        raise HTTPException(status_code=400, detail="CIDR must be between 1 and 128.")

    try:
        result = split_ipv6_subnet(ip, prefix, count)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return result



@router.post("/suggest-mask", response_model=MaskSuggestionResult)
def suggest_mask(input_data: MaskSuggestionInput):
    try:
        result = suggest_subnet_mask(input_data.host_count)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
