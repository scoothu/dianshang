from api.base_api import BaseAPI


class ProductAPI(BaseAPI):
    def __init__(self):
        super().__init__()

    def get_product_list(self, page=1, size=10, category=None, keyword=None):
        url = "/api/products"
        params = {
            "page": page,
            "size": size
        }
        if category:
            params["category"] = category
        if keyword:
            params["keyword"] = keyword
        return self.get(url, params=params)

    def get_product_by_id(self, product_id):
        url = f"/api/products/{product_id}"
        return self.get(url)

    def create_product(self, name, price, stock, category, description=""):
        url = "/api/products"
        data = {
            "name": name,
            "price": price,
            "stock": stock,
            "category": category,
            "description": description
        }
        return self.post(url, json=data)

    def update_product(self, product_id, name=None, price=None, stock=None, category=None, description=None):
        url = f"/api/products/{product_id}"
        data = {}
        if name is not None:
            data["name"] = name
        if price is not None:
            data["price"] = price
        if stock is not None:
            data["stock"] = stock
        if category is not None:
            data["category"] = category
        if description is not None:
            data["description"] = description
        return self.put(url, json=data)

    def delete_product(self, product_id):
        url = f"/api/products/{product_id}"
        return self.delete(url)