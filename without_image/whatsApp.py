import pandas as pd
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By


class WhatsApp(webdriver.Chrome):

    def __init__(self, teardown=False):

        # self.driver = webdriver.Chrome(ChromeDriverManager().install())/§
        self.teardown = teardown
        options = webdriver.ChromeOptions()
        # options.add_experimental_option('excludeSwitches', ['enable-logging'])
        # options.add_argument("--headless")
        super(WhatsApp, self).__init__(options=options)
        self.implicitly_wait(30)
        # self.maximize_window()

    def __exit__(self, exc_type, exc_val, exc_tb):

        if self.teardown:
            self.quit()

    def land_on_whatsapp(self):
        self.get('https://web.whatsapp.com')

    def get_recipients(self, xlsx_name, sheet_name=''):

        if sheet_name == '':
            recipients=pd.read_excel(f"{xlsx_name}.xlsx", sheet_name='Sheet1')
        else:
            recipients=pd.read_excel(f"{xlsx_name}.xlsx", sheet_name=sheet_name)
        return recipients

    def send_message(self, phone_number, message):

        url = f'https://web.whatsapp.com/send?phone=+{str(int(phone_number))}&text={message}'
        self.get(url)
        sleep(2)
        try:
            click_btn = self.find_element(
                by=By.XPATH,
                value='//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[2]/button/span'
                )
        except Exception:
            print("Sorry message could not sent to " + str(phone_number))
        else:
            click_btn.click()
            sleep(1)
            print('Message sent to: ' + str(phone_number))