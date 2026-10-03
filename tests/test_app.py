"""Exercise the real Flask HTTP layer without downloading the correction model."""

import importlib.util
import json
import sys
import types
import unittest
from pathlib import Path
from unittest.mock import Mock, patch


class CorrectEndpointTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.model = Mock()
        module = types.ModuleType("pycorrector")
        module.MacBertCorrector = Mock(return_value=cls.model)
        spec = importlib.util.spec_from_file_location(
            "corrector_http_test", Path(__file__).parents[1] / "app.py"
        )
        app_module = importlib.util.module_from_spec(spec)
        with (
            patch.dict(sys.modules, {"pycorrector": module}),
            patch("logging.handlers.RotatingFileHandler") as handler,
        ):
            handler.return_value.level = 100
            spec.loader.exec_module(app_module)
        cls.app = app_module.app
        cls.app.config.update(TESTING=True)
        cls.client = cls.app.test_client()

    def setUp(self):
        self.model.reset_mock()

    def test_chinese_text_and_result_keep_existing_wire_shape(self):
        result = [{"source": "中文纠错", "target": "中文纠错", "errors": []}]
        self.model.correct_batch.return_value = result
        response = self.client.post("/correct", json={"text": "中文纠错"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, "application/json")
        self.assertEqual(response.get_json(), {"corrected_result": result})
        self.assertIn("中文纠错", response.get_data(as_text=True))
        self.model.correct_batch.assert_called_once_with(["中文纠错"])

    def test_missing_text_is_rejected_without_model_call(self):
        for payload in ({}, {"other": "中文"}, None):
            with self.subTest(payload=payload):
                response = self.client.post(
                    "/correct",
                    data=json.dumps(payload),
                    content_type="application/json",
                )
                self.assertEqual(response.status_code, 400)
                self.assertEqual(response.get_json(), {"error": "No text provided"})
        self.model.correct_batch.assert_not_called()

    def test_malformed_json_does_not_invoke_model(self):
        response = self.client.post(
            "/correct", data="{", content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)
        self.model.correct_batch.assert_not_called()

    def test_non_json_requests_keep_400_json_error(self):
        for content_type in (None, "text/plain", "application/x-www-form-urlencoded"):
            with self.subTest(content_type=content_type):
                response = self.client.post(
                    "/correct", data='{"text":"中文"}', content_type=content_type
                )
                self.assertEqual(response.status_code, 400)
                self.assertEqual(response.get_json(), {"error": "No text provided"})
        self.model.correct_batch.assert_not_called()

    def test_endpoint_remains_post_only(self):
        self.assertEqual(self.client.get("/correct").status_code, 405)
        self.model.correct_batch.assert_not_called()

    def test_json_provider_emits_literal_chinese(self):
        with self.app.app_context():
            self.assertIn("中文", self.app.json.dumps({"text": "中文"}))


if __name__ == "__main__":
    unittest.main()
