
import time
from threading import Thread
from config import INI_CONFIG
from helpers.screen import cls
import json


from queue import Queue




def getch():
    return input()


class Dashboard:
    FIRST_RUN = True
    ACCOUNTS_TO_CREATE = 0
    THREADS = INI_CONFIG['THREADS']
    ACCOUNTS_CREATED = 0
    FAILRUES = 0
    ACCOUNTS_IN_DATABASE = 0
    WAITING_FOR_CAPTCHA = 0

    def makedec(val):
        return '{:,}'.format(val)

    def makedash():
        cls()
        strr = """

        +----------------------------+----------------------------------------+
          BOT Status                 | %s                                     
        +----------------------------+----------------------------------------+
          Configured threads         | %s                                     
        +----------------------------+----------------------------------------+
          Bots waiting for captcha   | %s                                     
        +----------------------------+----------------------------------------+
          Accounts created           | %s                                     
        +----------------------------+----------------------------------------+
          Failures                   | %s                                     
        +----------------------------+----------------------------------------+
          Accounts created all-time  | %s                                     
        +----------------------------+----------------------------------------+

        """ % (
            "%s. Press S to start" % ("STOPPED" if Dashboard.FIRST_RUN else "Finished") if Dashboard.ACCOUNTS_TO_CREATE == 0 else "Creating %s accounts" % (
                Dashboard.ACCOUNTS_TO_CREATE),

            Dashboard.THREADS,
            Dashboard.WAITING_FOR_CAPTCHA,
            Dashboard.ACCOUNTS_CREATED,
            Dashboard.FAILRUES,
            Dashboard.ACCOUNTS_IN_DATABASE


        )
        print(strr)
        print(
            "[S] (Input number of accounts to create)  [T] (Generate TXT File with all accounts)  [D] (Delete all accounts from DB)]\n> ")

    def run(start_bot):
        while True:
            Dashboard.makedash()
            io = getch().lower()
            if io == "t":
                from actions import generate_accounts_txt
                cls()
                generated_cnt = generate_accounts_txt()
                print("[+] TXT file generated with %s accounts. Filepath: %s " %
                      (
                          generated_cnt,
                          INI_CONFIG['SAVE_ACCOUNTS_TEXTFILE_PATH'])
                      )
                input("Press any key to continue...")
            elif io == "d":
                from actions import delete_all_accounts
                cls()
                print("[!] Deleting all accounts from DB? (y/n)")
                y = getch().lower()
                if y == "y":
                    delete_all_accounts()
                    print("[!] All accounts deleted!")
                    input("[!] Press any key to continue...\n")
            elif io == 's':
                cls()
                try:
                    accs = int(input("Input amount accounts to create...\n> "))
                except:
                    continue
                start_bot(accs)
            else:
                continue
