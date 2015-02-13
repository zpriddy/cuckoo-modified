# Copyright (C) 2015 Jeremy Hedges (KillerInstinct)
# This file is part of Cuckoo Sandbox - http://www.cuckoosandbox.org
# See the file 'docs/LICENSE' for copying permission.

from lib.cuckoo.common.abstracts import Signature
import re

class DecryptsConfig(Signature):
    name = "decrypts_config"
    description = "An IP address was found in a decryption routine"
    severity = 3
    categories = ["crypto"]
    authors = ["KillerInstinct"]
    minimum = "1.2"
    evented = True

    def __init__(self, *args, **kwargs):
        Signature.__init__(self, *args, **kwargs)
        self.decrypted = []

    filter_apinames = set(["CryptHashData"])

    def on_call(self, call, process):
        if call["api"] == "CryptHashData":
            self.decrypted.append(self.get_raw_argument(call, "Buffer"))
        return None

    def on_complete(self):
        matches = [
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{2,5}',
        ]
        extracted_config = False
        for potential_config in self.decrypted:
            for entry in matches:
                if re.match(entry, potential_config):
                    extracted_config = True
                    self.data.append({"config": potential_config})

        return extracted_config       
