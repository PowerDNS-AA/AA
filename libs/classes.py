import json
import os

from tldextract import tldextract


class Resolve(object):
    def __init__(self, domain, type):
        self.inputDomain = domain.lower()
        type = type.lower()
        extracted = tldextract.extract(self.inputDomain)
        self.subDomain = extracted.subdomain
        self.suffix = extracted.suffix
        self.domain = extracted.domain
        self.type = type
        self.response = []

    def lookup(self):
        if self.type == "a" or self.type == "any":
            self.parse_a_records()
        elif self.type == "ns":
            self.parse_ns_records()

        return self

    def get_standard_domain(self):
        return self.domain + "." + self.suffix

    def get_config_file_address(self):
        return 'zones/' + self.get_standard_domain() + ".json"

    def get_config_file_content(self):
        with open(self.get_config_file_address()) as data_file:
            return json.load(data_file)

    def parse_a_records(self):
        for value in self.get_config_file_content()['A']:
            if self.subDomain == value['address'] or self.inputDomain + '.' == value['address']:
                self.response.append({
                    "qtype": "A",
                    "qname": value['address'],
                    "content": value['content'],
                    "ttl": value['ttl']
                })

    def parse_ns_records(self):
        for value in self.get_config_file_content()['NS']:
            self.response.append({
                "qtype": "NS",
                "qname": value['address'],
                "content": value['content'],
                "ttl": value['ttl']
            })