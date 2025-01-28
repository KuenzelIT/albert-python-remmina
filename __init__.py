# -*- coding: utf-8 -*-

"""

"""

import configparser
import os
from albert import *
from pathlib import Path
from string import hexdigits
from urllib.parse import quote_plus

md_iid = '2.0'
md_version = '1.2'
md_name = 'Remmina'
md_description = 'Open rdp connections with remmina'
md_license = 'MIT'
md_url = 'https://github.com/KuenzelIT/albert-python-remmina'
md_authors = "@kuenzelit"

HOME_DIR = os.environ["HOME"]
REMMINA_DIR = HOME_DIR + "/.remmina"


class Plugin(PluginInstance, GlobalQueryHandler):

    def __init__(self):
        GlobalQueryHandler.__init__(self,
                                    id=md_id,
                                    name=md_name,
                                    description=md_description,
                                    defaultTrigger='#')
        PluginInstance.__init__(self, extensions=[self])
        self.icon_url = f"file:{Path(__file__).parent}/icon.png"

    def handleGlobalQuery(self, query):
        if not query.string.strip():
            return

        if not os.path.isdir(REMMINA_DIR):
            return

        results = []

        search = query.string.lower()

        parser = configparser.RawConfigParser()
        files = os.listdir(REMMINA_DIR)

        for fileName in files:
            fullPath = REMMINA_DIR + '/' + fileName
            parser.read(fullPath)

            name = parser.get('remmina', 'name').lower()

            if search not in name:
                continue

            results.append(
                RankItem(
                    StandardItem(
                        id=md_id,
                        text=name,
                        subtext="Open rdp connection to %s" % search,
                        iconUrls=[self.icon_url],
                        actions=[
                            Action(
                                search,
                                "Open rdp connection to %s" % search,
                                lambda file=fullPath: runDetachedProcess(
                                    ['remmina', file]
                                ),
                            )
                        ]
                    ),
                    1
                )
            )

        return results