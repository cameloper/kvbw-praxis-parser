from enum import Enum

class WorkDay(Enum):
    MONDAY = 0
    TUESDAY = 1
    WEDNSDAY = 2
    THURSDAY = 3
    FRIDAY = 4

class Time(object):
    def __init__(self, workday, startTime, endTime):
        self.workday = workday # MONDAY
        self.startTime = startTime # 12:00
        self.endTime = endTime # 14:30
