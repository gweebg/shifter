class YearOutOfBoundsException(Exception):
    def __init__(self, message):
        super().__init__(message)


class CourseNameDoesNotExistException(Exception):
    def __init__(self, message):
        super().__init__(message)


