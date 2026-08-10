import pytest


login_test_data = [
    ("admin", "admin123", 200, True, "正常登录"),
    ("admin", "", 400, False, "密码为空"),
    ("", "admin123", 400, False, "用户名为空"),
    ("admin", "wrongpwd", 401, False, "密码错误"),
    ("nonexistent", "admin123", 404, False, "用户不存在"),
    ("admin@test.com", "admin123", 200, True, "邮箱格式用户名登录"),
    ("admin", "admin", 401, False, "密码长度不足"),
    ("a" * 50, "admin123", 400, False, "用户名超长"),
    ("admin", "a" * 100, 400, False, "密码超长"),
    ("admin", "ADMIN123", 401, False, "密码大小写错误"),
]

user_info_test_data = [
    ("admin", "admin123", 200),
]


@pytest.fixture(params=login_test_data)
def login_data(request):
    return request.param


@pytest.fixture(params=user_info_test_data)
def user_info_data(request):
    return request.param