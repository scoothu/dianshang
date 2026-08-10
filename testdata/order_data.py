import pytest


order_create_data = [
    (1, 1, "北京市朝阳区xxx街道xxx号", 201),
    (1, 10, "上海市浦东新区xxx路xxx号", 201),
    (1, 0, "广州市天河区xxx街xxx号", 400),
    (99999, 1, "深圳市南山区xxx路xxx号", 404),
    (1, 1, "", 400),
    (1, 99999, "杭州市西湖区xxx路xxx号", 400),
]

order_status_data = [
    ("paid", "支付成功"),
    ("shipped", "发货成功"),
    ("completed", "完成成功"),
    ("cancelled", "取消成功"),
    ("invalid_status", 400),
]

order_query_data = [
    (1, 10, None, None),
    (1, 10, "pending", None),
    (1, 10, "paid", None),
    (2, 5, None, None),
]


@pytest.fixture(params=order_create_data)
def order_create_fixture(request):
    return request.param


@pytest.fixture(params=order_status_data)
def order_status_fixture(request):
    return request.param


@pytest.fixture(params=order_query_data)
def order_query_fixture(request):
    return request.param