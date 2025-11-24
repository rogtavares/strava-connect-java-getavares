"""
Utilitários para Backend APIs
"""
import json
import logging
import hashlib
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
import boto3
from config import (
    DYNAMODB_TABLE_CACHE,
    DYNAMODB_TABLE_USERS,
    AWS_REGION,
    CACHE_TTL_ATHLETE,
    CACHE_TTL_ACTIVITIES,
    CACHE_TTL_STATS
)

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.resource('dynamodb', region_name=AWS_REGION)


class CacheManager:
    """Gerencia cache no DynamoDB"""
    
    def __init__(self):
        self.table = dynamodb.Table(DYNAMODB_TABLE_CACHE)
    
    def get(self, key: str) -> Optional[Dict[str, Any]]:
        """Recupera item do cache se não expirou"""
        try:
            response = self.table.get_item(Key={'cache_key': key})
            if 'Item' in response:
                item = response['Item']
                # Verifica expiração
                if datetime.fromisoformat(item['expires_at']) > datetime.now(datetime.now().astimezone().tzinfo):
                    logger.info(f"Cache HIT: {key}")
                    return json.loads(item['data'])
                else:
                    logger.info(f"Cache EXPIRED: {key}")
                    self.delete(key)
            logger.info(f"Cache MISS: {key}")
            return None
        except Exception as e:
            logger.error(f"Erro ao recuperar cache: {e}")
            return None
    
    def set(self, key: str, data: Dict[str, Any], ttl: int) -> bool:
        """Armazena item no cache com TTL"""
        try:
            expires_at = datetime.now() + timedelta(seconds=ttl)
            self.table.put_item(
                Item={
                    'cache_key': key,
                    'data': json.dumps(data),
                    'expires_at': expires_at.isoformat(),
                    'created_at': datetime.now().isoformat()
                }
            )
            logger.info(f"Cache SET: {key} (TTL: {ttl}s)")
            return True
        except Exception as e:
            logger.error(f"Erro ao armazenar cache: {e}")
            return False
    
    def delete(self, key: str) -> bool:
        """Remove item do cache"""
        try:
            self.table.delete_item(Key={'cache_key': key})
            return True
        except Exception as e:
            logger.error(f"Erro ao deletar cache: {e}")
            return False


class TokenManager:
    """Gerencia tokens de autenticação"""
    
    def __init__(self):
        self.table = dynamodb.Table(DYNAMODB_TABLE_USERS)
    
    def save_token(self, user_id: str, tokens: Dict[str, Any]) -> bool:
        """Salva access_token e refresh_token para um usuário"""
        try:
            self.table.update_item(
                Key={'user_id': user_id},
                UpdateExpression='SET #tokens = :tokens, #updated = :updated',
                ExpressionAttributeNames={
                    '#tokens': 'tokens',
                    '#updated': 'updated_at'
                },
                ExpressionAttributeValues={
                    ':tokens': {
                        'access_token': tokens.get('access_token'),
                        'refresh_token': tokens.get('refresh_token'),
                        'expires_at': tokens.get('expires_at'),
                        'token_type': tokens.get('token_type', 'Bearer')
                    },
                    ':updated': datetime.now().isoformat()
                }
            )
            logger.info(f"Tokens salvos para usuário: {user_id}")
            return True
        except Exception as e:
            logger.error(f"Erro ao salvar tokens: {e}")
            return False
    
    def get_token(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Recupera tokens de um usuário"""
        try:
            response = self.table.get_item(Key={'user_id': user_id})
            if 'Item' in response and 'tokens' in response['Item']:
                return response['Item']['tokens']
            return None
        except Exception as e:
            logger.error(f"Erro ao recuperar tokens: {e}")
            return None


def response_success(data: Dict[str, Any], status_code: int = 200) -> Dict[str, Any]:
    """Formata resposta de sucesso"""
    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps({
            'success': True,
            'data': data,
            'timestamp': datetime.now().isoformat()
        })
    }


def response_error(message: str, status_code: int = 400, error_code: str = 'ERROR') -> Dict[str, Any]:
    """Formata resposta de erro"""
    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps({
            'success': False,
            'error': {
                'message': message,
                'code': error_code
            },
            'timestamp': datetime.now().isoformat()
        })
    }


def generate_cache_key(prefix: str, user_id: str, suffix: str = '') -> str:
    """Gera chave de cache única"""
    key_str = f"{prefix}:{user_id}:{suffix}"
    return hashlib.sha256(key_str.encode()).hexdigest()
