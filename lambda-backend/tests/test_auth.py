"""
Exemplo de teste para auth_handler.py
"""
import json
import pytest
from unittest.mock import patch, MagicMock
import sys

# Mock das variáveis de ambiente antes de importar os handlers
import os
os.environ['STRAVA_CLIENT_ID'] = 'test_client_id'
os.environ['STRAVA_CLIENT_SECRET'] = 'test_client_secret'
os.environ['DYNAMODB_TABLE_USERS'] = 'strava-users'
os.environ['AWS_REGION'] = 'us-east-1'


def test_auth_callback_success():
    """Testa OAuth callback com sucesso"""
    from src import auth_handler
    
    event = {
        'body': json.dumps({
            'code': 'test_auth_code',
            'scope': 'read,activity:read_all'
        })
    }
    
    context = MagicMock()
    
    # Mock do requests.post
    with patch('src.auth_handler.requests.post') as mock_post:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'access_token': 'test_token',
            'refresh_token': 'test_refresh',
            'expires_at': 1234567890,
            'token_type': 'Bearer',
            'athlete': {
                'id': 123456,
                'firstname': 'João',
                'lastname': 'Silva',
                'email': 'joao@example.com',
                'profile': 'https://example.com/profile.jpg'
            }
        }
        mock_post.return_value = mock_response
        
        # Mock do DynamoDB
        with patch('src.auth_handler.dynamodb.Table') as mock_table:
            mock_table.return_value.put_item = MagicMock()
            
            response = auth_handler.lambda_handler(event, context)
    
    assert response['statusCode'] == 200
    body = json.loads(response['body'])
    assert body['success'] is True
    assert body['data']['user_id'] == '123456'


def test_auth_callback_missing_code():
    """Testa OAuth callback sem código"""
    from src import auth_handler
    
    event = {
        'body': json.dumps({
            'scope': 'read,activity:read_all'
        })
    }
    
    context = MagicMock()
    response = auth_handler.lambda_handler(event, context)
    
    assert response['statusCode'] == 400
    body = json.loads(response['body'])
    assert body['success'] is False
    assert body['error']['code'] == 'MISSING_CODE'


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
