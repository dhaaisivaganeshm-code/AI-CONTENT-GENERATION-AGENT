import asyncio
import unittest
from types import SimpleNamespace
from unittest.mock import patch

from app.services import gemini_service


class AIServiceTests(unittest.TestCase):
    def test_openai_like_provider_returns_text(self):
        class FakeResponse:
            status_code = 200

            def json(self):
                return {
                    "choices": [
                        {"message": {"content": "Hello from the AI provider"}}
                    ]
                }

        fake_settings = SimpleNamespace(
            ai_provider="openai",
            ai_api_key="test-key",
            ai_model="gpt-4o-mini",
            ai_base_url=None,
            gemini_api_key=None,
        )

        with patch.object(gemini_service, "settings", fake_settings), patch("app.services.gemini_service.httpx.post", return_value=FakeResponse()) as mocked_post:
            result = asyncio.run(gemini_service.generate_reply([], "Hello"))

        self.assertEqual(result, "Hello from the AI provider")
        mocked_post.assert_called_once()


if __name__ == "__main__":
    unittest.main()
