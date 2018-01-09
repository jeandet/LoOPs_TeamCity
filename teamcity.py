import requests
import traceback
import configparser
from os.path import expanduser
home = expanduser("~")

class TeamCityJsonObject:

    def __init__(self, json):
        self.__dict__.update(json)

    def __repr__(self):
        return str(self.__dict__)


class TeamCityProject(TeamCityJsonObject):

    def __init__(self, json):
        super(TeamCityProject, self).__init__(json)


class TeamCityBuildType(TeamCityJsonObject):

    def __init__(self, json):
        super(TeamCityBuildType, self).__init__(json)
        
class TeamCityBuild(TeamCityJsonObject):

    def __init__(self, json):
        super(TeamCityBuild, self).__init__(json)


class TeamCityAPI:

    def __init__(self, server, user, password):
        self.server = server if '/app/rest' in server else server + '/app/rest'
        self.session = requests.Session()
        self.session.auth = (user, password)
        self.session.headers.update({
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        })

    def projects(self):
        projects = self.session.get(
            self.server + '/projects').json()
        return [TeamCityProject(project) for project in projects['project']]

    def build_types(self, project_id=None, project_name=None):
        if project_id is not None:
            url = self.server + '/projects/id:' + project_id + '/buildTypes'
        elif project_name is not None:
            url = self.server + '/projects/name:' + project_id + '/buildTypes'
        else:
            url = self.server + '/buildTypes'
        build_types = self.session.get(url).json()
        return [
            TeamCityBuildType(build_type)
            for build_type in build_types['buildType']
        ]

    def build_queue(self):
        build_queue = self.session.get(tc.server+'/buildQueue').json()
        return [
            TeamCityBuild(build)
            for build in build_queue['build']
        ]

config = configparser.ConfigParser()
config.read(home+"/.teamcity.conf")

    
tc = TeamCityAPI(config['DEFAULT']['server'], config['DEFAULT']['user'],config['DEFAULT']['password'])