class Validation(object):
    NAME = None

    def __init__(self):
        self.__errors = {}

    def reset(self):
        self.__errors.clear()

    def validate(self, context, scene):
        raise NotImplementedError()

    def warning(self, message, repair_func=None, repair_context=None):
        self.__add_error(False, message, repair_func, repair_context)

    def error(self, message, repair_func=None, repair_context=None):
        self.__add_error(True, message, repair_func, repair_context)

    def __add_error(self, error_type, message, repair_func, repair_context):
        if not isinstance(repair_context, tuple):
            repair_context = (repair_context,)
        self.__errors[len(self.__errors)] = (error_type, message, (repair_func, repair_context) if repair_func else None)

    def has_errors(self):
        return bool(self.__errors)

    def iter_errors(self):
        for error_id in self.__errors:
            error_type, message, repair = self.__errors[error_id]
            yield error_id, error_type, message, repair

    def has_repair(self, error_id):
        return bool(self.__errors[error_id][2])

    def repair(self, error_id):
        _, _, repair = self.__errors[error_id]
        if repair:
            repair_func, repair_context = repair
            return repair_func(repair_context)
        return False
