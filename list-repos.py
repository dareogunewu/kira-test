import json
from urllib import request
import argparse


DEFAULT_GITHUB_USERNAME = 'github'


def get_args ():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', help = 'username')
    parser.add_argument('--token', help = 'access token')
    return parser.parse_args()


def get_username ():
    args = get_args()

    if args.u:
        return args.u
    else:
        return DEFAULT_GITHUB_USERNAME


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

    access_token = args.token

    if access_token:

        get_all_repos(access_token, username, page)

    else:

        print ('no access token found ... showing public repos only:')


if __name__ == '__main__':
    begin(get_username(), 1)
