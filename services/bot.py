import concurrent.futures
from pickle import NONE
from driver.bots.battlenet import BattlenetAccountCreator
from services.logger import logger
from db import save_account
from services.dashboard import Dashboard
from multiprocessing.pool import ThreadPool
from threading import Semaphore
from config import INI_CONFIG
import gc


class Bot:

    SEMAPHORE = Semaphore(INI_CONFIG['THREADS'])
    THREADS = None

    @staticmethod
    def on_account_created(*args):
        email, phone, password = args[0]
        Bot.SEMAPHORE.release()
        """
        Function invoked directly as callback from the account generator in a threaded context
        """
        save_account(email, phone, password)
        Dashboard.ACCOUNTS_CREATED += 1
        Dashboard.ACCOUNTS_TO_CREATE -= 1
        gc.collect()

    @staticmethod
    def on_account_creation_failure(*args):
        logger.log("[ERROR] Account creation failure: " + str(args))
        Dashboard.FAILRUES += 1
        Dashboard.ACCOUNTS_TO_CREATE -= 1
        gc.collect()

    @staticmethod
    def start_bot(accs_number: int):
        Dashboard.FAILRUES = 0
        Dashboard.ACCOUNTS_CREATED = 0
        Dashboard.ACCOUNTS_TO_CREATE = accs_number

        threads = INI_CONFIG['THREADS']
        Bot.THREADS = ThreadPool(threads)
        Bot.SEMAPHORE = Semaphore(threads)

        for i in range(accs_number):

            bot = BattlenetAccountCreator()

            Bot.THREADS.apply_async(
                bot.run,
                error_callback=Bot.on_account_creation_failure,
                callback=Bot.on_account_created,
            )
