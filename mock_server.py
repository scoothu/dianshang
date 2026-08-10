"""
电商后台管理系统 Mock 服务
用于模拟电商后台API，供测试项目调用
"""
from flask import Flask, request, jsonify
import uuid
import re

app = Flask(__name__)

# 模拟数据存储
users = {
    "admin": {"password": "admin123", "email": "admin@test.com", "username": "admin"},
    "admin@test.com": {"password": "admin123", "email": "admin@test.com", "username": "admin"},
}
products = {}
orders = {}
next_product_id = 1
next_order_id = 1

VALID_STATUSES = ["pending", "paid", "shipped", "completed", "cancelled"]


# ==================== 登录模块 ====================

@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json(force=True, silent=True) or {}
    username = data.get("username", "")
    password = data.get("password", "")

    # 参数校验
    if not username or not password:
        return jsonify({"success": False, "message": "用户名或密码不能为空"}), 400
    if len(username) > 20:
        return jsonify({"success": False, "message": "用户名过长"}), 400
    if len(password) > 50:
        return jsonify({"success": False, "message": "密码过长"}), 400
    if len(password) < 6:
        return jsonify({"success": False, "message": "密码长度不足"}), 401

    # 用户不存在
    if username not in users:
        return jsonify({"success": False, "message": "用户不存在"}), 404

    # 密码错误
    if users[username]["password"] != password:
        return jsonify({"success": False, "message": "密码错误"}), 401

    # 登录成功
    token = str(uuid.uuid4())
    return jsonify({"token": token, "success": True, "message": "登录成功"}), 200


@app.route("/api/logout", methods=["POST"])
def logout():
    return jsonify({"success": True, "message": "退出成功"}), 200


@app.route("/api/user/info", methods=["GET"])
def get_user_info():
    return jsonify({"username": "admin", "email": "admin@test.com"}), 200


# ==================== 商品模块 ====================

@app.route("/api/products", methods=["GET"])
def get_product_list():
    page = int(request.args.get("page", 1))
    size = int(request.args.get("size", 10))
    category = request.args.get("category")
    keyword = request.args.get("keyword")

    result = list(products.values())
    if category:
        result = [p for p in result if p.get("category") == category]
    if keyword:
        result = [p for p in result if keyword in p.get("name", "")]

    total = len(result)
    start = (page - 1) * size
    end = start + size
    page_data = result[start:end]

    return jsonify({"list": page_data, "total": total, "page": page, "size": size}), 200


@app.route("/api/products/<int:product_id>", methods=["GET"])
def get_product(product_id):
    product = products.get(product_id)
    if not product:
        return jsonify({"success": False, "message": "商品不存在"}), 404
    return jsonify(product), 200


@app.route("/api/products", methods=["POST"])
def create_product():
    global next_product_id
    data = request.get_json(force=True, silent=True) or {}
    name = data.get("name", "")
    price = data.get("price")
    stock = data.get("stock")
    category = data.get("category", "")
    description = data.get("description", "")

    # 参数校验
    if not name:
        return jsonify({"success": False, "message": "商品名称不能为空"}), 400
    if len(name) > 100:
        return jsonify({"success": False, "message": "商品名称过长"}), 400
    if price is None or price < 0:
        return jsonify({"success": False, "message": "商品价格无效"}), 400
    if stock is None or stock < 0:
        return jsonify({"success": False, "message": "商品库存无效"}), 400
    if not category:
        return jsonify({"success": False, "message": "商品分类不能为空"}), 400

    product = {
        "id": next_product_id,
        "name": name,
        "price": price,
        "stock": stock,
        "category": category,
        "description": description,
    }
    products[next_product_id] = product
    next_product_id += 1

    return jsonify(product), 201


@app.route("/api/products/<int:product_id>", methods=["PUT"])
def update_product(product_id):
    product = products.get(product_id)
    if not product:
        return jsonify({"success": False, "message": "商品不存在"}), 404

    data = request.get_json(force=True, silent=True) or {}

    if "name" in data:
        if not data["name"]:
            return jsonify({"success": False, "message": "商品名称不能为空"}), 400
        if len(data["name"]) > 100:
            return jsonify({"success": False, "message": "商品名称过长"}), 400
        product["name"] = data["name"]
    if "price" in data and data["price"] is not None:
        if data["price"] < 0:
            return jsonify({"success": False, "message": "商品价格无效"}), 400
        product["price"] = data["price"]
    if "stock" in data and data["stock"] is not None:
        if data["stock"] < 0:
            return jsonify({"success": False, "message": "商品库存无效"}), 400
        product["stock"] = data["stock"]
    if "category" in data and data["category"] is not None:
        if not data["category"]:
            return jsonify({"success": False, "message": "商品分类不能为空"}), 400
        product["category"] = data["category"]
    if "description" in data and data["description"] is not None:
        product["description"] = data["description"]

    return jsonify({"success": True, "message": "更新成功"}), 200


@app.route("/api/products/<int:product_id>", methods=["DELETE"])
def delete_product(product_id):
    if product_id not in products:
        return jsonify({"success": False, "message": "商品不存在"}), 404
    del products[product_id]
    return jsonify({"success": True, "message": "删除成功"}), 200


# ==================== 订单模块 ====================

@app.route("/api/orders", methods=["GET"])
def get_order_list():
    page = int(request.args.get("page", 1))
    size = int(request.args.get("size", 10))
    status = request.args.get("status")
    user_id = request.args.get("user_id")

    result = list(orders.values())
    if status:
        result = [o for o in result if o.get("status") == status]

    total = len(result)
    start = (page - 1) * size
    end = start + size
    page_data = result[start:end]

    return jsonify({"list": page_data, "total": total, "page": page, "size": size}), 200


@app.route("/api/orders/<int:order_id>", methods=["GET"])
def get_order(order_id):
    order = orders.get(order_id)
    if not order:
        return jsonify({"success": False, "message": "订单不存在"}), 404
    return jsonify(order), 200


@app.route("/api/orders", methods=["POST"])
def create_order():
    global next_order_id
    data = request.get_json(force=True, silent=True) or {}
    product_id = data.get("product_id")
    quantity = data.get("quantity")
    address = data.get("address", "")

    # 参数校验
    if not product_id or product_id not in products:
        return jsonify({"success": False, "message": "商品不存在"}), 404
    if not quantity or quantity <= 0:
        return jsonify({"success": False, "message": "数量无效"}), 400
    if quantity > 9999:
        return jsonify({"success": False, "message": "数量超出限制"}), 400
    if not address:
        return jsonify({"success": False, "message": "地址不能为空"}), 400

    order = {
        "id": next_order_id,
        "product_id": product_id,
        "quantity": quantity,
        "address": address,
        "status": "pending",
    }
    orders[next_order_id] = order
    next_order_id += 1

    return jsonify(order), 201


@app.route("/api/orders/<int:order_id>/status", methods=["PUT"])
def update_order_status(order_id):
    order = orders.get(order_id)
    if not order:
        return jsonify({"success": False, "message": "订单不存在"}), 404

    data = request.get_json(force=True, silent=True) or {}
    status = data.get("status")

    if status not in VALID_STATUSES:
        return jsonify({"success": False, "message": "无效的订单状态"}), 400

    order["status"] = status
    return jsonify({"success": True, "message": "状态更新成功"}), 200


@app.route("/api/orders/<int:order_id>/cancel", methods=["PUT"])
def cancel_order(order_id):
    order = orders.get(order_id)
    if not order:
        return jsonify({"success": False, "message": "订单不存在"}), 404

    order["status"] = "cancelled"
    return jsonify({"success": True, "message": "取消成功"}), 200


if __name__ == "__main__":
    print("电商后台Mock服务启动中...")
    print("服务地址: http://127.0.0.1:8080")
    print("按 Ctrl+C 停止服务")
    app.run(host="127.0.0.1", port=8080, debug=False)
