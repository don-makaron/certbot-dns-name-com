import configparser
import json
import os
import sys

import requests


class NameComDNS:
    def __init__(self, username, token, domain_name):
        if not username or not token:
            raise ValueError('Please specify `username` or `token`')

        if not domain_name:
            raise ValueError('Please specify `domain_name`')

        self.domain_name = domain_name
        self.base_url = 'https://api.name.com/v4/domains/{0}/records'.format(self.domain_name)
		
		self.username = username
		self.token = token

    def list_records(self):
        r = requests.get(self.base_url, auth=(self.username, self.token))

        return r.json()

    def create_record(self, data):
        r = requests.post(self.base_url, data=json.dumps(data), auth=(self.username, self.token))

        if r.status_code in (requests.codes.ok, requests.codes.created):
            print(r.json())
        else:
            print('{0}: {1}'.format(r.status_code, r.content))

    def del_record(self, record_id):
        r = requests.delete('{0}/{1}'.format(self.base_url, record_id), auth=(self.username, self.token))

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
    if '*' in splitted_domain:
        splitted_domain.remove('*')

    top_level_domain = '.'.join(splitted_domain[-2:])  # 2nd level: domain.tld
    low_level_domain = '.'.join(splitted_domain[:-2])  # rest levels: subdomain2.subdomain

    host = '_acme-challenge'
    fqdn = '{0}.{1}'.format(host, top_level_domain)

    if low_level_domain:
        fqdn = '{0}.{1}.{2}'.format(host, low_level_domain, top_level_domain)
        host += '.{0}'.format(low_level_domain)

    # new record
    data = {
        'domainName': top_level_domain,
        'host': host,
        'fqdn': fqdn,
        'type': 'TXT',
        'answer': certbot_validation,
        'ttl': 300,
    }

    ncd = NameComDNS(config['auth']['username'], config['auth']['token'], top_level_domain)

    if cmd == 'add':
        ncd.create_record(data)
    elif cmd == 'clean':
        j = ncd.list_records()

        for record in j['records']:
            if record['fqdn'].startswith(fqdn):  # `startswith` because '.' at the end, but not in api docs
                ncd.del_record(record['id'])
