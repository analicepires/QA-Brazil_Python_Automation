import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from helpers import retrieve_phone_code

class UrbanRoutesPage:
    # Seção De e Para
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')

    # Selecionar tarifa e chamar taxi
    taxi_option_locator = (By.XPATH, '//button[contains(text(),"Chamar")]')
    # Locator mais robusto para o Comfort (não depende de um SVG específico que pode mudar)
    comfort_tariff_locator = (By.XPATH, "//div[contains(@class, 'tcard') and .//div[normalize-space()='Comfort']]")
    
    # Numero de Telefone
    number_text_locator = (By.CSS_SELECTOR, '.np-button')
    number_enter = (By.ID, 'phone')
    number_confirm = (By.CSS_SELECTOR, '.button.full')
    number_code = (By.XPATH, "//input[@id='code' and not(contains(@class, 'card-input'))]")
    code_confirm = (By.XPATH, '//button[contains(text(),"Confirmar")]')
    number_finish = (By.CSS_SELECTOR, '.np-text')

    # METODO DE PAGAMENTO
    add_metodo_pagamento = (By.CSS_SELECTOR, '.pp-button.filled')
    add_card = (By.CSS_SELECTOR, '.pp-plus')
    number_card = (By.ID, 'number')
    code_card = (By.CSS_SELECTOR, 'input.card-input#code')
    add_finish_card = (By.XPATH, '//button[contains(text(),"Adicionar")]')
    close_button_card = (By.CSS_SELECTOR, '.payment-picker.open .close-button')
    comfirm_card = (By.CSS_SELECTOR, '.pp-value-text')

    # ADICIONAR COMENTARIO
    add_comment = (By.ID, 'comment')

    # REQUISITOS (Cobertor e Sorvete)
    switch_blanket = (By.XPATH, "//div[contains(@class, 'r-type-switch') and contains(., 'Cobertor')]//div[contains(@class, 'switch')]")
    switch_blanket_active = (By.XPATH, "//div[contains(@class, 'r-type-switch') and contains(., 'Cobertor')]//input[contains(@class, 'switch-input')]")
    
    add_icecream = (By.XPATH, "//div[contains(@class, 'r-group') and .//div[normalize-space()='Pote de sorvete']]//div[contains(@class, 'counter-plus')]")
    qnt_icecream = (By.XPATH, "//div[contains(@class, 'r-group') and .//div[normalize-space()='Pote de sorvete']]//div[contains(@class, 'counter-value')]")
    
    call_taxi_button = (By.CSS_SELECTOR, '.smart-button')
    pop_up = (By.CSS_SELECTOR, '.order-header-title')

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def enter_from_location(self, from_text):
        element = self.wait.until(EC.visibility_of_element_located(self.from_field))
        element.clear()
        element.send_keys(from_text)

    def enter_to_location(self, to_text):
        element = self.wait.until(EC.visibility_of_element_located(self.to_field))
        element.clear()
        element.send_keys(to_text)

    def enter_locations(self, from_text, to_text):
        self.enter_from_location(from_text)
        self.enter_to_location(to_text)

    def get_from_location_value(self):
        return self.wait.until(EC.visibility_of_element_located(self.from_field)).get_attribute('value')

    def get_to_location_value(self):
        return self.wait.until(EC.visibility_of_element_located(self.to_field)).get_attribute('value')

    def click_taxi_option(self):
        self.wait.until(EC.element_to_be_clickable(self.taxi_option_locator)).click()

    def click_comfort_icon(self):
        comfort_element = self.driver.find_element(*self.comfort_icon_locator)
        
        if "active" not in comfort_element.get_attribute("class"):
            comfort_element.click()

    def select_comfort_plan(self):
        comfort_button = self.wait.until(EC.element_to_be_clickable(self.comfort_tariff_locator))
        if "active" not in comfort_button.get_attribute("class"):
            comfort_button.click()

    def click_number_text(self, telefone):
        self.wait.until(EC.element_to_be_clickable(self.number_text_locator)).click()
        self.wait.until(EC.visibility_of_element_located(self.number_enter)).send_keys(telefone)
        self.wait.until(EC.element_to_be_clickable(self.number_confirm)).click()
        time.sleep(2)
        code = retrieve_phone_code(self.driver)
        
        code_input = self.wait.until(EC.visibility_of_element_located(self.number_code))
        code_input.clear()
        code_input.send_keys(code)
        self.wait.until(EC.element_to_be_clickable(self.code_confirm)).click()

    def numero_confirmado(self):
        return self.wait.until(EC.visibility_of_element_located(self.number_finish)).text

    def click_add_cartao(self, cartao, code):
        self.wait.until(EC.element_to_be_clickable(self.add_metodo_pagamento)).click()
        self.wait.until(EC.element_to_be_clickable(self.add_card)).click()
        
        self.wait.until(EC.visibility_of_element_located(self.number_card)).send_keys(cartao)
        
        cvv_field = self.wait.until(EC.visibility_of_element_located(self.code_card))
        cvv_field.send_keys(code)
        
        cvv_field.send_keys(Keys.TAB)
        time.sleep(0.5) # Pequena pausa para o DOM processar a perda de foco
        
        self.wait.until(EC.element_to_be_clickable(self.add_finish_card)).click()
        
        # Fechar o modal de pagamento
        try:
            self.wait.until(EC.element_to_be_clickable(self.close_button_card)).click()
        except:
            pass 

    def confirm_cartao(self):
        return self.wait.until(EC.visibility_of_element_located(self.comfirm_card)).text

    def add_comentario(self, comentario):
        self.wait.until(EC.element_to_be_clickable(self.add_comment)).send_keys(comentario)

    def coment_confirm(self):
        return self.driver.find_element(*self.add_comment).get_attribute('value')

    def switch_cobertor(self):
        self.wait.until(EC.element_to_be_clickable(self.switch_blanket)).click()

    def switch_cobertor_active(self):
        switch_input = self.wait.until(EC.presence_of_element_located(self.switch_blanket_active))
        return switch_input.is_selected()

    def order_two_ice_creams(self):
        for _ in range(2):
            self.wait.until(EC.element_to_be_clickable(self.add_icecream)).click()
            time.sleep(0.5)

    def qnt_sorvete(self):
        return self.wait.until(EC.visibility_of_element_located(self.qnt_icecream)).text

    def call_taxi(self):
        self.wait.until(EC.element_to_be_clickable(self.call_taxi_button)).click()

    def pop_up_show(self):
        return self.wait.until(EC.visibility_of_element_located(self.pop_up)).text
