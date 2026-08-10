import pytest


product_create_data = [
    ("测试商品1", 99.99, 100, "电子产品", 201),
    ("测试商品2", 0.01, 1, "日用品", 201),
    ("测试商品3", 99999.99, 9999, "服装", 201),
    ("", 99.99, 100, "电子产品", 400),
    ("测试商品", -1, 100, "电子产品", 400),
    ("测试商品", 99.99, -1, "电子产品", 400),
    ("测试商品", 99.99, 100, "", 400),
    ("a" * 200, 99.99, 100, "电子产品", 400),
]

product_update_data = [
    ("更新商品名称", 199.99, 200, "数码产品", "更新成功"),
    ("", None, None, None, 400),
    (None, -1, None, None, 400),
    (None, None, -1, None, 400),
]

product_query_data = [
    (1, 10, None, None),
    (1, 10, "电子产品", None),
    (1, 10, None, "测试"),
    (2, 5, "服装", None),
]


@pytest.fixture(params=product_create_data)
def product_create_fixture(request):
    return request.param


@pytest.fixture(params=product_update_data)
def product_update_fixture(request):
    return request.param


@pytest.fixture(params=product_query_data)
def product_query_fixture(request):
    return request.param