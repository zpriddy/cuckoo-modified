# Copyright (C) 2015 KillerInstinct
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from lib.cuckoo.common.abstracts import Signature

class Multiple_UA(Signature):
    name = "multiple_useragents"
    description = "Network activity contains more than one unique useragent."
    severity = 3
    categories = ["network"]
    authors = ["KillerInstinct"]
    minimum = "1.2"
    evented = True

    def __init__(self, *args, **kwargs):
        Signature.__init__(self, *args, **kwargs)
        self.useragents = list()
        self.procs = list()

    filter_apinames = set(["InternetOpenA", "InternetOpenW"])

    def on_call(self, call, process):
        # Dict whitelist with process name as key, and useragent as value
        whitelist = {
            "AcroRd32.exe": "Mozilla/3.0 (compatible; Acrobat 5.0; Windows)",
            "iexplore.exe": "VCSoapClient",
            "iexplore.exe": "Shockwave Flash",
        }
        ua = self.get_argument(call, "Agent")
        proc = process["process_name"]
        if proc in whitelist.keys() and ua == whitelist[proc]:
            pass
        else:
            if ua not in self.useragents:
                self.useragents.append(ua)
                self.procs.append((process["process_name"], ua))

    def on_complete(self):
        ret = False
        if len(self.useragents) > 1:
            ret = True
            for item in self.procs:
                self.data.append({"Process" : item[0]})
                self.data.append({"User-Agent" : item[1]})

        return ret
