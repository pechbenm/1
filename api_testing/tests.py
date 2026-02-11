from user_api import UserAPI
from store_api import StoreAPI
import time
import random
from pydantic import BaseModel
import allure
import pytest
import json

class UserData(BaseModel):
    id: int
    username: str
    firstName: str
    lastName: str
    email: str
    password: str
    phone: str
    userStatus: int

class OrderData(BaseModel):
    id: int
    petId: int
    quantity: int
    shipDate: str
    status: str
    complete: bool

def safe_json(response):
    try:
        return json.dumps(response.json(), indent=2, ensure_ascii=False)
    except Exception:
        return response.text or "Нет данных"

@allure.feature("Магазин")
class TestStoreAPI:
    
    @pytest.fixture(autouse=True)
    def setup(self):
        self.base_url = "https://petstore.swagger.io/v2"
        self.store_api = StoreAPI(self.base_url)
        self.order_id = random.randint(10000, 99999)
    
    @allure.title("Тест жизненного цикла заказа")
    def test_store_crud(self):
        allure.attach(str(self.order_id), name="ID заказа")
        
        with allure.step("Получить инвентарь"):
            inventory_response = self.store_api.get_inventory()
            allure.attach(safe_json(inventory_response), name="Ответ сервера")
            assert inventory_response.status_code == 200, f"Ошибка получения инвентаря: {inventory_response.status_code}"
        
        with allure.step("Создать заказ"):
            order_data = OrderData(
                id=self.order_id,
                petId=12345,
                quantity=1,
                shipDate="2024-01-20T10:00:00.000Z",
                status="placed",
                complete=True
            )
            create_response = self.store_api.create_order(order_data.model_dump())
            allure.attach(safe_json(create_response), name="Ответ сервера")
            assert create_response.status_code == 200, f"Ошибка создания заказа: {create_response.status_code}"
        
        with allure.step("Получить заказ по ID"):
            get_response = self.store_api.get_order(self.order_id)
            allure.attach(safe_json(get_response), name="Ответ сервера")
            assert get_response.status_code == 200, f"Ошибка получения заказа: {get_response.status_code}"
        
        with allure.step("Удалить заказ"):
            delete_response = self.store_api.delete_order(self.order_id)
            allure.attach(safe_json(delete_response), name="Ответ сервера")
            assert delete_response.status_code == 200, f"Ошибка удаления заказа: {delete_response.status_code}"


@allure.feature("Пользователи")
class TestUserAPI:
    
    @pytest.fixture(autouse=True)
    def setup(self):
        self.base_url = "https://petstore.swagger.io/v2"
        self.user_api = UserAPI(self.base_url)
        self.timestamp = int(time.time())
        self.username = f"student_{self.timestamp}"
    
    @allure.title("Тест жизненного цикла пользователя")
    def test_user_crud(self):
        allure.attach(self.username, name="Имя пользователя")
        
        with allure.step("Создать пользователя"):
            user_data = UserData(
                id=self.timestamp,
                username=self.username,
                firstName="Иван",
                lastName="Иванов",
                email=f"ivan{self.timestamp}@mail.ru",
                password="password123",
                phone="1234567890",
                userStatus=1
            )
            create_response = self.user_api.create_user(user_data.model_dump())
            allure.attach(safe_json(create_response), name="Ответ сервера")
            assert create_response.status_code == 200, f"Ошибка создания пользователя: {create_response.status_code}"
        
        with allure.step("Получить пользователя"):
            get_response = self.user_api.get_user(self.username)
            allure.attach(safe_json(get_response), name="Ответ сервера")
            assert get_response.status_code == 200, f"Ошибка получения пользователя: {get_response.status_code}"
            user_info = get_response.json()
            assert user_info['username'] == self.username
        
        with allure.step("Обновить пользователя"):
            updated_data = UserData(
                id=self.timestamp,
                username=self.username,
                firstName="Петр",
                lastName="Петров",
                email=f"petr{self.timestamp}@mail.ru",
                password="newpassword456",
                phone="0987654321",
                userStatus=1
            )
            update_response = self.user_api.update_user(self.username, updated_data.model_dump())
            allure.attach(safe_json(update_response), name="Ответ сервера")
            assert update_response.status_code == 200, f"Ошибка обновления пользователя: {update_response.status_code}"
        
        with allure.step("Удалить пользователя"):
            delete_response = self.user_api.delete_user(self.username)
            allure.attach(safe_json(delete_response), name="Ответ сервера")
            assert delete_response.status_code == 200, f"Ошибка удаления пользователя: {delete_response.status_code}"