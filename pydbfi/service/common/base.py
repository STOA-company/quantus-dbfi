import logging
import random
import time
from typing import Any, Dict, Optional

import requests
from tenacity import retry, stop_after_attempt, wait_exponential

from ...oauth import OAuth


class BaseService:
    BASE_URL = "https://openapi.dbsec.co.kr:8443"

    def __init__(self, auth: OAuth):
        self.auth = auth
        self.logger = logging.getLogger(__name__)
        
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(
            multiplier=1,    # 기본 승수
            min=1,          # 최소 대기 시간 (초)
            max=10          # 최대 대기 시간 (초)
        ),
        reraise=True
    )
    def _request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        content_type: str = "application/json",
        cont_yn: str = "N",
        cont_key: str = None,
        max_cont_cnt: int = 100,
        **kwargs,
    ) -> dict:
        url = f"{self.BASE_URL}{endpoint}"

        request_headers = {
            **(headers if isinstance(headers, dict) else {}),
            **self.auth.get_auth_header()
        }
        request_headers["Content-Type"] = content_type

        if cont_yn:
            request_headers["cont_yn"] = cont_yn

        if cont_key:
            request_headers["cont_key"] = cont_key


        try:
            self.logger.debug(
                f"Request to {url}, method={method}, headers={request_headers}"
            )
            self.logger.debug(f"Request data: {data}")

            if content_type == "application/json":
                response = requests.request(
                    method=method,
                    url=url,
                    params=params,
                    json=data,
                    headers=request_headers,
                )
            else:
                response = requests.request(
                    method=method,
                    url=url,
                    params=params,
                    data=data,
                    headers=request_headers,
                )

            if 500 <= response.status_code < 600:
                # token 유효성 만료: 토큰 재발급
                time.sleep(1.5)
                self.auth.request_token()

            response.raise_for_status()

            self.logger.debug(f"Response status: {response.status_code}")
            self.logger.debug(f"Response headers: {response.headers}")

            cont_yn = response.headers.get("cont_yn", "N")
            cont_key = response.headers.get("cont_key", "")
            cont_cnt = kwargs.get("cont_cnt", 0)
            if cont_yn == "Y" and cont_key != "" and cont_cnt < max_cont_cnt:
                # 연속 조회 여부 판단"
                kwargs.update(
                    outputs = kwargs.get("outputs", []) + [
                        response.json() if "application/json" in response.headers.get("Content-Type", "") else {"text": response.text}
                    ],
                    cont_cnt = kwargs.get("cont_cnt", 0) + 1
                )
                time.sleep(1.5) # 연속 조회를 위한 1초 대기
                return self._request(
                    method=method,
                    endpoint=endpoint,
                    params=params,
                    data=data,
                    content_type=content_type,
                    cont_yn=cont_yn,
                    cont_key=cont_key,
                    **kwargs
                )
            
            if kwargs.get("outputs"):
                return kwargs.get("outputs", []) + [
                    response.json() if "application/json" in response.headers.get("Content-Type", "") else {"text": response.text}
                ]
            else:
                if "application/json" in response.headers.get("Content-Type", ""):
                    return response.json()

                return {"text": response.text}

        except requests.RequestException as e:
            self.logger.error(f"API request failed: {str(e)}")
            if hasattr(e, "response") and e.response is not None:
                self.logger.error(f"Response({e.response.status_code}): {e.response.text}")
            raise e
