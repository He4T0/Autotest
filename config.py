import os
import sys
import logging
from datetime import datetime

# paths
project_path = os.path.abspath(os.getcwd())
libs_path = project_path + "/libs"
resources_path = project_path + "/resources"
google_token = resources_path + "/stable-ring-316114-8acf36454762.json"
chromedriver = resources_path + "/chromedriver" if sys.platform == "linux" else resources_path + "/chromedriver.exe"
autotest_results = project_path + "/../autotest-results"
allure_results = project_path + "/../allure-results"
# telegram socket
IP = "127.0.0.1"
PORT = 1234
# gather the logs
today = datetime.now().date()
fname = autotest_results + "/logs" + "/" + str(today) + ".log"
if not os.path.exists(fname):
    with open(fname, "w"): pass
logging.basicConfig(filename=fname,
                    format='%(asctime)s|%(levelname)s|%(message)s',
                    level=logging.WARNING,
                    datefmt='%d/%m/%Y %H:%M:%S')
logger = logging
# DB
db_login = "kali"
db_password = "P3N7dbw3"
# sdo.Niidpo.ru
listener_login = "an.karenovna@yandex.ru"
listener_password = "an.karenovna"
listener_months_SSID = {
    8: "1u88yKDi46j1AjpSxVr2tp1sdt1oKyCzoLkSXZ99cGh4",
    9: "1zXsJTkKzEnli-TAIuKL27cV1_54y4BjwOYCNKKYCrSM",
    10: "1cxBX10S5_NKYk7qpjBjtjBwatb7boosR9qAjeMX86dw",
    11: "1JU7xbBQVN8Fisg4A678okvBn_Z4J6_3pq_VW3HNkwTc"
}