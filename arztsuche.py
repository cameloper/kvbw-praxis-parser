from enum import StrEnum

class Address(object):
    def __init__(self, plz, province, city, street_no):
        self.plz = plz # 76131
        self.province = province # Karlsruhe - Stadt
        self.city = city # Oststadt
        self.street_no = street_no # Haizingerstraße 11

class WorkDay(StrEnum):
    MONDAY = 'Mo'
    TUESDAY = 'Di'
    WEDNSDAY = 'Mi'
    THURSDAY = 'Do'
    FRIDAY = 'Fr'

class Time(object):
    def __init__(self, workday, time_tuples):
        self.workday = workday # MONDAY
        self.time_tuples = time_tuples # [("12:00", "13:00"), ("14:00", "16:30")]

class Praxis(object):
    def __init__(self, name, email, tel, fax, web, address, praxistypes):
        self.name = name # Praxis A und B
        self.email = email # info@praxis-ab.de
        self.tel = tel # 0721123456
        self.fax = fax # 0721789012
        self.web = web # praxis-ab.de
        self.address = address # type Address
        self.praxistypes = praxistypes # Zweigpraxis
        
class Arzt(object):
    def __init__(self,
                 degree = "",
                 name = "",
                 surname = "",
                 ids = None,
                 languages = None,
                 status = "",
                 drtype = "",
                 fields = None,
                 focus = None,
                 permits = None,
                 misc = None,
                 praxis = None,
                 office_hours = None,
                 phone_hours = None):
        self.degree = degree # Dr. med.
        self.name = name # Max
        self.surname = surname # Mustermann
        self.ids = ids # {"LANR": 817957768, "BSNR": 526920700, "HBSNR": 526920700}
        self.languages = languages # ["en", "tr"]
        self.status = status # zugelassener Psychotherapeut
        self.drtype = drtype # Facharzt
        self.fields = fields # Psychologischer Psychotherapeut
        self.focus = focus # Nephrologie
        self.permits = permits # ["Verhaltenstherapeutische Einzeltherapie – Erwachsene", "Verhaltenstherapeutische Gruppentherapie – Erwachsene"]
        self.misc = misc # ["Psychoanalyse"]
        self.praxis = praxis # type Praxis
        self.office_hours = office_hours # type [Time]
        self.phone_hours = phone_hours # type [Time]
