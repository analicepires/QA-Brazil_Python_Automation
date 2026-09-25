from pages import UrbanRoutesPage
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import data
import helpers

class TestUrbanRoutes:
    @classmethod
    def setup_class(cls):
        if helpers.is_url_reachable(data.URBAN_ROUTES_URL):
            print("Conectado a servidor Urban Routes")
        else:
            print("Não foi possível conectar ao Urban Routes. Verifique se o servidor está ligado e ainda em execução")

        from selenium.webdriver import DesiredCapabilities
        capabilities = DesiredCapabilities.CHROME
        capabilities["goog:loggingPrefs"] = {'performance': 'ALL'}
        cls.driver = webdriver.Chrome()

    def test_set_route(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.enter_locations(data.ADDRESS_FROM, data.ADDRESS_TO)
        
        assert routes_page.get_from_location_value() == data.ADDRESS_FROM
        assert routes_page.get_to_location_value() == data.ADDRESS_TO

    def test_select_plan(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.enter_locations(data.ADDRESS_FROM, data.ADDRESS_TO)
        
        routes_page.click_taxi_option()
        routes_page.select_comfort_plan()
        
        comfort_element = routes_page.driver.find_element(*routes_page.comfort_tariff_locator)
        assert "active" in comfort_element.get_attribute("class")

    def test_fill_phone_number(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.enter_locations(data.ADDRESS_FROM, data.ADDRESS_TO)
        routes_page.click_taxi_option()
        routes_page.select_comfort_plan()
        
        phone_clean = data.PHONE_NUMBER.replace(" ", "")
        routes_page.click_number_text(phone_clean)

        displayed_number = routes_page.numero_confirmado().replace(" ", "")
        assert phone_clean in displayed_number

    def test_fill_card(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.enter_locations(data.ADDRESS_FROM, data.ADDRESS_TO)
        routes_page.click_taxi_option()
        routes_page.select_comfort_plan()
        
        routes_page.click_add_cartao(data.CARD_NUMBER, data.CARD_CODE)
        assert "Cartão" in routes_page.confirm_cartao()

    def test_comment_for_driver(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.enter_locations(data.ADDRESS_FROM, data.ADDRESS_TO)
        routes_page.click_taxi_option()
        routes_page.select_comfort_plan()
        
        routes_page.add_comentario(data.MESSAGE_FOR_DRIVER)
        assert data.MESSAGE_FOR_DRIVER in routes_page.coment_confirm()

    def test_order_blanket_and_handkerchiefs(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.enter_locations(data.ADDRESS_FROM, data.ADDRESS_TO)
        routes_page.click_taxi_option()
        routes_page.select_comfort_plan()
        
        routes_page.switch_cobertor()
        assert routes_page.switch_cobertor_active() is True

    def test_order_2_ice_creams(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.enter_locations(data.ADDRESS_FROM, data.ADDRESS_TO)
        routes_page.click_taxi_option()
        routes_page.select_comfort_plan()
        routes_page.order_two_ice_creams()
        assert int(routes_page.qnt_sorvete()) == 2

    def test_car_search_model_appears(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        routes_page = UrbanRoutesPage(self.driver)
        
        # Fluxo completo para pedir o taxi
        routes_page.enter_locations(data.ADDRESS_FROM, data.ADDRESS_TO)
        routes_page.click_taxi_option()
        routes_page.select_comfort_plan()
        phone_clean = data.PHONE_NUMBER.replace(" ", "")
        routes_page.click_number_text(phone_clean)
        routes_page.click_add_cartao(data.CARD_NUMBER, data.CARD_CODE)
        routes_page.add_comentario(data.MESSAGE_FOR_DRIVER)
        routes_page.switch_cobertor()
        routes_page.order_two_ice_creams()
        
        # Pedido final
        routes_page.call_taxi()
        
        # Verifica se o modal apareceu (O texto pode ser "Buscar carro" ou "Procurando carro")
        popup_text = routes_page.pop_up_show()
        assert "Buscar" in popup_text or "Procurando" in popup_text

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()