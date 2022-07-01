import datetime

import jwt
from django.test import TestCase

from rest_framework.test import APIRequestFactory, force_authenticate
from orders.views import CreateOrderView

from products.models import Product
from users.models import User


class OrderTestCase(TestCase):
    def setUp(self) -> None:
        User.objects.create(first_name='Kene', last_name='Nwogu')
        Product.objects.create(name='Drift', brand='Micha', price=9000)
        self.factory = APIRequestFactory()
        self.user = User.objects.all().first()
        self.view = CreateOrderView.as_view()
        self.json = {
            "orders": [
                {
                    "product_id": str(Product.objects.all().first()._id),
                    "quantity": 1
                }
            ],
            "state": "Abuja",
            "address": "Lone Lane, Unilag."
        }

    @property
    def payload_auth_header(self):
        payload = {
            "user_id": str(self.user._id),
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30),
            "iat": datetime.datetime.utcnow()
        }
        SECRET_KEY = 'django-insecure-#l-*ga8-37s(!vo4+vp&(xc%8pqaigdo+l%(%-!1p@v62ii+o5'
        token = jwt.encode(payload, SECRET_KEY, "HS256")
        return {
            'Authorization': token
        }

    def test_200_ok_ordering_products(self):
        request = self.factory.post('/orders/', headers=self.payload_auth_header, data=self.json, format='json')
        force_authenticate(request, user=self.user)
        response = self.view(request)
        print(response.data)
        self.assertEqual(response.status_code, 200)


# if __name__ == "__main__":
#     unittest.main()