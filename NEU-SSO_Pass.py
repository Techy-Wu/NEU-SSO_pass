import requests
from bs4 import BeautifulSoup 
import re
import json
import argparse

def request_jsessionid(user_name, password, inquery_url, plain_headers):
    def get_value(data, name):
        soup = BeautifulSoup(data, 'html.parser')
        input = soup.find('input', {'name': name})
        if input and 'value' in input.attrs:
            value = input['value']
            return value
        else:
            return "Input element not found or doesn't have a value attribute."

    # Get universal login pass

    url = 'https://pass.neu.edu.cn/tpass/login'
    headers = {
        **plain_headers
    }
    params = {
        'service': inquery_url
    }

    response = requests.get(url, params = params)
    headers = response.headers

    lt = get_value(response.text, 'lt')
    execution = get_value(response.text, 'execution')
    _eventId = get_value(response.text, '_eventId')

    coockie = headers.get('Set-Cookie')
    match = re.search(r"JSESSIONID=([^;]+)", coockie)
    if match:
        jsessionid_pass = match.group(1)
    else:
        raise Exception("Error - Unexpected Response")

    # Submit form
    
    url = 'https://pass.neu.edu.cn/tpass/login'

    form_data = {
        'rsa': user_name + password + lt,
        'ul': str(len(user_name)),
        'pl': str(len(password)),
        'lt': lt,
        'execution': execution,
        '_eventId': _eventId
    }
    form_data_length = len(str(json.dumps(form_data)))
    headers = {
        **plain_headers,
        'Cookie': 'JSESSIONID=' + jsessionid_pass + '; Language=zh_CN',
        'Host': 'pass.neu.edu.cn',
        'Referer': url,
        'Origin': 'https://pass.neu.edu.cn/',
        'Content-Length': str(form_data_length),
        'Content-Type': 'application/x-www-form-urlencoded',
        'Pragma': 'no-cache',
    }
    params = {
        'service': inquery_url
    }
    response = requests.post(url, data = form_data, params = params, headers = headers, allow_redirects = False)
    if str(response.status_code)[0] != "3":
        raise Exception("Error - Unexpected Response")
    headers = response.headers
    location = headers.get('Location')

    # Redirect to inquery app

    url = location
    return url

if __name__ == '__main__':

    parse = argparse.ArgumentParser()
    parse.add_argument('-n', '--name', help = 'Username')
    parse.add_argument('-p', '--pwd', help = 'Account password')
    parse.add_argument('-u', '--url', help = 'URL of inquiry application')
    parse.add_argument('-j', '--json', help = 'Path of json file indicating headers')
    parse.add_argument('-w', '--warn', help = 'Raise warning switch', default = 0)
    args = parse.parse_args()
    
    if args.name:
        name = str(args.name)
    else:
        raise SyntaxError('Username not specified')
    if args.pwd:
        password = str(args.pwd)
    else:
        raise SyntaxError('Account password not specified')
    if args.url:
        url = str(args.url)
    else:
        raise SyntaxError('URL not specified')
    if args.json:
        with open(str(args.json), 'r') as json_file:
            headers = json.load(json_file)
    else:
        headers = {}
        if args.warn != 0:
            raise SyntaxWarning('Headers not specified')
    
    print(request_jsessionid(name, password, url, headers))