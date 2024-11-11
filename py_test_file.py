import pytest
from unittest.mock import patch, MagicMock, mock_open
from mail_server import send_email

def test_send_email_with_attachment():
    # Test sending an email with an existing attachment
    with patch("smtplib.SMTP") as mock_smtp, \
         patch("builtins.open", mock_open(read_data=b"file content")) as mock_file, \
         patch("os.path.isfile", return_value=True) as mock_isfile:
        
        mock_server = MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_server

        # Call the function with a mocked file path
        send_email(
            to="recipient@example.com",
            subject="Test Email with Attachment",
            body="This email has an attachment.",
            attachments=["existing_file.txt"]
        )

        # Assert that the file was opened for reading
        mock_file.assert_called_once_with("existing_file.txt", "rb")
        
        # Check that send_message was called on the server
        mock_server.send_message.assert_called_once()

def test_send_email_attachment_not_found():
    # Test sending an email with a non-existent attachment, expecting FileNotFoundError
    with patch("os.path.isfile", return_value=False):
        with pytest.raises(FileNotFoundError, match="Attachment .* not found"):
            send_email(
                to="recipient@example.com",
                subject="Test Email with Missing Attachment",
                body="This email should raise a FileNotFoundError.",
                attachments=["non_existent_file.txt"]
            )
