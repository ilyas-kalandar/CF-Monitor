from requests import get
from colorama import Fore, init
from datetime import datetime
from tabulate import tabulate
from sys import platform
from os import system
from collections import Counter

URL = "http://codeforces.com/api/user.status?handle="

def get_submissions(username):
	""" Returns all submissions of user"""
	try:
		data = {
			'lang': 'ru',
		}

		r = get(URL + username, params=data)
	except ConnectionError:
		return

	assert r.json()['status'] != 'FAILED'

	result = {
		'submissions': [],
		'good_submissions': [],
		'bad_submissions': [],
	}

	for subm in r.json()['result']:
		time = datetime.fromtimestamp(subm['creationTimeSeconds'])
		time = f"{time.year}:{time.month}:{time.day}"
		
		try:
			result[subm['problem']['name']]
		except KeyError:
			result[subm['problem']['name']] = {
				'good_submissions': [],
				'bad_submissions': [],
			}

		try:
			result[time]
		except KeyError:
			result[time] = {
				'good_submissions': [],
				'bad_submissions': [],
				'submissions': [],
			}

		result[time]['submissions'].append(subm)
		result['submissions'].append(subm)

		if subm['verdict'] == 'OK':
			result[time]['good_submissions'].append(subm)
			result['good_submissions'].append(subm)
			result[subm['problem']['name']]['good_submissions'].append(subm)
		else:
			result[time]['bad_submissions'].append(subm)
			result['bad_submissions'].append(subm)
			result[subm['problem']['name']]['bad_submissions'].append(subm)


	return result

def clear():
	""" Cross-platform clearing function."""

	if 'win' in platform:
		system("cls")
	else:
		system("clear")

def set_color(color):
	print(color, end='')

def add_zero(num):
	return ('0' if num < 10 else '') + str(num)

def is_solved_today(data, task_subm, date):
	for i in data[task_subm['problem']['name']]['good_submissions']:
		creation_time = datetime.fromtimestamp(i['creationTimeSeconds'])

		if creation_time.year != date.year or (
			creation_time.month != date.month or creation_time.day != date.day):
			return False

	return True

def str_date(date):
	return f"{date.year}:{date.month}:{date.day}"

def get_solved_tasks(data, date):
	result = {}
	if date:
		submissions = data[str_date(date)]['good_submissions']
	else:
		submissions = data['submissions']

	for subm in submissions:
		if date and not is_solved_today(data, subm, date):
			continue

		result[subm['problem']['name']] = subm

	return result

if __name__ == '__main__':
	init()
	set_color(Fore.LIGHTCYAN_EX)
	bar = r"""
  ____ _____   __  __             _ _
 / ___|  ___| |  \/  | ___  _ __ (_) |_ ___  _ __
| |   | |_    | |\/| |/ _ \| '_ \| | __/ _ \| '__|
| |___|  _|   | |  | | (_) | | | | | || (_) | |
 \____|_|     |_|  |_|\___/|_| |_|_|\__\___/|_|

 ____         __        ___       ____
| __ ) _   _  \ \      / (_)_ __ |  _ \ _   _ ____
|  _ \| | | |  \ \ /\ / /| | '_ \| | | | | | |_  /
| |_) | |_| |   \ V  V / | | | | | |_| | |_| |/ /
|____/ \__, |    \_/\_/  |_|_| |_|____/ \__,_/___|
       |___/

	"""
	print(bar)

	while True:
		set_color(Fore.LIGHTCYAN_EX)
		string = input("Введите хендл: ")
		if not string or string == '0':
			break

		time = None

		if input("Просмотреть в определенный день ? Y\\N: ").lower().startswith('y'):

			year = input("Введите год: ")

			if not year:
				year = datetime.now().year
			else:
				year = int(year)

			month = input("Введите месяц: ")

			if not month:
				month = datetime.now().month
			else:
				month = int(month)

			day = input("Введите день: ")

			if not day:
				day = datetime.now().day
			else:
				day = int(day)

			time = datetime(year, month, day)

		try:
			subm = get_submissions(string)
		except:
			set_color(Fore.LIGHTRED_EX)
			print("[ERROR] Такого юзера не существует или плохое соединение с интернетом...")
			continue

		
		really_solved = get_solved_tasks(subm, time)
		good_submissions_count = len(subm['good_submissions']) if not time else len(
			subm[str_date(time)]['good_submissions'])
		bad_submissions_count = len(subm['bad_submissions']) if not time else len(
			subm[str_date(time)]['bad_submissions'])
		fraud_count = abs(good_submissions_count - len(really_solved))
		power = 0
		table = []

		for s in really_solved:
			name = s
			try: lvl = really_solved[s]['problem']['rating']
			except KeyError: lvl = 'Отсуствует'
			time = datetime.fromtimestamp(really_solved[s]['creationTimeSeconds'])
			time = f"{time.year}.{time.month}.{add_zero(time.day)} {add_zero(time.hour)}:{add_zero(time.minute)}"
			lang = really_solved[s]['programmingLanguage']
			subm_count = len(
				subm[really_solved[s]['problem']['name']]['good_submissions']) + len(
				subm[really_solved[s]['problem']['name']]['bad_submissions'])
			power += lvl if type(lvl) == int else 0
			table.append([name, lvl, time, lang, subm_count])

		print(tabulate([
			['Количество успешных попыток', good_submissions_count],
			['Количество неуспешных попыток', bad_submissions_count],
			['Количество мошеннических попыток', fraud_count],
			['Количество действительно решенных задач', len(really_solved)],
			['Сила', power / 100],
			],
			tablefmt="psql"
		))
		set_color(Fore.LIGHTGREEN_EX)
		print(tabulate(table,  headers=['Имя задачи', 'Уровень', 'Время', 'Язык', 'Попытки'],
			tablefmt="psql"))
		input("Нажмите ENTER")
		clear()