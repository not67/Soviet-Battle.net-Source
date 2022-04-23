
from config import INI_CONFIG
from db import delete_all_accounts, get_all_accounts, save_account

from services.bot import Bot


def generate_accounts_txt():
    accs = get_all_accounts()
    cnt = 0
    with open(INI_CONFIG['SAVE_ACCOUNTS_TEXTFILE_PATH'], "w") as f:
        for acc in accs:
            cnt += 1
            f.write(str(acc[0]) + ":" + str(acc[1]) + ':' + str(acc[2]) + ':' + str(acc[3]) + "\n")
    return cnt


def start_bot(accs):
    Bot.start_bot(accs)
