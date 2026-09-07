import data
import helpers
# tarefa 03
class TestUrbanRoutes:
    # tarefa 4
    @classmethod
    def setup_class(cls):
        if is_url_reachable(URBAN_ROUTES_URL):
            print("Conectado ao servidor Urban Routes")
        else:
            print("Não foi possível conectar ao Urban Routes. Verifique se o servidor está ligado e ainda em execução.")

    def test_set_route(self):
        # Adicionar em S8
        pass
    def test_select_plan(self):
        # Adicionar em S8
        pass
    def test_fill_phone_number(self):
        # Adicionar em S8
        pass
    def test_fill_card(self):
        # Adicionar em S8
        pass
    def test_comment_for_driver(self):
        # Adicionar em S8
        pass
    def test_order_blanket_and_handkerchiefs(self):
        # Adicionar em S8
        pass
    def test_order_2_ice_creams(self):
        #tarefa 5
        for i in range():
            #Adicionar em S8
            pass
    def test_car_search_model_appears(self):
        # Adicionar em S8
        pass

if __name__ == "__main__":
    objeto = TestUrbanRoutes()
    objeto.test_set_route()