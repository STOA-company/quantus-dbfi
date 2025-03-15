from oauth import Oauth
import logging
from typing import Dict, Any, Optional
import requests

class BaseAPI:
    BASE_URL = "https://openapi.db-fi.com:8443"
    
    def __init__(self, auth: Oauth):
        self.auth = auth
        self.logger = logging.getLogger(__name__)
    
    def _request(self, method: str, endpoint: str, params: Optional[Dict[str, Any]] = None, 
                 data: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None,
                 content_type: str = "application/json") -> dict:

        url = f"{self.BASE_URL}{endpoint}"
        
        request_headers = self.auth.get_auth_header()
        request_headers["Content-Type"] = content_type
        
        if headers:
            request_headers.update(headers)
        
        try:
            if content_type == "application/json":
                response = requests.request(
                    method=method,
                    url=url,
                    params=params,
                    json=data,
                    headers=request_headers
                )
            else:
                response = requests.request(
                    method=method,
                    url=url,
                    params=params,
                    data=data,
                    headers=request_headers
                )
            
            response.raise_for_status()
            
            if 'application/json' in response.headers.get('Content-Type', ''):
                return response.json()
            
            return {"text": response.text}
            
        except requests.RequestException as e:
            self.logger.error(f"API request failed: {str(e)}")
            if hasattr(e, 'response') and e.response is not None:
                self.logger.error(f"Response: {e.response.text}")
            raise


