from typing import Union


class ResponseDataBuilder:
    @staticmethod
    def build_error_response(
        error_message: str, error_fields: dict = None, error_code: str = None
    ) -> dict:
        error_data = {"message": error_message}

        if error_code is not None:
            error_data.update({"code": error_code})
        if error_fields is not None:
            error_data.update({"fields": error_fields})

        response = {"error": error_data}

        return response

    @staticmethod
    def build_success_response(data: Union[dict, list]) -> dict:
        return {"data": data}
