import configparser
import json
import os
import sys

import requests


class NameComDNS:
    def __init__(self, username, token, domain_name):
        self.username = username
        self.token = token

        self.domain_name = domain_name

        self.base_url = 'https://api.name.com/v4/domains/{0}/records'.format(self.domain_name)

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
        r = requests.delete('{0}/{1}'.format(self.base_url, record_id), data=data, auth=(self.username, self.token))

        print(r.json())


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read(os.path.join(os.path.dirname(__file__), '.env'))

    if 'auth' not in config or 'username' not in config['auth'] or 'token' not in config['auth']:
        print('Create ".env" file and add "username", "token" to "auth" section')
        sys.exit()

    file_name, cmd, certbot_domain, certbot_validation = sys.argv

    data = {
        'domainName': 'lonelyassistant.net',
        'host': '_acme-challenge',
        'fqdn': '_acme-challenge.lonelyassistant.net',
        'type': 'TXT',
        'answer': certbot_validation,
        'ttl': 300,
    }

    ncd = NameComDNS(config['auth']['username'], config['auth']['token'], certbot_domain)

    if cmd == 'add':
        ncd.create_record(data)

    elif cmd == 'clean':
        j = ncd.list_records()

        for record in j['records']:
            if record['host'] == '_acme-challenge':
                ncd.del_record(record['id'])



