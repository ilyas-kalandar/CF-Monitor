from datetime import datetime
from colorama import init, Fore
from cfparser import Parser
from tabulate import tabulate
from utils import days_ago, cross_platform_clear

BANNER = """
  ____ _____      __  __             _ _
 / ___|  ___|    |  \/  | ___  _ __ (_) |_ ___  _ __
| |   | |_  ____ | |\/| |/ _ \| '_ \| | __/ _ \| '__|
| |___|  _| ____ | |  | | (_) | | | | | || (_) | |
 \____|_|        |_|  |_|\___/|_| |_|_|\__\___/|_|
 ____         __        ___       ____
| __ ) _   _  \ \      / (_)_ __ |  _ \ _   _ ____
|  _ \| | | |  \ \ /\ / /| | '_ \| | | | | | |_  /
| |_) | |_| |   \ V  V / | | | | | |_| | |_| |/ /
|____/ \__, |    \_/\_/  |_|_| |_|____/ \__,_/___|
       |___/
 """

VERSION = 0.5

def main():
    init()
    print(Fore.LIGHTCYAN_EX + BANNER)
    print(Fore.LIGHTYELLOW_EX)
    print(f"VERSION {VERSION}")
    print("github.com/ilyas-kalandar/cf-monitor")
    parser = Parser()
    while True:
        try:
            print(Fore.LIGHTWHITE_EX)
            handle = input("Enter your handle: ")
            if not handle:
                continue

            parser.set_handle(handle)
            parser.clear()

            if not parser.check_handle():
                print(Fore.LIGHTRED_EX + "Error, user does not exits.")
                continue

            try:
                parser.parse()
            except ConnectionError:
                print(Fore.LIGHTRED_EX + "Connection error, oh no...")
                continue

            date = None

            if input("Do you want to see submissions on a specific day? Y\\N: ").lower().startswith("y"):
                d = input("Input day: ")
                if d:
                    day = int(d)
                else:
                    day = datetime.now().day

                m = input("Input month: ")
                if m:
                    month = int(m)
                else:
                    month = datetime.now().month

                y = input("Enter year: ")

                if y:
                    year = int(y)
                else:
                    year = datetime.now().year

                date = datetime(year, month, day)

            accepted_submissions = parser.get_submissions(
                date=date, verdict="OK", check=True)
            all_accepted_submissions = parser.get_submissions(
                to=datetime.now(), check=True, verdict='OK'
            )
            rejected_submissions = parser.get_submissions(
                date=date, verdict="N")
            not_checked_submissions = parser.get_submissions(
                date=date, verdict="OK")

            accepted_submissions_two_days_ago = parser.get_submissions(
                to=days_ago(date if date else datetime.now(), 2), verdict="OK", check=True)

            power = 0
            power_two_days_ago = 0
            power_today = 0

            for s in accepted_submissions:
                try:
                    power_today += accepted_submissions[s][-1].rating
                except KeyError:
                    power_today += 800

            for s in all_accepted_submissions:
                try:
                    power += all_accepted_submissions[s][-1].rating
                except TypeError:
                    power += 800

            for s in accepted_submissions_two_days_ago:
                try:
                    power_two_days_ago += all_accepted_submissions[s][-1].rating
                except TypeError:
                    power_two_days_ago += 800

            print(Fore.LIGHTYELLOW_EX + f"\nStatistics of user {handle.capitalize()}")

            try:
                increase_in_percentage = int(
                    power / (power_two_days_ago // 100)) - 100
            except ZeroDivisionError:
                increase_in_percentage = power

            s_count = len(parser.get_submissions(date=date))
            s_count_two_days_ago = len(
                parser.get_submissions(date=days_ago(date, 2)))

            hardworking_increase = s_count - s_count_two_days_ago

            statistics = [
                ["Power", power // 100],
                [f"Power on {date.year}:{date.month}:{date.day}", power_today // 100],
                ["Total submissions", len(
                    rejected_submissions) + len(not_checked_submissions)],
                ["Total accepted submissions", len(accepted_submissions)],
                ["Total rejected submissions", len(rejected_submissions)],
                ["User rating", parser.userinfo['rating']],
                ["Increase",
                    f"{(power // 100) - (power_two_days_ago // 100)} | {increase_in_percentage}%"],
                ["Hardworking Increase", hardworking_increase]
            ]

            table = []
            for a in accepted_submissions:
                s = accepted_submissions[a][-1]
                try:
                    bad_submissions_count = len(parser.get_submissions(
                        verdict="nok",
                        problem_name=s.problem_name,
                    )[s.problem_name])
                except KeyError:
                    bad_submissions_count = 0

                table.append([
                    s.problem_name,
                    s.rating,
                    s.programming_lang,
                    bad_submissions_count,
                    datetime.fromtimestamp(s.creation_time),
                ]
                )
            print(Fore.LIGHTGREEN_EX, end='')
            print(tabulate(statistics, tablefmt='psql', ))
            print(tabulate(table, tablefmt='psql', headers=[
                "Problem", "Rating", "LANG", "Bad submissions", "Time"
            ]))
            input("Press enter")
            cross_platform_clear()
        except KeyboardInterrupt:
            print(Fore.LIGHTGREEN_EX + "\nExiting...")
            return


if __name__ == '__main__':
    main()
