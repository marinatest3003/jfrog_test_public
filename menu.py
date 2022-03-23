from artifactory import Artifactory
from user import User
from repository import Repository
from hashlib import sha256

def authenticate(username, password):
    user_digest = sha256(username.encode()).hexdigest()
    password_digest = sha256(password.encode()).hexdigest()
    users_passwords = [line.rstrip() for line in open('administrators.txt', 'r')]
    if user_digest + ' ' + password_digest in users_passwords:
        return True
    else:
        return False

#tell them we cant use typer command in while loop. it creates
#a problem because we need to enter password after every function call


if __name__ == "__main__":
    username = input("enter username: ")
    password = input("enter password: ")
    if authenticate(username, password):
        artifactory = Artifactory("https://marinatest3003.jfrog.io/artifactory", "marinatest3003@gmail.com", "AKCp8krAhgWSHGbTQQTQeXwougdJEgkfTVy8f783Zb3L1gMTQ3sTRohL4SSqQnuiYmynDEUun")

        while True:
            print("\nChoose what to do!")
            print("1 - ping")
            print("2 - system version")
            print("3 - create user")
            print("4 - delete user")
            print("5 - storage info")
            print("6 - create repository")
            print("7 - update repository")
            print("8 - list repositories")
            print("Hit any other key to exit\n")
            choice = int(input())

            if choice > 8 or choice < 1:
                break
            else:
                if choice == 1:
                    print(artifactory.ping())

                if choice == 2:
                    print(artifactory.system_version())

                if choice == 3:
                    name = input("enter name: ")
                    password = input("enter password: ")
                    email = input("enter email: ")
                    print(artifactory.create_user(User(name, password, email)))

                if choice == 4:
                    name = input("enter name: ")
                    print(artifactory.delete_user(name))

                if choice == 5:
                    print(artifactory.storage_info())

                if choice == 6:
                    key = input("enter key: ")
                    description = input("enter description (optional): ")
                    package_type = input("enter package type (Maven, Docker, etc): ")
                    rclass = input("enter rclass (local, remote, virtual): ")
                    print(artifactory.create_repository(Repository(key, description, package_type, rclass)))

                if choice == 7:
                    key = input("enter key of desired repository: ")
                    new_repo_description = input("enter new repository description: ")
                    print(artifactory.update_repository(key, new_repo_description))

                if choice == 8:
                    print(artifactory.list_repositories())
    else:
        input("Wrong credentials! Hit any key to exit...")