import pytest
from api.login_api import LoginAPI
from api.product_api import ProductAPI
from testdata.product_data import product_create_data, product_update_data, product_query_data
from utils.logger import Logger


class TestProduct:
    def setup_method(self):
        self.login_api = LoginAPI()
        self.product_api = ProductAPI()
        self.logger = Logger()
        self._login()

    def _login(self):
        login_response = self.login_api.login("admin", "admin123")
        if login_response.status_code == 200:
            token = login_response.json().get("token")
            self.product_api.set_token(token)

    def teardown_method(self):
        pass

    @pytest.mark.parametrize("name, price, stock, category, expected_code", product_create_data)
    def test_create_product(self, name, price, stock, category, expected_code):
        self.logger.info(f"执行测试用例: 创建商品 - {name}")
        response = self.product_api.create_product(name, price, stock, category)
        
        assert response.status_code == expected_code, f"预期状态码{expected_code}，实际{response.status_code}"
        
        if expected_code == 201:
            data = response.json()
            assert "id" in data, "响应中缺少id字段"
            assert data.get("name") == name, "商品名称不匹配"
            assert data.get("price") == price, "商品价格不匹配"
            assert data.get("stock") == stock, "商品库存不匹配"
            assert data.get("category") == category, "商品分类不匹配"
            self.logger.info(f"创建商品测试通过: {name}")
        else:
            self.logger.info(f"创建商品测试通过(异常场景): {name}")

    @pytest.mark.parametrize("page, size, category, keyword", product_query_data)
    def test_get_product_list(self, page, size, category, keyword):
        self.logger.info(f"执行测试用例: 查询商品列表 - page={page}, size={size}, category={category}, keyword={keyword}")
        response = self.product_api.get_product_list(page, size, category, keyword)
        
        assert response.status_code == 200, f"预期状态码200，实际{response.status_code}"
        
        data = response.json()
        assert "list" in data, "响应中缺少list字段"
        assert "total" in data, "响应中缺少total字段"
        assert "page" in data, "响应中缺少page字段"
        assert "size" in data, "响应中缺少size字段"
        
        self.logger.info(f"查询商品列表测试通过，共{data.get('total')}条记录")

    def test_get_product_by_id(self):
        self.logger.info("执行测试用例: 查询单个商品")
        
        create_response = self.product_api.create_product("查询测试商品", 59.99, 50, "测试分类")
        assert create_response.status_code == 201, "创建商品失败"
        
        product_id = create_response.json().get("id")
        
        response = self.product_api.get_product_by_id(product_id)
        assert response.status_code == 200, f"预期状态码200，实际{response.status_code}"
        
        data = response.json()
        assert data.get("id") == product_id, "商品ID不匹配"
        assert data.get("name") == "查询测试商品", "商品名称不匹配"
        assert data.get("price") == 59.99, "商品价格不匹配"
        
        self.logger.info("查询单个商品测试通过")

    @pytest.mark.parametrize("name, price, stock, category, expected_result", product_update_data)
    def test_update_product(self, name, price, stock, category, expected_result):
        self.logger.info(f"执行测试用例: 更新商品 - name={name}")
        
        create_response = self.product_api.create_product("更新测试商品", 39.99, 30, "原始分类")
        assert create_response.status_code == 201, "创建商品失败"
        
        product_id = create_response.json().get("id")
        
        response = self.product_api.update_product(product_id, name, price, stock, category)
        
        if expected_result == 400:
            assert response.status_code == 400, f"预期状态码400，实际{response.status_code}"
            self.logger.info("更新商品测试通过(异常场景)")
        else:
            assert response.status_code == 200, f"预期状态码200，实际{response.status_code}"
            
            data = response.json()
            assert data.get("success") == True, "更新失败"
            
            get_response = self.product_api.get_product_by_id(product_id)
            update_data = get_response.json()
            
            if name is not None:
                assert update_data.get("name") == name, "商品名称未更新"
            if price is not None:
                assert update_data.get("price") == price, "商品价格未更新"
            if stock is not None:
                assert update_data.get("stock") == stock, "商品库存未更新"
            if category is not None:
                assert update_data.get("category") == category, "商品分类未更新"
            
            self.logger.info("更新商品测试通过")

    def test_delete_product(self):
        self.logger.info("执行测试用例: 删除商品")
        
        create_response = self.product_api.create_product("删除测试商品", 29.99, 20, "删除分类")
        assert create_response.status_code == 201, "创建商品失败"
        
        product_id = create_response.json().get("id")
        
        delete_response = self.product_api.delete_product(product_id)
        assert delete_response.status_code == 200, f"预期状态码200，实际{delete_response.status_code}"
        
        data = delete_response.json()
        assert data.get("success") == True, "删除失败"
        
        get_response = self.product_api.get_product_by_id(product_id)
        assert get_response.status_code == 404, f"预期状态码404，实际{get_response.status_code}"
        
        self.logger.info("删除商品测试通过")