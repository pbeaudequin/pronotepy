import unittest
from unittest.mock import Mock

import requests

from .generic_func import _educonnect


def _response(url: str, html: str) -> requests.Response:
    response = requests.Response()
    response.status_code = 200
    response.url = url
    response._content = html.encode()
    response.encoding = "utf-8"
    return response


class TestEduConnect(unittest.TestCase):
    def test_three_step_parent_login(self) -> None:
        e1s1 = _response(
            "https://educonnect.example/sso?execution=e1s1",
            """
            <form action="?execution=e1s1">
              <input type="hidden" name="csrf_token" value="csrf-1">
              <input type="hidden" name="shib_idp_ls_supported" value="">
            </form>
            """,
        )
        e1s2 = _response(
            "https://educonnect.example/sso?execution=e1s2",
            """
            <form action="?execution=e1s2">
              <input type="hidden" name="csrf_token" value="csrf-2">
              <input type="text" name="j_username">
              <input type="password" name="j_password">
            </form>
            """,
        )
        saml = _response(
            "https://educonnect.example/sso?execution=e1s2",
            """
            <form action="https://cas.example/saml">
              <input type="hidden" name="SAMLResponse" value="assertion">
              <input type="hidden" name="RelayState" value="relay">
            </form>
            """,
        )
        completed = _response("https://pronote.example/parent.html?ticket=ST-1", "ok")

        session = Mock(spec=requests.Session)
        session.post.side_effect = [e1s2, saml, completed]

        result = _educonnect(
            session,
            "parent-user",
            "secret",
            e1s1.url,
            type_user="responsable",
            initial_response=e1s1,
        )

        self.assertIs(result, completed)
        first_payload = session.post.call_args_list[0].kwargs["data"]
        self.assertNotIn("j_username", first_payload)
        self.assertEqual(first_payload["csrf_token"], "csrf-1")

        login_payload = session.post.call_args_list[1].kwargs["data"]
        self.assertEqual(login_payload["j_username"], "parent-user")
        self.assertEqual(login_payload["j_password"], "secret")
        self.assertEqual(login_payload["typeUser"], "responsable")
        self.assertIn("_eventId_proceed", login_payload)


if __name__ == "__main__":
    unittest.main()
