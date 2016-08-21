import json
import os

from tldextract import tldextract


class Resolve(object):
    def __init__(self, domain, type):
        self.inputDomain = domain.lower()
        extracted = tldextract.extract(self.inputDomain)
        self.subDomain = extracted.subdomain
        self.suffix = extracted.suffix
        self.domain = extracted.domain
        self.type = type.lower()
        self.response = []

    def lookup(self):
        self.parse_records()
        return self

    def get_standard_domain(self):
        return self.domain + "." + self.suffix

    def get_config_file_address(self):
        return 'zones/' + self.get_standard_domain() + ".json"

    def get_config_file_content(self):
        with open(self.get_config_file_address()) as data_file:
            return json.load(data_file)

    def parse_records(self):
        type = self.get_standard_type()

        if type == "SOA":
            data = self.get_config_file_content()[type]

            self.response.append({
                "qtype": type,
                "qname": self.get_standard_domain(),
                "content": data['content'],
                "ttl": data['ttl']
            })

        else:
            for value in self.get_config_file_content()[type]:
                if type == "A" and self.subDomain != value['address'] and self.inputDomain + '.' != value['address']:
                    continue

                self.response.append({
                    "qtype": type,
                    "qname": value['address'],
                    "content": value['content'],
                    "ttl": value['ttl']
                })

    def get_standard_type(self):
        if self.type == "a" or self.type == 'any':
            return "A"
        elif self.type == "ns":
            return "NS"
        elif self.type == "mx":
            return "MX"
        elif self.type == "soa":
            return "SOA"
        elif self.type == "cname":
            return "CNAME"
        elif self.type == "srv":
            return "SRV"
        elif self.type == "txt":
            return "TXT"
        else:
            return None


class Monitor(object):

    def __init__(self):
        pass