import data
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import time
from selenium.webdriver.chrome.options import Options


# no modificar
def retrieve_phone_code(driver) -> str:
    """Este código devuelve un número de confirmación de teléfono y lo devuelve como un string.
    Utilízalo cuando la aplicación espere el código de confirmación para pasarlo a tus pruebas.
    El código de confirmación del teléfono solo se puede obtener después de haberlo solicitado en la aplicación."""

    import json
    import time
    from selenium.common import WebDriverException
    code = None
    for i in range(10):
        try:
            logs = [log["message"] for log in driver.get_log('performance') if log.get("message")
                    and 'api/v1/number?number' in log.get("message")]
            for log in reversed(logs):
                message_data = json.loads(log)["message"]
                body = driver.execute_cdp_cmd('Network.getResponseBody',
                                              {'requestId': message_data["params"]["requestId"]})
                code = ''.join([x for x in body['body'] if x.isdigit()])
        except WebDriverException:
            time.sleep(1)
            continue
        if not code:
            raise Exception("No se encontró el código de confirmación del teléfono.\n"
                            "Utiliza 'retrieve_phone_code' solo después de haber solicitado el código en tu aplicación.")
        return code

#▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄#
#▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄#
#▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄#
#▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄#
class UrbanRoutesPage:
    from_field = (By.ID, 'from') #Campo de direccion "desde"
    to_field = (By.ID, 'to') #Campo de direccion "hasta"
    orderTaxiButton = (By.XPATH, '//*[@class="workflow-subcontainer"]/div/div[@class="results-container"]/div[@class="results-text"]/button')  # boton de "pedir un taxi" ▄
    selectComfortButton = (By.ID, 'tariff-card-4') #boton de seleccion "comfort"▄
    phoneButton = (By.CLASS_NAME, 'np-text') #boton de agregar numero de telefono▄
    phoneButtonField = (By.ID, 'phone') #para hacer click en el field e ingresar un telefono despues▄
    nextButton_PhoneField = (By.CLASS_NAME, 'button full') #boton para "siguiente" y te lleve a lo del codigo▄
    phoneCodeField = (By.XPATH, '//*[@id="code"]') #donde se pone el codigo que te da por ingresar el telefono
    confirmButtonCodefield = (By.CLASS_NAME, 'submit') #boton de confirmar, para cerrar la ventana donde se pone el codigo▄
    payMethodMenu = (By.CLASS_NAME, 'pp-text') #boton "metodo de pago"▄
    addPayMethodButton = (By.CLASS_NAME, 'pp-title') #boton "agregar tarjeta"▄
    cardNumberField = (By.ID, 'number') #campo para agregar el numero de tarjeta▄
    cardNumberCVV = (By.NAME, 'code') # campo de CVV▄
    endAddCard = (By.CLASS_NAME, 'button full') # boton de "agregar" en la ventana emergente de agregar tarjeta▄
    endCloseCardWindow = (By.CLASS_NAME, 'close-button section-close') # Boton para cerrar la ventana emergente de agregar tarjeta▄
    tellDriverComment = (By.CLASS_NAME, 'label')# field de "Mensaje para el conductor"▄
    toggleBlanketTissues = (By.CLASS_NAME, 'slider round') #el slider/boton de si llevar cobija y pañuelos▄
    addIceCream = (By.CLASS_NAME, 'counter-plus') #boton de agregar un helado▄
    finishOrderTaxiButton = (By.CLASS_NAME, 'smart-button') #boton para terminar de ordenar un taxi, para que empeice la busqueda de tu auto▄






    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)

    def set_from(self, from_address):
        self.wait.until(EC.presence_of_element_located(self.from_field)).send_keys(from_address)

    def set_to(self, to_address):
        self.wait.until(EC.presence_of_element_located(self.to_field)).send_keys(to_address)

    def set_route(self, from_address, to_address):
        self.set_from(from_address)
        self.set_to(to_address)

    def get_from(self):
        return self.driver.find_element(*self.from_field).get_property('value')

    def get_to(self):
        return self.driver.find_element(*self.to_field).get_property('value')

    def hacerclick_taxi(self):
        button = WebDriverWait(self.driver, 3).until(EC.element_to_be_clickable(self.orderTaxiButton))
        button.click()
        #print('hizo click')

    def click_On_Comfort_button(self):
        self.driver.find_element(*self.selectComfortButton).click()

    def click_On_Phone_button_Menu(self):
        self.driver.find_element(*self.phoneButton).click()

    def add_Phone_field(self, phone_number):
        self.driver.find_element(*self.phoneButtonField).send_keys(phone_number)

    def click_on_next_button_phone_field(self):
        self.driver.find_element(*self.nextButton_PhoneField).click()

    def add_phone_codesms(self):
        code = retrieve_phone_code(driver=self.driver)
        self.driver.find_element(*self.phoneCodeField).send_keys(code)

    def click_on_confirm_button_phone_field(self):
        self.driver.find_element(*self.confirmButtonCodefield).click()

    def click_on_patMethodMenu(self):
        self.driver.find_element(*self.payMethodMenu).click()

    def click_on_addPayMethodButton(self):
        self.driver.find_element(*self.addPayMethodButton).click()

    def add_card_Number_Field(self, card_number):
        self.driver.find_element(*self.cardNumberField).send_keys(card_number)

    def add_cvv_field(self, card_cvv_number):
        self.driver.find_element(*self.cardNumberCVV).send_keys(card_cvv_number)

    def click_on_endAddCard(self):
        self.driver.find_element(*self.endAddCard).click()

    def click_on_endCloseCardWindow(self):
        self.driver.find_element(*self.endCloseCardWindow).click()

    def write_driver_a_message(self, message):
        self.driver.find_element(*self.tellDriverComment).send_keys(message)

    def  click_on_toggleBlanket(self):
        self.driver.find_element(*self.toggleBlanketTissues).click()

    def click_on_add_ice_cream(self):
        option_add_controls = self.driver.find_elements(*self.addIceCream)
        self.driver.execute_script("arguments[0].scrollIntoView();", option_add_controls[0])
        option_add_controls[0].click()
        option_add_controls[0].click()


class TestUrbanRoutes:

    driver = None

    @classmethod
    def setup_class(cls):
        # no lo modifiques, ya que necesitamos un registro adicional habilitado para recuperar el código de confirmación del teléfono
        from selenium.webdriver import DesiredCapabilities
        capabilities = DesiredCapabilities.CHROME
        capabilities["goog:loggingPrefs"] = {'performance': 'ALL'}
        chrome_options = Options()
        chrome_options.add_argument('window-size=1920,1080')
        cls.driver = webdriver.Chrome()
        driver = webdriver.Chrome(options=chrome_options)
        #driver.get(data.urban_routes_url)



    #paso 2 ya esta hecho arriba, hasta donde se ponen las direcciones

    #paso 3 clickear el boton de "pedir un taxi"
    #def test_click_on_pedirUnTaxi(self):
    #    self.hacerclick_taxi()

    def test_set_route(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        address_from = data.address_from
        address_to = data.address_to
        routes_page.set_route(address_from, address_to)
        time.sleep(3)

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()