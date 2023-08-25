from unittest import TestCase
from Bingo.models import Users
from unittest.mock import patch, Mock
from Bingo.utils.login_token import LoginToken


class TestLoginToken(TestCase):

    def setUp(self):
        self.request = Mock()
        self.user = Users(id=1, username="testuser")
        self.request.session = {
            'login_token': {
                'user_id': 1,
                'user_role': 'Admin'
            }
        }
        self.request.user.username = "testuser"

    @patch('Bingo.utils.login_token.DAL')
    def test_validate_login_token_valid(self, MockDAL):
        mock_dal_instance = MockDAL.return_value
        mock_dal_instance.get_by_id.return_value = self.user
        
        token = LoginToken.validate_login_token(self.request)
        
        self.assertEqual(token.user_id, 1)
        self.assertEqual(token.user_role, 'Admin')
        self.assertEqual(self.request.user, self.user)

    @patch('Bingo.utils.login_token.DAL')
    def test_validate_login_token_missing_token(self, MockDAL):
        self.request.session = {}
        
        with self.assertRaises(PermissionError) as context:
            LoginToken.validate_login_token(self.request)
            
        self.assertIn("An error occurred while validating the login token", str(context.exception))

    
    @patch('Bingo.utils.login_token.DAL')
    def test_validate_login_token_invalid_token(self, MockDAL):
        self.request.session['login_token']['user_id'] = None
        
        with self.assertRaises(PermissionError) as context:
            LoginToken.validate_login_token(self.request)
            
        self.assertIn("An error occurred while validating the login token", str(context.exception))


    @patch('Bingo.utils.login_token.DAL')
    def test_validate_login_token_user_not_found(self, MockDAL):
        mock_dal_instance = MockDAL.return_value
        mock_dal_instance.get_by_id.return_value = None

        with self.assertRaises(PermissionError) as context:
            LoginToken.validate_login_token(self.request)
            
        self.assertIn("An error occurred while validating the login token", str(context.exception))

    @patch('Bingo.utils.login_token.DAL')
    def test_validate_login_token_exception(self, MockDAL):
        mock_dal_instance = MockDAL.return_value
        mock_dal_instance.get_by_id.side_effect = Exception("DB error")

        with self.assertRaises(PermissionError) as context:
            LoginToken.validate_login_token(self.request)
            
        self.assertIn("An error occurred while validating the login token", str(context.exception))
