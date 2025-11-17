import uuid
import random
import logging
import requests
import threading
from datetime import datetime, timedelta
from tenacity import retry, stop_after_attempt, wait_fixed

# user agent samples
desktop_agents = [
    # Chrome Windows
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
    
    # Chrome Mac
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    
    # Firefox Windows
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0",
    
    # Firefox Mac
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:121.0) Gecko/20100101 Firefox/121.0",
    
    # Safari Mac
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
    
    # Edge Windows
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
    
    # Chrome Linux
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
]

mobile_agents = [
    # iPhone
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
    
    # Android Chrome
    "Mozilla/5.0 (Linux; Android 13; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.43 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; SM-S908B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.6045.66 Mobile Safari/537.36",
    
    # Android Firefox
    "Mozilla/5.0 (Android 13; Mobile; rv:121.0) Gecko/121.0 Firefox/121.0",
]


class TokenRequestError(Exception):
    """API 토큰 요청 과정에서 발생한 오류를 처리하기 위한 커스텀 예외"""
    def __init__(self, original_error, status_code=None, error_message=None, response_body=None):
        self.original_error = original_error
        self.status_code = status_code
        self.error_message = error_message
        self.response_body = response_body
        
        # 예외 정보를 객체 형태로 args에 저장
        error_info = {
            "original_error": original_error,
            "status_code": status_code,
            "error_message": error_message,
            "response_body": response_body
        }
        
        # args 튜플의 첫 번째 요소로 객체 전달
        super().__init__(error_info)

class OAuth:
    BASE_URL = "https://openapi.dbsec.co.kr:8443"

    def __init__(
        self, 
        appkey: str, 
        appsecretkey: str, 
        headers: dict = {}, 
        token: str = None,
        token_type: str = None,
        expire_in: str = None,
    ):
        self.appkey = appkey
        self.appsecretkey = appsecretkey
        self.token = token
        self.token_type = token_type
        self.expire_in = expire_in
        self.logger = logging.getLogger(__name__)
        self._initialized = True
        self.headers = headers
        self._lock = threading.Lock()  # 인스턴스별 락
        
        # init auth
        self.init_auth()
        
    def init_auth(self):
        # init token
        self.init_token()
        
    def init_token(self, is_refresh: bool = False):
        # init token
        self.get_token(is_refresh)
        
        # init headers
        self.get_auth_header()

    def get_token(self, is_refresh: bool = False) -> str:
        # 토큰 강제 업데이트
        if is_refresh:
            self.request_token()
            return self.token
        
        if not self.is_token_valid():
            with self._lock:
                if not self.is_token_valid():
                    self.request_token()
        return self.token

    def is_token_valid(self) -> bool:
        if not self.token or not self.token_type or not self.expire_in:
            return False
        return datetime.now() + timedelta(minutes=10) < self.expire_in

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_fixed(70), # 70초 고정 대기 후 재시도
        reraise=True
    )
    def request_token(self) -> None:
        headers = {"content-type": "application/x-www-form-urlencoded"}
        data = {
            "grant_type": "client_credentials",
            "appkey": self.appkey,
            "appsecretkey": self.appsecretkey,
            "scope": "oob",
        }
        try:
            self.logger.info("Requesting new access token from DB Securities API")
            response = requests.post(
                f"{self.BASE_URL}/oauth2/token", headers=headers, data=data
            )
            response.raise_for_status()
            token_data = response.json()

            self.token = token_data.get("access_token")
            expire_in = int(token_data.get("expires_in", 86400))
            self.expire_in = datetime.now() + timedelta(seconds=expire_in)
            self.token_type = token_data.get("token_type")
            self.logger.info(
                f"New access token obtained. Valid until: {self.expire_in}"
            )
        except requests.exceptions.RequestException as e:
            status_code = None
            error_message = str(e)
            response_body = None
            
            # response 객체가 있는 경우 상태 코드와 응답 내용 추출
            if hasattr(e, 'response') and e.response is not None:
                status_code = e.response.status_code
                
                # 응답 본문 저장
                try:
                    response_body = e.response.json()
                    error_message = response_body.get('error_description', response_body.get('error', str(e)))
                except ValueError:
                    # JSON이 아닌 경우 텍스트 내용 사용
                    response_body = e.response.text
                    error_message = response_body
            
            self.logger.error(f"Failed to obtain access token: Status code: {status_code}, Error: {error_message}")
            raise TokenRequestError(e, status_code, error_message, response_body)

    def revoke_token(self) -> dict:
        if not self.token:
            self.logger.warning("No token to revoke")
            return {"code": 400, "message": "No token to revoke"}

        headers = {"content-type": "application/x-www-form-urlencoded"}
        data = {
            "appkey": self.appkey,
            "appsecretkey": self.appsecretkey,
            "token": self.token,
            "token_type_hint": "access_token",
        }
        try:
            self.logger.info("Revoking access token")
            response = requests.post(
                f"{self.BASE_URL}/oauth2/revoke", headers=headers, data=data
            )
            response.raise_for_status()
            result = response.json()
            if result.get("code") == 200:
                self.token = None
                self.expire_in = None
                self.token_type = None
                self.logger.info("Token successfully revoked")
            return result
        except requests.RequestException as e:
            self.logger.error(f"Failed to revoke token: {str(e)}")
            if hasattr(e, "response") and e.response:
                self.logger.error(f"Response: {e.response.text}")
            raise e

    def get_auth_header(self) -> dict:    
        try:
            from fake_useragent import UserAgent
            user_agent = UserAgent().random
        except Exception as e:
            self.logger.error(f"UserAgent Error: {e}")
            user_agent = random.choice(desktop_agents + mobile_agents)
        
        headers = {
            'Authorization': f"{self.token_type} {self.get_token()}",
            'User-Agent': user_agent,
            'X-Session-ID': str(uuid.uuid4()),
            'Accept': 'application/json',
            'Accept-Language': 'ko-KR,ko;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Cache-Control': 'no-cache',
            'Pragma': 'no-cache',
            'Connection': 'keep-alive',
            **self.headers
        }
        # 20% 확률로 추가 헤더 삽입 (자연스러운 변화)
        if random.random() < 0.2:
            headers['X-Forwarded-For'] = f"10.0.{random.randint(1,254)}.{random.randint(1,254)}"
        self.headers = headers        
        return self.headers