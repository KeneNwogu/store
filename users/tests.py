from django.test import TestCase
from rest_framework.test import APIRequestFactory

from users.views import UserTransactionWebHook


class PaystackWebhookTest(TestCase):
    def setUp(self) -> None:
        self.factory = APIRequestFactory()
        self.view = UserTransactionWebHook.as_view()
        self.data = {
            'event': 'charge.success',
            'data': {
                'id': 1923036003,
                'domain': 'test',
                'status': 'success',
                'reference': '92fff1c304691a67fc5c3ed3a6fcf128',
                'amount': 4595984,
                'message': None,
                'gateway_response': 'Successful',
                'paid_at': '2022-07-02T01:03:28.000Z',
                'created_at': '2022-07-02T01:03:19.000Z',
                'channel': 'card',
                'currency': 'NGN',
                'ip_address': '165.154.234.52',
                'metadata': {
                    'referrer': 'http://localhost:8080/checkout'
                },
                'fees_breakdown': None,
                'log': None, 'fees': 78940,
                'fees_split': None,
                'authorization': {
                    'authorization_code': 'AUTH_s2nz8jlm07',
                    'bin': '408408',
                    'last4': '4081',
                    'exp_month': '12',
                    'exp_year': '2030',
                    'channel': 'card',
                    'card_type': 'visa ',
                    'bank': 'TEST BANK',
                    'country_code': 'NG',
                    'brand': 'visa',
                    'reusable': True,
                    'signature': 'SIG_axLXXJBa5PhYoD4ReSax',
                    'account_name': None,
                    'receiver_bank_account_number': None,
                    'receiver_bank': None
                },
                'customer': {
                    'id': 85440699,
                    'first_name': '',
                    'last_name': '',
                    'email': 'gbovo@test.com',
                    'customer_code': 'CUS_o7rvo0x5tsctr69',
                    'phone': '',
                    'metadata': None,
                    'risk_action': 'default',
                    'international_format_phone': None
                },
                'plan': {}, 'subaccount': {},
                'split': {}, 'order_id': None,
                'paidAt': '2022-07-02T01:03:28.000Z',
                'requested_amount': 4595984,
                'pos_transaction_data': None,
                'source': {
                    'type': 'web', 'source': 'checkout', 'entry_point': 'request_inline', 'identifier': None
                }
            }
        }

    def test_200_webhook_success_event(self):
        request = self.factory.post('/users/transactions-webhook/', data=self.data,
                                    format='json')
        response = self.view(request)
        self.assertEqual(response.status_code, 200)
