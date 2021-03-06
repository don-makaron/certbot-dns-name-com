import configparser
import json
import os
import sys
from typing import Dict

import requests


class NameComDNS:
    def __init__(self, username: str, token: str, domain_name: str) -> None:
        if not username or not token:
            raise ValueError('Please specify `username` and `token`')

        if not domain_name:
            raise ValueError('Please specify `domain_name`')

        self.username: str = username
        self.token: str = token

        self.domain_name: str = domain_name

        self.base_url: str = f'https://api.name.com/v4/domains/{self.domain_name}/records'

    def list_records(self) -> Dict:
        r = requests.get(self.base_url, auth=(self.username, self.token))

        return r.json()

    def create_record(self, data: Dict) -> None:
        r = requests.post(self.base_url, data=json.dumps(data), auth=(self.username, self.token))

        if r.status_code in (requests.codes.ok, requests.codes.created):
            print(r.json())
        elif r.status_code == requests.codes.bad_request:
            r_json = r.json()

            if r_json['details'] == 'Parameter Value Error - Duplicate Record':
                # TODO: get record id to UpdateRecord
                print('Duplicated record: {r.content!r}')
            else:
                print(f'{r.status_code}: {r.content!r}')
        else:
            print(f'{r.status_code}: {r.content!r}')

    def delete_record(self, record_id: int) -> None:
        r = requests.delete(f'{self.base_url}/{record_id}', auth=(self.username, self.token))

        print(r.json())


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read(os.path.join(os.path.dirname(__file__), '.env'))

    if 'auth' not in config or 'username' not in config['auth'] or 'token' not in config['auth']:
        print('Create ".env" file and add "username", "token" to "auth" section')
        sys.exit()

    file_name, cmd, certbot_domain, certbot_validation = sys.argv

    splitted_domain = certbot_domain.split('.')

    # wildcard domains
    if splitted_domain[0] == '*':
        splitted_domain = splitted_domain[1:]

    top_level_domain = '.'.join(splitted_domain[-2:])  # 2nd level: domain.tld
    low_level_domain = '.'.join(splitted_domain[:-2])  # rest levels: subdomain2.subdomain

    host = '_acme-challenge'

    if low_level_domain:
        host = '.'.join((host, low_level_domain))

    # new record
    data = {
        'domainName': top_level_domain,
        'host': host,
        'type': 'TXT',
        'answer': certbot_validation,
        'ttl': 300,
    }

    ncd = NameComDNS(config['auth']['username'], config['auth']['token'], top_level_domain)

    if cmd == 'add':
        ncd.create_record(data)
    elif cmd == 'clean':
        fqdn = '.'.join((host, top_level_domain, ''))  # empty element for ending `.`
        j = ncd.list_records()

        for record in j['records']:
            if record['type'] == 'TXT' and record['fqdn'] == fqdn:
                ncd.delete_record(record['id'])
