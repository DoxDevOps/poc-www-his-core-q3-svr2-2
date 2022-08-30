import os
import utils
from invoke import Responder
from fabric import Connection

cluster_endpoint = 'http://10.44.0.52:8000/sites/api/v1/get_single_cluster/1'
site_endpoint = 'http://10.44.0.52:8000/sites/api/v1/get_single_site/'



for site in utils.api.get_sites_from_cluster(cluster_endpoint, site_endpoint):    
    
    for fetched_site in utils.api.get_site(site, site_endpoint):

        if utils.net.ping(fetched_site['fields']['ip_address']):

            apps = ['api', 'core', 'art']   

            dir_name = {
                'api'   :   'BHT-EMR-API',
                'core'  :   'BHT-Core',
                'art'   :   'BHT-Core/apps/ART'
            }    

            app_tag = {
                'api'   :   'v4.10.29',
                'core'  :   'v4.7.11',
                'art'   :   'v4.11.5'
            }        

            for app in apps:

                if utils.files.push(app, fetched_site['fields']['username'], fetched_site['fields']['ip_address']):

                    print("Files pushed successfully.")
                    
                    # change app version/tag
                    host = fetched_site['fields']['username'] + "@" + fetched_site['fields']['ip_address']

                    directory = "/var/www/" + dir_name[app]

                    if utils.git.checkout(host, directory, app_tag[app]):

                        if app == 'api':

                            #os.system("ssh " + host + " bash --login -c 'cd /var/www/BHT-EMR-API && bundle install --local && mysql -uroot -proot openmrs < db/sql/openmrs_metadata_1_7.sql -v -f && mysql -uroot -proot openmrs < db/sql/alternative_drug_names.sql -v -f && mysql -uroot -proot openmrs < db/sql/moh_regimens_v2020.sql -v -f && mysql -uroot -proot openmrs < db/sql/bart2_views_schema_additions.sql -v -f && rake db:migrate'")
                            #check = os.system("ssh " + host + " ' . ~/.profile; exec cd /var/www/BHT-EMR-API && bundle install --local && mysql -uroot -proot openmrs < db/sql/openmrs_metadata_1_7.sql -v -f && mysql -uroot -proot openmrs < db/sql/alternative_drug_names.sql -v -f && mysql -uroot -proot openmrs < db/sql/moh_regimens_v2020.sql -v -f && mysql -uroot -proot openmrs < db/sql/bart2_views_schema_additions.sql -v -f && rake db:migrate'")
                            #check = os.system("ssh " + host + " -t ' bash -l -c cd /var/www/BHT-EMR-API && bundle install --local && mysql -uroot -proot openmrs < db/sql/openmrs_metadata_1_7.sql -v -f && mysql -uroot -proot openmrs < db/sql/alternative_drug_names.sql -v -f && mysql -uroot -proot openmrs < db/sql/moh_regimens_v2020.sql -v -f && mysql -uroot -proot openmrs < db/sql/bart2_views_schema_additions.sql -v -f && rake db:migrate'")
                            #ssh user@host -t 'ls; exec $SHELL -l'
                            #ssh user@host  -t 'bash -l -c "ls"'

                            check = os.system("ssh " + host + " -t 'cd /var/www/BHT-EMR-API; bundle install --local; mysql -uroot -proot openmrs < db/sql/openmrs_metadata_1_7.sql -v -f; mysql -uroot -proot openmrs < db/sql/alternative_drug_names.sql -v -f; mysql -uroot -proot openmrs < db/sql/moh_regimens_v2020.sql -v -f; mysql -uroot -proot openmrs < db/sql/bart2_views_schema_additions.sql -v -f; rvm use 2.5.3; rake db:migrate; bash --login'")
                            #ssh server -t "do.sh; bash --login"
                            print("checking bundle and rake: " + str(check))

                        elif app == 'core':

                            Connection(host).run("mv /var/www/BHT-Core/config/config.json.example /var/www/BHT-Core/config/config.json")

                        elif app == 'art':

                            Connection(host).run("mv /var/www/BHT-Core/apps/ART/application.json.example /var/www/BHT-Core/apps/ART/application.json")

                        print("Successfully checked out " + app + " to " + app_tag[app])

                        c = Connection(host)

                        sudopass = Responder(
                            pattern=r'\[sudo\] password:',
                            response='123456\n',
                        )

                        c.run('sudo /opt/nginx/sbin/nginx -s reload', pty=True, watchers=[sudopass])

                    else:

                        print("Failed to check out " + app)
                    

                    # load meta data
                    # change status on Xi to depict successful transfer of files to site
                    # send email alert to followers or maybe generate report

                else:

                    print("Failed to transfer.")
                    # change status on Xi to depict failed transfer of files
                    # send email alert to followers or maybe generate report
