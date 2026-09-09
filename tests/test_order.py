import pytest
from api.login_api import LoginAPI
from api.product_api import ProductAPI
from api.order_api import OrderAPI
from testdata.order_data import order_create_data, order_status_data, order_query_data
from utils.logger import Logger
from utils.database import Database


class TestOrder:
    def setup_method(self):
        self.login_api = LoginAPI()
        self.product_api = ProductAPI()
        self.order_api = OrderAPI()
        self.logger = Logger()
        self.db = Database()
        self._login()
        self.test_product_id = self._create_test_product()

    def _login(self):
        login_response = self.login_api.login("admin", "admin123")
        if login_response.status_code == 200:
            token = login_response.json().get("token")
            self.product_api.set_token(token)
            self.order_api.set_token(token)

    def _create_test_product(self):
        create_response = self.product_api.create_product("订单测试商品", 49.99, 100, "订单分类")
        if create_response.status_code == 201:
            return create_response.json().get("id")
        return None

    def teardown_method(self):
        pass

    @pytest.mark.parametrize("product_id, quantity, address, expected_code", order_create_data)
    def test_create_order(self, product_id, quantity, address, expected_code):
        self.logger.info(f"执行测试用例: 创建订单 - product_id={product_id}, quantity={quantity}")
        
        if product_id == 1:
            product_id = self.test_product_id
        
        response = self.order_api.create_order(product_id, quantity, address)
        
        assert response.status_code == expected_code, f"预期状态码{expected_code}，实际{response.status_code}"
        
        if expected_code == 201:
            data = response.json()
            assert "id" in data, "响应中缺少id字段"
            assert data.get("product_id") == product_id, "商品ID不匹配"
            assert data.get("quantity") == quantity, "数量不匹配"
            assert data.get("address") == address, "地址不匹配"
            assert data.get("status") == "pending", "订单状态不正确"
            # DB层校验：验证订单已写入数据库
            db_order = self.db.get_order(data["id"])
            assert db_order, f"DB层校验失败：订单id={data['id']}未写入数据库"
            assert db_order[0]["product_id"] == product_id, "DB层校验：订单商品ID不一致"
            assert db_order[0]["quantity"] == quantity, "DB层校验：订单数量不一致"
            assert db_order[0]["status"] == "pending", "DB层校验：订单状态不一致"
            self.logger.info(f"创建订单测试通过(含DB校验)，订单ID: {data.get('id')}")
        else:
            self.logger.info(f"创建订单测试通过(异常场景)")

    @pytest.mark.parametrize("page, size, status, user_id", order_query_data)
    def test_get_order_list(self, page, size, status, user_id):
        self.logger.info(f"执行测试用例: 查询订单列表 - page={page}, size={size}, status={status}")
        response = self.order_api.get_order_list(page, size, status, user_id)
        
        assert response.status_code == 200, f"预期状态码200，实际{response.status_code}"
        
        data = response.json()
        assert "list" in data, "响应中缺少list字段"
        assert "total" in data, "响应中缺少total字段"
        assert "page" in data, "响应中缺少page字段"
        assert "size" in data, "响应中缺少size字段"
        
        self.logger.info(f"查询订单列表测试通过，共{data.get('total')}条记录")

    def test_get_order_by_id(self):
        self.logger.info("执行测试用例: 查询单个订单")
        
        create_response = self.order_api.create_order(self.test_product_id, 2, "查询订单测试地址")
        assert create_response.status_code == 201, "创建订单失败"
        
        order_id = create_response.json().get("id")
        
        response = self.order_api.get_order_by_id(order_id)
        assert response.status_code == 200, f"预期状态码200，实际{response.status_code}"
        
        data = response.json()
        assert data.get("id") == order_id, "订单ID不匹配"
        assert data.get("product_id") == self.test_product_id, "商品ID不匹配"
        assert data.get("quantity") == 2, "数量不匹配"
        
        self.logger.info("查询单个订单测试通过")

    @pytest.mark.parametrize("status, expected_result", order_status_data)
    def test_update_order_status(self, status, expected_result):
        self.logger.info(f"执行测试用例: 更新订单状态 - {status}")
        
        create_response = self.order_api.create_order(self.test_product_id, 1, "状态更新测试地址")
        assert create_response.status_code == 201, "创建订单失败"
        
        order_id = create_response.json().get("id")
        
        response = self.order_api.update_order_status(order_id, status)
        
        if expected_result == 400:
            assert response.status_code == 400, f"预期状态码400，实际{response.status_code}"
            self.logger.info("更新订单状态测试通过(异常场景)")
        else:
            assert response.status_code == 200, f"预期状态码200，实际{response.status_code}"
            
            data = response.json()
            assert data.get("success") == True, "更新失败"
            
            get_response = self.order_api.get_order_by_id(order_id)
            order_data = get_response.json()
            assert order_data.get("status") == status, "订单状态未更新"
            # DB层校验：验证数据库中订单状态已更新
            db_order = self.db.get_order(order_id)
            assert db_order, "DB层校验失败：订单不存在"
            assert db_order[0]["status"] == status, f"DB层校验：订单状态未更新，期望{status}"
            
            self.logger.info(f"更新订单状态测试通过(含DB校验)，当前状态: {status}")

    def test_cancel_order(self):
        self.logger.info("执行测试用例: 取消订单")
        
        create_response = self.order_api.create_order(self.test_product_id, 1, "取消订单测试地址")
        assert create_response.status_code == 201, "创建订单失败"
        
        order_id = create_response.json().get("id")
        
        cancel_response = self.order_api.cancel_order(order_id)
        assert cancel_response.status_code == 200, f"预期状态码200，实际{cancel_response.status_code}"
        
        data = cancel_response.json()
        assert data.get("success") == True, "取消失败"
        
        get_response = self.order_api.get_order_by_id(order_id)
        order_data = get_response.json()
        assert order_data.get("status") == "cancelled", "订单状态未更新为已取消"
        # DB层校验：验证数据库中订单状态已取消
        db_order = self.db.get_order(order_id)
        assert db_order, "DB层校验失败：订单不存在"
        assert db_order[0]["status"] == "cancelled", "DB层校验：订单状态未更新为已取消"
        
        self.logger.info("取消订单测试通过(含DB校验)")