import sys
sys.path.append('insana/')
import constants
import requests
import simplejson
from urllib import urlencode

BASE_URL = "https://app.asana.com/api/1.0"

class AsanaClient():
    def __init__(self, profile):
        self.access_token = profile.access_token
        self.asana_id = profile.asana_id
        self.profile = profile
        self.refresh_token = profile.refresh_token

    def get(self, endpoint, with_access_token=True, **kwargs):
        url = BASE_URL + endpoint + "?" + urlencode(kwargs)
        headers = {"Authorization":"Bearer %s" % (self.access_token) }
        response = requests.get(url, headers=headers)
        if response.status_code == 401:
            #refresh token
            self.get_refresh_token()
            response = requests.get(url, headers=headers)
        return response
    
    def post(self, endpoint, with_access_token=True, **kwargs):
        url = BASE_URL + endpoint
        data = kwargs
        response = requests.post(url, data=data)
        if response.status_code == 401:
            self.get_refresh_token()
            response = requests.post(url, data=data)
        return response

    def get_user_info(self):
        info = simplejson.loads(self.get('/users/me').text)
        if info is not None:
            return info.get('data')
        return None

    def get_projects_for_user(self, workspace):
        """doing this really inefficiently. looks like you can't get the project names along with the ids"""
        
#        tasks = self.get('/tasks', assignee=self.asana_id, workspace=workspace, opt_fields='projects', opt_expand=['projects'])
        tasks = self.get('/tasks', assignee=self.asana_id, workspace=workspace, opt_fields='projects')
        tasks = simplejson.loads(tasks.text).get('data')
        projects_list = []
        unique_project_ids = []

        for task in tasks:
            projects = task.get('projects')
            p = None
            project_id = None
            if projects:
                for p in projects:
                    project_id = p.get('id')
                    if project_id not in unique_project_ids:
                        count = len(unique_project_ids) % 4
                        projects_list.append(self.get_project_info(project_id, count=count))
                        unique_project_ids.append(project_id)
        # task is { 'id':'', 'name':''}                        
        return projects_list

    def get_project_info(self, project_id, count=0):
        project = {}
        response = self.get("/projects/%s" % (project_id))
        data = simplejson.loads(response.text).get('data')
        project['id'] = project_id
        project['name'] = data.get('name')
        project['followers'] = data.get('followers')
        project['color'] = constants.PROJECT_COLORS[count]
        return project

    def get_tasks_for_project(self, project_id):
        response = self.get('/projects/%s/tasks' % (project_id))
        tasks = simplejson.loads(response.text).get('data')
        return tasks
    
    def get_users_on_project(self):
        pass

    def get_workspaces(self):
        user_info = self.get_user_info()
        workspaces = []
        if user_info is not None:
            workspaces = user_info.get('workspaces')
        return workspaces

    def get_refresh_token(self):
        url = "https://app.asana.com/-/oauth_token"
        data = {
            'grant_type':'refresh_token',
            'client_id':constants.ASANA_CLIENT_ID,
            'client_secret':constants.ASANA_CLIENT_SECRET,
            'redirect_uri':constants.redirect_uri,
            'refresh_token':self.refresh_token,
            }
        response = requests.post(url, data=data)
        info = simplejson.loads(response.text)
        access_token = info.get('access_token')
        self.profile.access_token = access_token
        self.profile.save()
        return access_token 
