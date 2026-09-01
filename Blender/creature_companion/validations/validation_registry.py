# Store all validations (populated during registration)
VALIDATIONS = []


def register_validator(cls):
    VALIDATIONS.append(cls())
    return cls


def register():
    VALIDATIONS.sort(key=lambda x: x.NAME)


def unregister():
    VALIDATIONS.clear()