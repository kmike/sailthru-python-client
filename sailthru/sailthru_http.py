# -*- coding: utf-8 -*-
import sys
import requests
from sailthru.sailthru_error import SailthruClientError
from sailthru.sailthru_response import SailthruResponse

def flatten_nested_hash(hash_table):
    """
    Flatten nested dictionary for GET / POST / DELETE API request
    """
    def flatten(hash_table, brackets=True):
        f = {}
        for key,value in hash_table.items():
            _key = '[' + str(key) + ']' if (brackets == True) else str(key)
            if type(value) is dict:
                for k,v in flatten(value).items():
                    f[_key + k] = v
            elif type(value) is list:
                temp_hash = {}
                for i,v in enumerate(value):
                    temp_hash[str(i)] = v
                for k,v in flatten(temp_hash).items():
                    f[ _key + k] = v
            else:
                f[_key] = value
        return f
    return flatten(hash_table, False)

def sailthru_http_request(url, data, method, file_data = None):
    """
    Perform an HTTP GET / POST / DELETE request
    """
    data = flatten_nested_hash(data)

    params = data if method.lower() != 'post' else None
    body = data if method.lower() == 'post' else None
    headers = { 'User-Agent': 'Sailthru API Python Client' }

    try:
        response = requests.request(method, url,
            params=params,
            data=body,
            headers=headers,
            files = file_data
        )
        response.raise_for_status()
        return SailthruResponse(response)
    except requests.RequestException, e:
        trace = sys.exc_info()[2]
        raise SailthruClientError(str(e)), None, trace
