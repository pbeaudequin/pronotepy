import unittest

import requests

from .pronoteAPI import _Communication


class TestCommunicationCookies(unittest.TestCase):
    def test_ent_cookies_are_installed_on_persistent_session(self) -> None:
        cookies = requests.cookies.RequestsCookieJar()
        cookies.set("TGC", "ticket", domain="cas.example", path="/")

        communication = _Communication(
            "https://pronote.example/pronote/parent.html", cookies, False
        )

        self.assertEqual(communication.session.cookies.get("TGC"), "ticket")


if __name__ == "__main__":
    unittest.main()
