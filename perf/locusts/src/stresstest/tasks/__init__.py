from http import HTTPStatus
from stresstest import HTTPStatusReason


# Base is used only for internal fonctions (not tasks)
# If you use @task, push your fonction into CommonTaskSet
class BaseTaskSet:

    def shoot(self, url, name=None, traceback=None):
        if name is None:
            name = url
        with self.client.get(url, catch_response=True, name=name) as response:
            print(f"[DEBUG] shoot {url}")
            if traceback is not None:
                traceback(response)
            return response

    # TODO : need a refactoring
    # Maybe switch to Error 5xx for failure()
    # 5xx => LB can't reach the app
    # another error code like 4xx isn't really useful
    def traceback(self, response):
        status_code = response.status_code
        if status_code == HTTPStatus.OK:
            response.success()
        elif status_code == HTTPStatus.CREATED:
            response.success()
        elif status_code == HTTPStatus.TOO_MANY_REQUESTS:
            response.success()   # success to avoid limit rate error
            # (TODO: check if still necessary, used for some endpoint with limit rate)
        elif status_code == 0:
            response.failure(f"Failure: No Data (aborted)")
        elif status_code >= 500:   # Bad Gateway or Gateway timeout
            response.failure(f"Failure: Cannot reach app : {HTTPStatusReason(status_code)} (HTTP Code {status_code})")
        else:
            response.failure(f"Failure: {HTTPStatusReason(status_code)} (HTTP Code {status_code}) (*)")

