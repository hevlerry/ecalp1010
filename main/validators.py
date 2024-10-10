import re
from django.core.exceptions import ValidationError

class StudentEmailValidator:
    def __call__(self, value):
        if not re.match(r'^[\w\.-]+@student\.hau\.edu\.ph$', value):
            raise ValidationError('Email must end with @student.hau.edu.ph')