import threading
import time
import unittest
import requests
from http.server import HTTPServer
from servidor import *

IP = "127.0.0.1"
PORT = 21080

class TestRequests(unittest.TestCase):

    def setUp(self):
        self.server = HTTPServer((IP, PORT), RequestHandler)
        self.server_thread = threading.Thread(target=self.server.serve_forever)
        self.server_thread.start()
        time.sleep(0.5) 

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()
        self.server_thread.join()

    def test_request_raiz(self):
        response = requests.get(f"http://{IP}:{PORT}/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("<html", response.text.lower()) 

    def test_request_autor(self):
        response = requests.get(f"http://{IP}:{PORT}/author")
        self.assertIn("José María Condo Tuanama", response.text) 

    def test_request_no_existe(self):
        response = requests.get(f"http://{IP}:{PORT}/noexiste")
        self.assertEqual(response.status_code, 400)
        self.assertIn("PAGE NOT FOUND", response.text)

    def test_query_parameters_limite(self):
        url = f"http://{IP}:{PORT}/results?target=&disease=EFO_0000616&score=0.5"
        response = requests.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Target ID", response.text)

    def test_filtrado_y_caso_vacio(self):
        url = f"http://{IP}:{PORT}/searchTarget?id=ENSG0000SQXSD"
        response = requests.get(url)
        self.assertEqual(response.status_code, 404)
        self.assertIn("The query don't have the correct formatted data", response.text)


if __name__ == "__main__":
    unittest.main()
