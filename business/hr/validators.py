from django.core.exceptions import ValidationError

from hr.constants import (
    MAXIMUM_AGE,
    MINIMUM_WORKING_AGE
)
from hr.utils import (
    get_age
)


def validate_dob(dob):
    age = get_age(dob)
    if age > MAXIMUM_AGE:
        raise ValidationError(f'Age must be no greater than {MAXIMUM_AGE}, but is {age}')
    return True 

def validate_dob_with_yoe(dob, yoe):
    age = get_age(dob)
    diff = age - yoe
    if diff < MINIMUM_WORKING_AGE:
        raise ValidationError(f'Age minus yoe must be at least {MINIMUM_WORKING_AGE}, but is {age} - {yoe} = {diff}')
