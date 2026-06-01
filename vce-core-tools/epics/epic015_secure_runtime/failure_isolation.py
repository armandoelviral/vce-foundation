class FailureIsolation:

    def protect(self, operation):

        try:

            result = operation()

            return {
                "success": True,
                "result": result
            }


        except Exception as error:

            return {
                "success": False,
                "error_type": type(
                    error
                ).__name__,
                "contained": True
            }
