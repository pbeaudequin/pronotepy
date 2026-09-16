import unittest

from pronotepy.exceptions import PronoteAPIError
from .pronoteAPI import _Communication


class TestCommunicationParsing(unittest.TestCase):
    def test_ip_text_in_valid_bootstrap_page_is_not_a_suspension(self) -> None:
        communication = _Communication(
            "https://pronote.example/pronote/parent.html", None, False
        )
        html = "<script>Start({h:'123',a:'root'})</script><p>IP</p>"

        self.assertEqual(
            communication._parse_html(html),
            {"h": "123", "a": "root"},
        )

    def test_explicit_ip_suspension_message_is_reported(self) -> None:
        communication = _Communication(
            "https://pronote.example/pronote/parent.html", None, False
        )
        html = "<html><body>Your IP address is suspended.</body></html>"

        with self.assertRaisesRegex(PronoteAPIError, "IP address is suspended"):
            communication._parse_html(html)


if __name__ == "__main__":
    unittest.main()
