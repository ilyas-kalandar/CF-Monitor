from requests import get
from datetime import datetime
from utils import date_to_str, is_between
from submission import Submission


class Parser:
    def __init__(self):
        self.handle = None
        self.handle_is_valid = True
        self.userinfo = {
            'handle': None,
            'rating': None,
            'last_online': None
        }

    def set_handle(self, new_handle):
        """ Changes handle"""
        self.handle = new_handle

    def check_handle(self):
        """ Check for valid handle """

        data = get("http://codeforces.com/api/user.info?handles=" + self.handle)

        data = data.json()
        data['result'] = data['result'][0]
        self.handle_is_valid = data['status'] == 'OK'

        if not self.handle_is_valid:
            return False

        self.userinfo['handle'] = data['result']['handle']
        
        try:
            self.userinfo['rating'] = data['result']['rating']
        except KeyError:
            self.userinfo['rating'] = "None"
        self.userinfo['last_online'] = datetime.fromtimestamp(
            data['result']['lastOnlineTimeSeconds'])

        return True
    
    def clear(self):
        self.submissions = {
            'submissions': {
                'accepted_submissions': [],
                'rejected_submissions': [],
            }
        }

    def parse(self):
        """ Parse all submissions """
        if not self.handle or not self.handle_is_valid:
            raise ValueError(
                "Invalid handle, please set handle with set_handle method.")

        r = get(f"http://codeforces.com/api/user.status?handle={self.handle}")

        for s in r.json()['result']:
            date = date_to_str(datetime.fromtimestamp(
                s['creationTimeSeconds']))
            try:
                s['problem']['rating']
            except KeyError:
                s['problem']['rating'] = "Unknown"

            submission = Submission(
                s['problem']['name'],
                s['problem']['rating'],
                s['programmingLanguage'],
                s['verdict'],
                s['creationTimeSeconds'],
            )

            # let's create list if not exist!
            try:
                self.submissions[date]
            except KeyError:
                self.submissions[date] = {
                    'accepted_submissions': [],
                    'rejected_submissions': [],
                }

            try:
                self.submissions[s['problem']['name']]
            except KeyError:
                self.submissions[s['problem']['name']] = {
                    'accepted_submissions': [],
                    'rejected_submissions': [],
                }

            verdict = 'accepted_submissions' if s['verdict'] == 'OK' else 'rejected_submissions'

            self.submissions[s['problem']['name']][verdict].append(
                submission
            )

            self.submissions['submissions'][verdict].append(
                submission
            )

            self.submissions[date][verdict].append(
                submission
            )

    def __get(self, key, verdict=None):
        try:
            if not verdict:
                return self.__get(key, verdict="OK") + self.__get(key, verdict="not_ok")
            return self.submissions[key][
                'accepted_submissions' if verdict == "OK" else 'rejected_submissions'
            ]
        except KeyError:
            return []

    def get_submissions(self, **kwargs):
        result = {}
        try:
            kwargs['problem_name']
        except KeyError:
            kwargs['problem_name'] = None

        try:
            kwargs['_from']
        except KeyError:
            kwargs['_from'] = None

        try:
            kwargs['to']
        except KeyError:
            kwargs['to'] = None

        try:
            kwargs['verdict']
        except:
            kwargs['verdict'] = None

        try:
            if kwargs['date']:
                kwargs['date'] = date_to_str(kwargs['date'])
        except KeyError:
            kwargs['date'] = None

        try:
            kwargs['check']
        except KeyError:
            kwargs['check'] = False

        if kwargs['problem_name'] and kwargs['date']:
            raise ValueError("Only problem_name or only date may store value.")

        if kwargs['date'] and (kwargs['_from'] or kwargs['to']):
            raise ValueError(
                "If filtering by date enable, _from and to not cant be used.")

        if kwargs['problem_name']:
            key = kwargs['problem_name']
        elif kwargs['date']:
            key = kwargs['date']
        else:
            key = 'submissions'

        for s in self.__get(key, kwargs['verdict']):
            if (kwargs['_from'] or kwargs['to']) and not is_between(
                    datetime.fromtimestamp(s.creation_time), _from=kwargs['_from'], to=kwargs['to']):
                continue

            if kwargs['check'] and not self.is_good_submission(s):
                continue

            try:
                result[s.problem_name].append(s)
            except KeyError:
                result[s.problem_name] = [s]

        return result

    def is_good_submission(self, s):
        """ Check submission, if problem not solved previously, return True"""

        submissions = self.__get(s.problem_name, "OK")
        sent_time = datetime.fromtimestamp(s.creation_time)
        for s in submissions:
            time = datetime.fromtimestamp(s.creation_time)
            if sent_time.year != time.year or sent_time.month != time.month or sent_time.day != time.day:
                return False

        return True
