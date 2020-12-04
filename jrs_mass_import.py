import sys
import os
import datetime
import zipfile
import shutil

class Zip:
    def __init__(self, filename):
        self.zipf = zipfile.ZipFile(filename, 'w', zipfile.ZIP_DEFLATED)

    def __del__(self): 
        self.zipf.close()

    def add_file(self, filepath):
        self.zipf.write(filepath)

    def add_dir(self, path):
        for root, dirs, files in os.walk(path):
            for file in files:
                self.add_file(os.path.join(root, file))


class User:
    def __init__(self, s):
        if '@' in s:
            self.username = s[:s.find('@')]
            self.email = s
        else:
            self.username = s
            self.email = ''
        self.password = ''
        self.externallyDefined = True
        self.enabled = True
        self.role = 'ROLE_USER'
        self.previousPasswordChangeTime = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.000+03:00")

    def __repr__(self):
        return f"User(Username:'{self.username}', Email:'{self.email}')"
    
    def to_XML(self):
        return f"""{self.username}, {self.role}"""


def clear_working_dir():
    try:
        shutil.rmtree("users", ignore_errors=True)
    except:
        pass
    try:
        os.remove("index.xml")
    except:
        pass


def write_index_file(users, filename):
    with open(filename, 'w', encoding="utf-8") as file:
        file.write("""<?xml version="1.0" encoding="UTF-8"?><export><property name="pathProcessorId" value="zip"/><property name="rootTenantId" value="organizations"/><property name="jsVersion" value="7.2.0 CE"/><module id="authority">""")
        for u in users:
            file.write(f"""<user>{u.username}</user>""")
        file.write("""</module></export>""")


def write_users_files(users, parent_folder):
    for u in users:
        with open(f"{parent_folder}/{u.username}.xml", 'w', encoding="utf-8") as file:
            file.write(f"""<?xml version="1.0" encoding="UTF-8"?><user><username>{u.username}</username><fullName>{u.username}</fullName><password>{u.password}</password><email>{u.email}</email><externallyDefined>{str(u.externallyDefined).lower()}</externallyDefined><enabled>{str(u.enabled).lower()}</enabled><role>{u.role}</role><previousPasswordChangeTime>{u.previousPasswordChangeTime}</previousPasswordChangeTime></user>""")


def main(filename, role):
    with open(filename, 'r', encoding="utf-8") as file:
        lines = file.read().splitlines()

    basename = os.path.splitext(os.path.basename(filename))[0]
         
    users = []
    for line in lines:
        u = User(line)
        u.role = role
        users.append(u)

    clear_working_dir()
    os.mkdir("users")
    write_index_file(users, "index.xml")
    write_users_files(users, "users")
    archive = Zip(f"{basename}.zip")
    archive.add_dir("users")
    archive.add_file("index.xml")
    clear_working_dir()


if __name__== "__main__":
    if len(sys.argv) < 2:
        print("Укажите файл с пользователями и, опционально, роль для новых пользователей")
        exit()

    INPUT_FILENAME = sys.argv[1]

    if len(sys.argv) < 3:
        INPUT_ROLE = "ROLE_USER"
    else:
        INPUT_ROLE = sys.argv[2]

    main(INPUT_FILENAME, INPUT_ROLE)