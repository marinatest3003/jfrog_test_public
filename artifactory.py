import requests
import configparser

config = configparser.ConfigParser()
# config["DEFAULT"] = {"ping_url": "/api/system/ping", "version_url": "/api/system/version",
#                      "storage_url": "/api/storageinfo", "users_url": "/api/security/users",
#                      "repositories_url": "/api/repositories"}
# with open("config.ini", 'w') as configfile:
#     config.write(configfile)
config.read("config.ini")

ping_url = config["DEFAULT"]["ping_url"]
version_url = config["DEFAULT"]["version_url"]
storage_url = config["DEFAULT"]["storage_url"]
users_url = config["DEFAULT"]["users_url"]
repositories_url = config["DEFAULT"]["repositories_url"]

class Artifactory:

    def __init__(self, url=None, username=None, password=None):
        """
        :param url: URL of artifactory
        :param username: username of user
        :param password: pass of user

        creates an instance of the Artifactory class
        """
        self.url = url
        self.auth = (username, password)

    def ping(self):
        """
        :return: True if pinged successfully, False otherwise
        """
        response = requests.get(self.url + ping_url)
        return response.status_code

    def system_version(self):
        response = requests.get(self.url + version_url, auth=self.auth)
        return response.json()

    def create_user(self, user):
        """
        :param user: new user to add. type(user) = User
        :return:
        """
        response = requests.put(self.url + users_url + '/' + user.name, auth=self.auth, **{"json": {"name": user.name, "password": user.password, "email": user.email}})
        return response.status_code

    def delete_user(self, user_name):
        """
        :param user_name: name of user to delete
        :return: True if deleted user successfully
        """
        response = requests.delete(self.url + users_url + '/' + user_name, auth=self.auth)
        return response.status_code

    def storage_info(self):
        response = requests.get(self.url + storage_url, auth=self.auth)
        return response.json()

    def create_repository(self, repository):
        """
        :param repository: new repository to add. type(user) = User
        :return:
        """
        response = requests.put(self.url + repositories_url + '/' + repository.key, auth=self.auth, **{'headers': {'Content-Type': 'application/json'}, 'data': f'{{"key": "{repository.key}", "description": "{repository.description}", "url" : "{self.url + repositories_url + "/" + repository.key}", "packageType" : "{repository.packageType}", "rclass": "{repository.rclass}"}}'})
        return response.status_code

    def update_repository(self, repository_key, new_repo_description):
        # Once a repository is created, we cannot change its key, type or rclass
        repository = requests.get(self.url + repositories_url + '/' + repository_key, auth=self.auth)
        response = requests.post(self.url + repositories_url + '/' + repository_key, auth=self.auth, **{'headers': {'Content-Type': 'application/json'}, 'data': f'{{"key": "{repository_key}", "description": "{new_repo_description}", "url" : "{self.url + repositories_url + "/" + repository_key}", "packageType" : "{repository.json()["packageType"]}", "rclass": "{repository.json()["rclass"]}"}}'})
        return response.status_code

    def list_repositories(self):
        """
        :return: list of all active repositories
        """
        response = requests.get(self.url + repositories_url, auth=self.auth)
        return response.json()