from .test_setup import TestSetUp


class Testapis(TestSetUp):
    ""
    def test_signup_badrequest(self):
        "error signup test case"
        response = self.client.post(self.signUpUrl)
        # import pdb  # to pause and debug
        # pdb.set_trace()
        # this will fail cause of no enough data provided
        self.assertEqual(response.status_code, 400)  # 400==badrequest.

    def test_signup_ok(self):
        "success signup test case"
        response = self.client.post(
            self.signUpUrl, self.userData, format="json")
        # import pdb  # to pause and debug
        # pdb.set_trace()
        self.assertEqual(response.status_code, 200)  # 200==ok.
