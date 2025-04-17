import os
import sys 

class AppException(Exception):

    def __init__(self, error_message: Exception, error_detail: sys):
        """
        Custom exception class to handle exceptions in the application.

        Parameters:
            error_message (Exception): The exception message.
            error_detail (sys): The system information where the exception occurred.
        """
        super().__init__(error_message)
        self.error_message = AppException.error_message_detail(error_message, error_detail)

    @staticmethod
    def error_message_detail(error: Exception, error_detail: sys) -> str:
        """
        Generates a detailed error message.

        Parameters:
            error (Exception): The exception message.
            error_detail (sys): The system information where the exception occurred.

        Returns:
            str: A detailed error message.
        """
        _, _, exc_tb = error_detail.exc_info()
        file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        line_number = exc_tb.tb_lineno
        error_message = f"Error occurred in script: [{file_name}] at line number: [{line_number}] error message: [{str(error)}]"
        return error_message
    
    def __repr__(self):
        """
        Formatted object representation of the exception message.
        """
        return AppException.__name__.str(self.error_message)
    
    def __str__(self):
        """
        String representation of the exception message.
        """
        return self.error_message
    