import unittest
from unittest.mock import patch, Mock

from greptile_api import GreptileAPI


class TestGreptileAPI(unittest.TestCase):
    def test_repo_id_encoding(self):
        api = GreptileAPI(api_key="dummy", base_url="https://example.com")
        rid = api._repo_id("github", "main", "owner/repo")
        # should fully encode reserved characters
        self.assertEqual(rid, "github%3Amain%3Aowner%2Frepo")

    @patch("greptile_api.requests.get")
    def test_check_repo_status_uses_resolved_branch(self, mock_get):
        api = GreptileAPI(api_key="dummy", base_url="https://example.com")
        api.get_default_branch = lambda repo: "develop"

        mock_resp = Mock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {
            "status": "PROCESSED",
            "chunksProcessed": 1,
            "totalChunks": 2,
        }
        mock_get.return_value = mock_resp

        out = api.check_repo_status("owner/repo", branch=None)
        self.assertTrue(out["success"])

        called_url = mock_get.call_args[0][0]
        self.assertIn("github%3Adevelop%3Aowner%2Frepo", called_url)

    @patch("greptile_api.requests.post")
    def test_enable_repo_accepts_201(self, mock_post):
        api = GreptileAPI(api_key="dummy", base_url="https://example.com")
        api.get_default_branch = lambda repo: "main"

        mock_resp = Mock()
        mock_resp.status_code = 201
        mock_resp.json.return_value = {"message": "ok", "repoData": {"status": "PROCESSING"}}
        mock_post.return_value = mock_resp

        out = api.enable_repo("owner/repo")
        self.assertTrue(out["success"])


if __name__ == "__main__":
    unittest.main()
