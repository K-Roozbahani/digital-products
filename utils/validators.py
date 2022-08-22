from django.utils.translation import ugettext_lazy as _
from django.core.validators import RegexValidator


class PhoneNumberValidator(RegexValidator):
    regex = r'^989[0-3,9]\d{8}$'
    message = 'A user with this mobile number already exist.'
    code = 'invalid_phone_number'


class SKUValidator(RegexValidator):
    regex = '^[a-zA-Z0-9\-\ ]{6,20}$'
    message = 'SKU must be alphanumeric with 6 to 20 characters'
    code = 'invalid_sku'


validate_sku = SKUValidator()
validate_phone_number = PhoneNumberValidator
