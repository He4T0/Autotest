from contextlib import contextmanager
from time import time

from conftest import allure_step
from libs.func4test import *
import re
import zlib
from urllib.parse import unquote
from pages.workPage import Pages

class Form:

    granddad = None
    name = None
    phone = None
    email = None
    button = ".//button"
    # "//button"
    callButton = None
    # If form if ready for test
    isready = True

    __emailDefault__ = "tester_form@gaps.edu.ru"
    __phoneDefault__ = "71234567890"
    __nameDefault__ = "Автотест"

    _email_ = {"class": ["email", "e-mail"], "placeholder": ["email", "e-mail", "email*", "e-mail*"],
                        "name": ["email", "e-mail"]}
    _phone_ = {"class": ["phone"], "placeholder": ["телефон", "телефон*"], "name": ["phone"]}
    _name_ = {"class": ["name", "fio"], "placeholder": ["фио", "фио*", "имя", "имя*"], "name": ["name", "fio"]}
    confirm = ["спасибо", "ваша заявка", "ожидайте", "менеджер", "перезвоним", "свяжется"]
    
  
class PageForm(Pages):

    def findform(self, *args, xpath=None, **kwargs):
        self.form = Form()
        if xpath is not None:
            self.form.granddad = self.findElement(xpath)
            args = self.searchElemsAtGranddad(self.form.granddad, f"({xpath})//input")

        self.form.name =  self.assigningAnArgumentField(args, self.form._name_)
        self.form.phone =  self.assigningAnArgumentField(args, self.form._phone_)
        self.form.email = self.assigningAnArgumentField(args, self.form._email_)
      
        if self.form.granddad is None:
            self.form.granddad = args[0].find_element("xpath", "..").find_element("xpath", "..").find_element("xpath", "..")
         
        try:
            data_test = self.getAttr(self.form.granddad)["data-test"]
            self.form.callButton = f"//button[@data-test='{data_test}']"
        except Exception as e:
            pass
        if any(map(lambda i: i is None, (self.form.name, self.form.phone, self.form.button))):
            self.form.isready = False

    def action(self, obj, act: str, data=None):
        def do(obj, act, data):
            if act == "send_keys":
                self.writingTextInField(input=obj, text=data)
            elif act == "click":
                self.clickButton(obj, self.form.granddad)

        # self.driver.execute_script(f"window.scrollTo(0, {obj.location['y'] - 400});")      
        for _ in range(10):
            try:
                do(obj, act, data)
                return True
            except:
                self.sleepPage(0.1)
        do(obj, act, data)

    def Test(self):
        return self.Evaluation()

    def Evaluation(self):
        if self.form.callButton is not None:
            self.callPopup()
        text_before = self.outTextElem("//body")
        # self.driver.backend.storage.clear_requests()
        try:
            self.fillForm()
        except Exception as e:
            raise Exception(f"Не получилось заполнить форму: {e}")
        # answer = self.answerEvaluation()
        # confirmation = self.confirmationEvaluation(text_before)
        confirmation = self.waitEvaluation(text_before)
        # return answer, confirmation
        return confirmation

    def callPopup(self):
        try:
            self.buttonCallPopup = self.findElement(self.form.callButton)
        except:
            self.buttonCallPopup = None
        try:
            if self.buttonCallPopup:
                self.buttonCallPopup.click()
        except Exception as e:
            raise Exception(f"Не удалось открыть поп-ап: {e}")

    def fillForm(self):
        try:
            self.action(obj=self.form.name, act="send_keys", data=self.form.__nameDefault__)
        except Exception as e:
            raise e
        # self.name.send_keys(self.__nameDefault__)
        self.action(obj=self.form.phone, act="send_keys", data=self.form.__phoneDefault__[1:])
        # self.phone.send_keys(self.__phoneDefault__[1:])
        self.sleepPage(1)
        if self.form.email is not None:
            self.action(obj=self.form.email, act="send_keys", data=self.form.__emailDefault__)
        self.action(obj=self.form.button, act="click")

    def findSendingRequest(self):
        with allure_step(f"Поиск отправленного запроса"):
            for request in self.getRequest:
                if request.response:
                    if request.response.headers['Content-Type'] == 'text/html; charset=UTF-8':
                        try:
                            rt = ''.join(re.findall(r'[0-9]*', request.body.decode("utf-8")))
                            if (rt != '') and (re.search(r'1234567890', rt).group(0) == '1234567890'):
                                # print(zlib.decompress(request.response.body, 16 + zlib.MAX_WBITS).decode())
                                return request
                        except:
                            continue
            return None

    def waitEvaluation(self, text_before, timeout=10, delta=0.25):
        start = time()
        while time() - start < timeout:
            request = self.confirmationEvaluation(text_before)
            if request:
                return request
                break
            self.sleepPage(delta)
        raise TimeoutError("Запрос не найден")

    def waitRequest(self, timeout=10, delta=0.25):
        start = time()
        while time() - start < timeout:
            request = self.findSendingRequest()
            if request:
                return request
                break
            self.sleepPage(delta)
        raise TimeoutError("Запрос не найден")

    def answerEvaluation(self):
        request = self.waitRequest()
        try:
            content_encoding = request.response.headers["content-encoding"]
            text = zlib.decompress(request.response.body, 16 + zlib.MAX_WBITS).decode()
        except:
            text = unquote(request.response.body.decode())
        return any([conf in text for conf in self.confirm])

    def confirmationEvaluation(self, text_before):
        with allure_step(f"Обработка результата"):
            text_after = self.outTextElem("//body")
            _, txt_after = compareLists(str2list(text_before), str2list(text_after))
            return any([conf in txt.lower() for txt in txt_after for conf in self.form.confirm])
