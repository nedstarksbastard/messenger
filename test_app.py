import unittest
import app
import tempfile
import os
from helpers import init_db


class OrderServiceTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = app.app.test_client()
        db_fd, cls.app.application.config['DATABASE'] = tempfile.mkstemp()
        cls.app.application.config['TESTING'] = True
        os.close(db_fd)
        os.unlink(cls.app.application.config['DATABASE'])

    def test_home_status_code(self):

        # assert the status code of the response. Add mock session and initialize temp db
        with self.app as c:
            with c.session_transaction() as sess:
                sess['logged_in'] = True
                sess['username'] = "Test User"
        with self.app.application.app_context():
            init_db()
        result = self.app.get('/')
        self.assertEqual(result.status_code, 200)

    @classmethod
    def tearDownClass(cls):
        if os.path.exists(cls.app.application.config['DATABASE']):
            os.remove(cls.app.application.config['DATABASE'])


if __name__ == "__main__":
    unittest.main()