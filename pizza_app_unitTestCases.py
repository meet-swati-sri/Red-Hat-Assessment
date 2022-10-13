import unittest
import requests
import json


class MyTestCase(unittest.TestCase):
    path = "http://127.0.0.1:5000"

    def testWelcome(self):
        temp = requests.get(self.path + "/welcome")
        self.assertEqual(temp.json(), "Welcome to Pizza House")

    '''
    def testAcceptOrder(self):
        temp = requests.get(self.path + "/order")
        self.assertEqual(temp.status_code, 405)
    '''

    def testAcceptOrder(self):
        temp = self.path + "/order"
        orders = {
            "orders": ["PIZZZZZAAAAAA"]
        }
        resp = requests.post(temp, data=json.dumps(orders), headers={"Content-Type": "application/json"})
        self.assertEqual(resp.json(), "Order Placed!")


    def testFetchAllOrders(self):
        temp = requests.get(self.path + "/getorders")
        self.assertEqual(temp.status_code, 200)
        json_response = temp.json()
        self.assertEqual(json_response[0]['_id']['$oid'], '634717a6a9e9a0a7bb6afaf0')
        self.assertEqual(json_response[0]['orders'][0], 'pizza')

    def testFetchOrder(self):
        temp = requests.get(self.path + "/getorders")
        self.assertEqual(temp.status_code, 200)
        json_response = temp.json()
        self.assertEqual(json_response[0]['_id']['$oid'], '634717a6a9e9a0a7bb6afaf0')
        self.assertEqual(json_response[0]['orders'][0], 'pizza')

if __name__ == '__main__':
    unittest.main()
