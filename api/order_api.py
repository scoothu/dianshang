from api.base_api import BaseAPI


class OrderAPI(BaseAPI):
    def __init__(self):
        super().__init__()

    def get_order_list(self, page=1, size=10, status=None, user_id=None):
        url = "/api/orders"
        params = {
            "page": page,
            "size": size
        }
        if status:
            params["status"] = status
        if user_id:
            params["user_id"] = user_id
        return self.get(url, params=params)

    def get_order_by_id(self, order_id):
        url = f"/api/orders/{order_id}"
        return self.get(url)

    def create_order(self, product_id, quantity, address):
        url = "/api/orders"
        data = {
            "product_id": product_id,
            "quantity": quantity,
            "address": address
        }
        return self.post(url, json=data)

    def update_order_status(self, order_id, status):
        url = f"/api/orders/{order_id}/status"
        data = {
            "status": status
        }
        return self.put(url, json=data)

    def cancel_order(self, order_id):
        url = f"/api/orders/{order_id}/cancel"
        return self.put(url)