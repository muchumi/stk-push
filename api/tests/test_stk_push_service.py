from unittest.mock import patch

from api.services.stk_push import initiate_stk_push


@patch("api.services.stk_push.generate_password")
@patch("api.services.stk_push.generate_timestamp")
@patch("api.services.stk_push.get_access_token")
def test_initiate_stk_push(
    mock_get_access_token,
    mock_generate_timestamp,
    mock_generate_password
):
    # Arrange
    mock_get_access_token.return_value = "test_access_token"
    mock_generate_timestamp.return_value = "20260928190600"
    mock_generate_password.return_value = "test_password"

    # Act
    result = initiate_stk_push(
        phoneNumber="+254719273876",
        amount=100
    )

    # Assert
    mock_get_access_token.assert_called_once()
    mock_generate_timestamp.assert_called_once()
    mock_generate_password.assert_called_once_with(
        "20260928190600"
    )

    assert result is None