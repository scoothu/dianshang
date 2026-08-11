"""
电商后台管理系统 Mock 服务
用于模拟电商后台API，供测试项目调用 + Web管理界面调用
"""
from flask import Flask, request, jsonify, send_from_directory
import uuid
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WEB_DIR = os.path.join(BASE_DIR, "web")

app = Flask(__name__, static_folder=WEB_DIR, static_url_path="/web")

# ==================== 模拟数据存储 ====================
users = {
    "admin": {"password": "admin123", "email": "admin@test.com", "username": "admin", "role": "admin"},
    "admin@test.com": {"password": "admin123", "email": "admin@test.com", "username": "admin", "role": "admin"},
}
products = {}
orders = {}
sessions = {}  # token -> username
next_product_id = 1
next_order_id = 1

VALID_STATUSES = ["pending", "paid", "shipped", "completed", "cancelled"]
STATUS_CN = {
    "pending": "待付款",
    "paid": "已付款",
    "shipped": "已发货",
    "completed": "已完成",
    "cancelled": "已取消",
}


def init_sample_data():
    """初始化示例数据"""
    global next_product_id, next_order_id
    samples = [
        ("iPhone 15 Pro", 7999.00, 120, "数码电子", "A17 Pro芯片，钛金属机身"),
        ("MacBook Air M3", 8999.00, 56, "数码电子", "13英寸 M3芯片，轻薄本"),
        ("华为Mate 60", 5999.00, 200, "数码电子", "麒麟芯片，卫星通话"),
        ("小米14 Ultra", 6499.00, 150, "数码电子", "徕卡全焦段四摄"),
        ("Apple Watch S9", 2999.00, 88, "智能穿戴", "S9芯片，双指互点功能"),
        ("AirPods Pro 2", 1899.00, 300, "智能穿戴", "主动降噪，空间音频"),
    ]
    products.clear()
    orders.clear()
    next_product_id = 1
    next_order_id = 1
    for name, price, stock, category, description in samples:
        products[next_product_id] = {
            "id": next_product_id, "name": name, "price": price,
            "stock": stock, "category": category, "description": description,
        }
        next_product_id += 1
    # 示例订单
    demo_orders = [
        (1, 2, "湖南省长沙市岳麓区湖南大学南校区"),
        (2, 1, "广东省深圳市南山区科技园"),
        (4, 1, "湖南省长沙市天心区芙蓉中路"),
    ]
    for idx, (pid, qty, addr) in enumerate(demo_orders):
        orders[next_order_id] = {
            "id": next_order_id, "product_id": pid, "quantity": qty,
            "address": addr, "status": VALID_STATUSES[idx],
        }
        next_order_id += 1
    print(f"[Mock] 初始化 {len(products)} 个商品、{len(orders)} 个订单")


init_sample_data()


def _get_current_user():
    """从请求头获取当前登录用户"""
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    if token and token in sessions:
        username = sessions[token]
        if username in users:
            return username, users[username]
    return None, None


# ==================== 静态页面路由 ====================
@app.route("/")
def index_page():
    return send_from_directory(WEB_DIR, "index.html")


@app.route("/login")
def login_page():
    return send_from_directory(WEB_DIR, "login.html")


@app.route("/web/<path:filename>")
def static_file(filename):
    return send_from_directory(WEB_DIR, filename)


# ==================== 注册 / 登录模块 ====================
@app.route("/api/register", methods=["POST"])
def register():
    """自定义注册账号密码"""
    data = request.get_json(force=True, silent=True) or {}
    username = (data.get("username") or "").strip()
    password = data.get("password") or ""
    email = (data.get("email") or "").strip()

    if not username or len(username) > 20:
        return jsonify({"success": False, "message": "用户名不能为空或过长"}), 400
    if len(password) < 6 or len(password) > 50:
        return jsonify({"success": False, "message": "密码长度6-50位"}), 400
    if username in users:
        return jsonify({"success": False, "message": "用户名已存在"}), 400

    info = {"password": password, "email": email or f"{username}@test.com",
            "username": username, "role": "user"}
    users[username] = info
    if info["email"] and info["email"] not in users:
        users[info["email"]] = info
    return jsonify({"success": True, "message": "注册成功"}), 201


@app.route("/api/change-password", methods=["POST"])
def change_password():
    """修改密码"""
    current_user, _ = _get_current_user()
    if not current_user:
        return jsonify({"success": False, "message": "未登录"}), 401
    data = request.get_json(force=True, silent=True) or {}
    old = data.get("old_password") or ""
    new = data.get("new_password") or ""
    user_info = users.get(current_user)
    if not user_info or user_info["password"] != old:
        return jsonify({"success": False, "message": "原密码错误"}), 400
    if len(new) < 6 or len(new) > 50:
        return jsonify({"success": False, "message": "新密码长度6-50位"}), 400
    email = user_info.get("email", "")
    user_info["password"] = new
    if email and email in users:
        users[email]["password"] = new
    return jsonify({"success": True, "message": "密码修改成功"}), 200


@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json(force=True, silent=True) or {}
    username = (data.get("username") or "").strip()
    password = data.get("password", "")

    if not username or not password:
        return jsonify({"success": False, "message": "用户名或密码不能为空"}), 400
    if len(username) > 20:
        return jsonify({"success": False, "message": "用户名过长"}), 400
    if len(password) > 50:
        return jsonify({"success": False, "message": "密码过长"}), 400
    if len(password) < 6:
        return jsonify({"success": False, "message": "密码长度不足"}), 401
    if username not in users:
        return jsonify({"success": False, "message": "用户不存在"}), 404
    if users[username]["password"] != password:
        return jsonify({"success": False, "message": "密码错误"}), 401

    token = str(uuid.uuid4())
    sessions[token] = users[username]["username"]
    return jsonify({"token": token, "success": True, "message": "登录成功",
                    "username": users[username]["username"]}), 200


@app.route("/api/logout", methods=["POST"])
def logout():
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    if token and token in sessions:
        del sessions[token]
    return jsonify({"success": True, "message": "退出成功"}), 200


@app.route("/api/user/info", methods=["GET"])
def get_user_info():
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    if token and token in sessions:
        name = sessions[token]
        u = users.get(name, {})
        return jsonify({"username": name, "email": u.get("email", ""),
                        "role": u.get("role", "user")}), 200
    return jsonify({"success": False, "message": "未登录"}), 401


@app.route("/api/user/list", methods=["GET"])
def user_list():
    """用户列表（去重）"""
    seen = {}
    for info in users.values():
        name = info["username"]
        seen.setdefault(name, info)
    result = [{"username": v["username"], "email": v["email"], "role": v["role"]}
              for v in seen.values()]
    return jsonify({"list": result, "total": len(result)}), 200


# ==================== 商品模块 ====================
@app.route("/api/products", methods=["GET"])
def get_product_list():
    page = int(request.args.get("page", 1))
    size = int(request.args.get("size", 20))
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
    return jsonify({"list": result[start:end], "total": total, "page": page, "size": size}), 200


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

    product = {"id": next_product_id, "name": name, "price": price, "stock": stock,
               "category": category, "description": description}
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
    size = int(request.args.get("size", 20))
    status = request.args.get("status")

    result = list(orders.values())
    if status:
        result = [o for o in result if o.get("status") == status]

    # 附带商品名称
    for o in result:
        p = products.get(o.get("product_id"), {})
        o["product_name"] = p.get("name", "-")
        o["product_price"] = p.get("price", 0)
        o["total_amount"] = o["product_price"] * o.get("quantity", 0)
        o["status_cn"] = STATUS_CN.get(o.get("status"), o.get("status"))

    total = len(result)
    start = (page - 1) * size
    end = start + size
    return jsonify({"list": result[start:end], "total": total, "page": page, "size": size}), 200


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

    if not product_id or product_id not in products:
        return jsonify({"success": False, "message": "商品不存在"}), 404
    if not quantity or quantity <= 0:
        return jsonify({"success": False, "message": "数量无效"}), 400
    if quantity > 9999:
        return jsonify({"success": False, "message": "数量超出限制"}), 400
    if not address:
        return jsonify({"success": False, "message": "地址不能为空"}), 400

    order = {"id": next_order_id, "product_id": product_id, "quantity": quantity,
             "address": address, "status": "pending"}
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


# ==================== 统计数据 ====================
@app.route("/api/dashboard", methods=["GET"])
def dashboard():
    total_p = len(products)
    total_o = len(orders)
    total_sales = 0
    status_count = {s: 0 for s in VALID_STATUSES}
    for o in orders.values():
        status_count[o["status"]] = status_count.get(o["status"], 0) + 1
        p = products.get(o["product_id"], {})
        total_sales += p.get("price", 0) * o.get("quantity", 0)
    total_u = len({v["username"] for v in users.values()})
    return jsonify({
        "total_users": total_u,
        "total_products": total_p,
        "total_orders": total_o,
        "total_sales": round(total_sales, 2),
        "status_count": status_count,
    }), 200


# ==================== 重置数据 ====================
@app.route("/api/reset", methods=["POST"])
def reset():
    init_sample_data()
    return jsonify({"success": True, "message": "数据已重置为初始示例"}), 200


if __name__ == "__main__":
    print("电商后台管理系统启动中...")
    print(f"管理后台页面: http://127.0.0.1:8080/")
    print(f"登录页面:     http://127.0.0.1:8080/login")
    print(f"API文档地址:  http://127.0.0.1:8080/")
    print(f"默认账号:     admin / admin123   (可自定义注册新账号)")
    print("按 Ctrl+C 停止服务")
    app.run(host="127.0.0.1", port=8080, debug=False)
