"""
Handler para OAuth Callback - POST /auth/callback
"""
import json
import logging
from typing import Dict, Any
import requests
from requests_oauthlib import OAuth2Session
from urllib.parse import urlparse, parse_qs
import boto3

from config import (
    STRAVA_CLIENT_ID,
    STRAVA_CLIENT_SECRET,
    STRAVA_TOKEN_URL,
    STRAVA_API_URL,
    DYNAMODB_TABLE_USERS,
    AWS_REGION
)
from utils import response_success, response_error, TokenManager

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.resource('dynamodb', region_name=AWS_REGION)
token_manager = TokenManager()


def lambda_handler(event, context):
    """
    Handler para OAuth Callback
    
    Expected event body:
    {
        "code": "authorization_code_from_strava",
        "scope": "read,activity:read_all"
    }
    """
    try:
        # Parsear body
        if isinstance(event.get('body'), str):
            body = json.loads(event['body'])
        else:
            body = event.get('body', {})
        
        code = body.get('code')
        if not code:
            return response_error('Authorization code is required', 400, 'MISSING_CODE')
        
        # Trocar code por access_token
        logger.info("Trocando authorization code por access token...")
        token_response = requests.post(
            STRAVA_TOKEN_URL,
            data={
                'client_id': STRAVA_CLIENT_ID,
                'client_secret': STRAVA_CLIENT_SECRET,
                'code': code,
                'grant_type': 'authorization_code'
            }
        )
        
        if token_response.status_code != 200:
            logger.error(f"Erro ao trocar code: {token_response.text}")
            return response_error('Failed to exchange authorization code', 400, 'AUTH_EXCHANGE_FAILED')
        
        tokens = token_response.json()
        athlete_data = tokens.get('athlete', {})
        user_id = str(athlete_data.get('id'))
        
        # Armazenar dados do usuário e tokens
        logger.info(f"Armazenando dados do usuário: {user_id}")
        users_table = dynamodb.Table(DYNAMODB_TABLE_USERS)
        
        users_table.put_item(
            Item={
                'user_id': user_id,
                'athlete_name': athlete_data.get('firstname', '') + ' ' + athlete_data.get('lastname', ''),
                'athlete_email': athlete_data.get('email', ''),
                'athlete_profile': athlete_data.get('profile', ''),
                'tokens': {
                    'access_token': tokens.get('access_token'),
                    'refresh_token': tokens.get('refresh_token'),
                    'expires_at': tokens.get('expires_at'),
                    'token_type': tokens.get('token_type', 'Bearer')
                },
                'created_at': __import__('datetime').datetime.now().isoformat(),
                'updated_at': __import__('datetime').datetime.now().isoformat()
            }
        )
        
        logger.info(f"Usuário {user_id} autenticado com sucesso")
        
        return response_success({
            'user_id': user_id,
            'athlete_name': athlete_data.get('firstname', '') + ' ' + athlete_data.get('lastname', ''),
            'access_token': tokens.get('access_token'),
            'expires_in': tokens.get('expires_in'),
            'message': 'Authentication successful'
        }, 200)
        
    except Exception as e:
        logger.error(f"Erro no auth callback: {str(e)}")
        return response_error(f'Internal server error: {str(e)}', 500, 'INTERNAL_ERROR')


def refresh_access_token(user_id: str) -> Dict[str, Any]:
    """Renova access token usando refresh token"""
    try:
        tokens = token_manager.get_token(user_id)
        if not tokens or 'refresh_token' not in tokens:
            raise Exception("Refresh token not found")
        
        logger.info(f"Renovando access token para usuário: {user_id}")
        
        refresh_response = requests.post(
            STRAVA_TOKEN_URL,
            data={
                'client_id': STRAVA_CLIENT_ID,
                'client_secret': STRAVA_CLIENT_SECRET,
                'refresh_token': tokens['refresh_token'],
                'grant_type': 'refresh_token'
            }
        )
        
        if refresh_response.status_code != 200:
            raise Exception(f"Failed to refresh token: {refresh_response.text}")
        
        new_tokens = refresh_response.json()
        token_manager.save_token(user_id, new_tokens)
        
        logger.info(f"Token renovado com sucesso para: {user_id}")
        return new_tokens
        
    except Exception as e:
        logger.error(f"Erro ao renovar token: {str(e)}")
        raise
