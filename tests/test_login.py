import pytest
from api.login_api import LoginAPI
from testdata.login_data import login_test_data, user_info_test_data
from utils.logger import Logger


class TestLogin:
    def setup_method(self):
        self.login_api = LoginAPI()
        self.logger = Logger()

    def teardown_method(self):
        pass

    @pytest.mark.parametrize("username, password, expected_code, expected_success, description", login_test_data)
    def test_login(self, username, password, expected_code, expected_success, description):
        self.logger.info(f"执行测试用例: {description}")
        response = self.login_api.login(username, password)
        
        assert response.status_code == expected_code, f"预期状态码{expected_code}，实际{response.status_code}"
        
        if expected_code == 200:
            data = response.json()
            assert "token" in data, "响应中缺少token字段"
            assert data.get("success") == expected_success, f"预期success={expected_success}"
            self.logger.info(f"测试通过: {description}")
        else:
            self.logger.info(f"测试通过(异常场景): {description}")

    @pytest.mark.parametrize("username, password, expected_code", user_info_test_data)
    def test_get_user_info(self, username, password, expected_code):
        self.logger.info("执行测试用例: 获取用户信息")
        
        login_response = self.login_api.login(username, password)
        assert login_response.status_code == 200, "登录失败"
        
        token = login_response.json().get("token")
        self.login_api.set_token(token)
        
        response = self.login_api.get_user_info()
        assert response.status_code == expected_code, f"预期状态码{expected_code}，实际{response.status_code}"
        
        if expected_code == 200:
            data = response.json()
            assert "username" in data, "响应中缺少username字段"
            assert "email" in data, "响应中缺少email字段"
            self.logger.info("获取用户信息测试通过")

    def test_logout(self):
        self.logger.info("执行测试用例: 退出登录")
        
        login_response = self.login_api.login("admin", "admin123")
        assert login_response.status_code == 200, "登录失败"
        
        token = login_response.json().get("token")
        self.login_api.set_token(token)
        
        response = self.login_api.logout()
        assert response.status_code == 200, f"预期状态码200，实际{response.status_code}"
        
        data = response.json()
        assert data.get("success") == True, "退出登录失败"
        self.logger.info("退出登录测试通过")