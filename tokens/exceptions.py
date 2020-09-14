from rest_framework.exceptions import APIException
from rest_framework import status

class AttendenceAlreadyStartedException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Attendence already started.'
    default_code = 'attendence_already_started'

class TokenAlreadyArchivedException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Token already archived.'
    default_code = 'token_already_archived'

class AttendenceNotStartedException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Attendence not started.'
    default_code = 'attendence_not_started'