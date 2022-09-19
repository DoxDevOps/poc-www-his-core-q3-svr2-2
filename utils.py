import urllib.request
import json
import platform
import subprocess
import sys
from fabric import Connection

""" 
Implements data collection commands
"""
class api:

    def get_sites_from_cluster(cluster_endpoint, site_endpoint):

        for cluster in json.loads(urllib.request.urlopen(urllib.request.Request(cluster_endpoint)).read().decode('utf-8')):

            return cluster['fields']['site']

    def get_site(site_id, site_endpoint):
        return json.loads(urllib.request.urlopen(urllib.request.Request(site_endpoint + str(site_id))).read().decode('utf-8'))

"""
Implements network commands 
"""
class net:

    def ping(ip_address):
        
        param = '-n' if platform.system().lower()=='windows' else '-c'

        if subprocess.call(['ping', param, '1', ip_address]) == 0:

            return True

        else:

            return False

""" 
Implements file related commands
"""         
class files:

    def push(app, username, ip):
        
        """ 
        default value for result 
        """
        result = False

        """ 
        default value for exit_code 
        """
        exit_code = 1

        """ 
        ship to various destination depending on the app, of course, the source is different too
        currently we are only dealing with 3 apps - api, core, and art
        add a if block for new app 
        """
        if app == 'api':  

            source_dir = "BHT-EMR-API/"

            destination_dir = username + "@" + ip + ":/var/www/BHT-EMR-API"

            exit_code = subprocess.call(['rsync', '--exclude=config', '-avzhe',  'ssh', source_dir, destination_dir])

            if exit_code == 0:

                result = True

        if app == 'core':

            source_dir = "BHT-Core/"

            destination_dir = username + "@" + ip + ":/var/www/BHT-Core"

            exit_code = subprocess.call(['rsync', '-avzhe',  'ssh', source_dir, destination_dir])

            if exit_code == 0:

                result = True

        if app == 'art':

            source_dir = 'ART/'

            destination_dir = username + "@" + ip + ":/var/www/BHT-Core/apps/ART"

            exit_code = subprocess.call(['rsync', '--exclude=config', '-avzhe',  'ssh', source_dir, destination_dir])

            if exit_code == 0:

                result = True

        return result

""" 
Implements git commands
"""
class git:
    
    def checkout(host, directory, tag):

        result = Connection(host).run('cd ' + directory + ' && git checkout -f ' + tag + ' && git describe > HEAD', hide=True)

        if result:  

            return True

        else:

            return False


    
