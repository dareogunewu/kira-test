from os import path
import json
from urllib import request, parse
import argparse
import getpass
from base64 import b64encode

DEFAULT_GITHUB_USERNAME = 'github'
DEFAULT_NOTE = 'public & private repos'


def get_auth_file_path (username):
    return './authorization-' + username + '.json'


def get_args ():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', help = 'username')
    parser.add_argument('--note', help = 'unique authorization note')
    parser.add_argument('--public', help = 'showing only public repos', default=False, action='store_true')
    return parser.parse_args()


def get_username ():
    args = get_args()

    if args.u:
        return args.u
    else:
        return DEFAULT_GITHUB_USERNAME


def get_access_token (username):
    args = get_args()

    auth_file_path = get_auth_file_path(username)

    auth_note = args.note if args.note else DEFAULT_NOTE

    if (path.exists(auth_file_path)):
        with open(auth_file_path) as auth_file:
            auth_json = json.loads(auth_file.read())
            return auth_json['token']
    else:
        password = getpass.getpass('Enter GitHub Password for ' + username + ': ')
        username_password = bytearray(username + ':' + password, 'utf8')
        basic_auth_64 = b64encode(username_password).decode("ascii")
        req = request.Request('https://api.github.com/authorizations')
        req.add_header('Content-Type', 'application/json')
        req.add_header('Authorization', 'Basic ' + basic_auth_64)
        try:
            req_content = json.dumps({
                'scopes': [
                    'repo'
                ],
                'note': auth_note
            }).encode("utf8")
            with request.urlopen(req, data=req_content) as res:
                res_content = res.read().decode('utf8')
                create_access_token_file(auth_file_path, res_content)
                res_data = json.loads(res_content)
                return res_data['token']
        except Exception as ex :
            print('')

            if (ex.code == 422):
                print ('an authorization already exists with note "' + auth_note + '"\n')
                print ('- consider specifying a value for the --note argument. see help info.')
            else:
                print ('an error occurred when creating access token:')
                print (ex)

            print('')


def create_access_token_file (file_path, contents):
    with open(file_path, 'w') as auth_file:
        auth_file.write(contents)


def get_public_repos (username, page):
    url = 'https://api.github.com/users/' + username + '/repos?page=' + str(page)

    repo_list = json.load(request.urlopen(url))

    for i in range(len(repo_list)):
        repo = repo_list[i]
        print(repo['name'])

    if len(repo_list) > 0:
        return get_public_repos(username, page + 1)


def get_all_repos (access_token, username, page):
    url = 'https://api.github.com/user/repos?access_token=' + access_token + '&token_type=bearer&page=' + str(page)

    repo_list = json.load(request.urlopen(url))

    for i in range(len(repo_list)):
        repo = repo_list[i]
        print(repo['name'])

    if len(repo_list) > 0:
        return get_all_repos(access_token, username, page + 1)


def begin (username, page):
    args = get_args()

    if (args.public):
        return get_public_repos(username, page)

    else:
        access_token = get_access_token(username)

        if access_token:

            get_all_repos(access_token, username, page)
        
        else:

            print ('no access token found ... showing public repos only:')

            get_public_repos(username, page)


if __name__ == '__main__':
    begin(get_username(), 1)