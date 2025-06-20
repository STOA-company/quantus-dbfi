import logging
import random
import time
from typing import Any, Dict, Optional

import requests

from ...oauth import OAuth


class BaseService:
    BASE_URL = "https://openapi.dbsec.co.kr:8443"

    def __init__(self, auth: OAuth):
        self.auth = auth
        self.logger = logging.getLogger(__name__)

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
        max_retries: int = 3,
        initial_backoff: float = 1.0,
        max_backoff: float = 10.0,
        **kwargs,
    ) -> dict:
        url = f"{self.BASE_URL}{endpoint}"

        request_headers = self.auth.get_auth_header()
        request_headers["Content-Type"] = content_type

        if cont_yn:
            request_headers["cont_yn"] = cont_yn

        if cont_key:
            request_headers["cont_key"] = cont_key

        if headers:
            request_headers.update(headers)

        retry_count = 0
        backoff = initial_backoff

        while True:
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
                    if isinstance(response.text, dict) and response.text.get("rsp_cd") == "IGW00121":
                        # token 유효성 만료: 토큰 재발급
                        self.auth.request_token()
                    
                    if retry_count < max_retries:
                        retry_count += 1
                        jitter = random.uniform(0, 0.1 * backoff)
                        sleep_time = min(backoff + jitter, max_backoff)

                        self.logger.warning(
                            f"서버 오류 발생 (상태 코드: {response.status_code}). "
                            f"{retry_count}/{max_retries} 재시도 중... {sleep_time:.2f}초 후 재시도"
                        )

                        time.sleep(sleep_time)
                        backoff = min(backoff * 2, max_backoff)
                        continue
                    else:
                        self.logger.error(
                            f"최대 재시도 횟수({max_retries})를 초과했습니다. "
                            f"서버 오류가 지속됩니다. 상태 코드: {response.status_code}"
                        )

                response.raise_for_status()

                self.logger.debug(f"Response status: {response.status_code}")
                self.logger.debug(f"Response headers: {response.headers}")

                cont_yn = response.headers.get("cont_yn", "N")
                cont_key = response.headers.get("cont_key", "")
                cont_cnt = kwargs.get("cont_cnt", 0) # 최대 연속 조회 가능 회수 20회
                if cont_yn == "Y" and cont_key != "" and cont_cnt < 20:
                    # 연속 조회 여부 판단"
                    kwargs.update(
                        outputs = kwargs.get("outputs", []) + [
                            response.json() if "application/json" in response.headers.get("Content-Type", "") else {"text": response.text}
                        ],
                        cont_cnt = kwargs.get("cont_cnt", 0) + 1
                    )
                    time.sleep(1) # 연속 조회를 위한 1초 대기
                    return self._request(
                        method=method,
                        endpoint=endpoint,
                        params=params,
                        data=data,
                        content_type=content_type,
                        cont_yn=cont_yn,
                        cont_key=cont_key,
                        max_retries=max_retries,
                        initial_backoff=initial_backoff,
                        max_backoff=max_backoff,
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
                if not (
                    hasattr(e, "response")
                    and e.response
                    and 500 <= e.response.status_code < 600
                ):
                    self.logger.error(f"API request failed: {str(e)}")
                    if hasattr(e, "response") and e.response is not None:
                        self.logger.error(f"Response: {e.response.text}")
                    raise

                if hasattr(e, "response") and e.response:
                    response = e.response
                    if retry_count < max_retries:
                        retry_count += 1
                        jitter = random.uniform(0, 0.1 * backoff)
                        sleep_time = min(backoff + jitter, max_backoff)

                        self.logger.warning(
                            f"서버 오류 발생 (상태 코드: {response.status_code}). "
                            f"{retry_count}/{max_retries} 재시도 중... {sleep_time:.2f}초 후 재시도"
                        )

                        time.sleep(sleep_time)
                        backoff = min(backoff * 2, max_backoff)
                        continue

                self.logger.error(f"API request failed: {str(e)}")
                if hasattr(e, "response") and e.response is not None:
                    self.logger.error(f"Response: {e.response.text}")
                raise
