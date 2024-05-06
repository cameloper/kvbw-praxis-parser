from enum import StrEnum

class Address(object):
    def __init__(self, plz, province, city, street_no):
        self.plz = plz # 76131
        self.province = province # Karlsruhe - Stadt
        self.city = city # Oststadt
        self.street_no = street_no # Haizingerstraße 11

    def to_csv(self):
        return ",".join([self.plz, self.province, self.city, self.street_no])

class Weekday(StrEnum):
    MONDAY = 'Mo'
    TUESDAY = 'Di'
    WEDNSDAY = 'Mi'
    THURSDAY = 'Do'
    FRIDAY = 'Fr'
    SATURDAY = 'Sa'
    SUNDAY = 'So'

    def to_csv(self):
        return "{}".format(self)

class Time(object):
    def __init__(self, workday, time_tuples):
        self.workday = workday # MONDAY
        self.time_tuples = time_tuples # [("12:00", "13:00"), ("14:00", "16:30")]

    def to_csv(self):
        tuples = " & ".join(["{} - {}".format(x[0], x[1]) for x in self.time_tuples])
        return "{}: {}".format(self.workday, tuples)

class Praxis(object):
    def __init__(self, name, email, tel, fax, web, address, praxistypes = list()):
        self.name = name # Praxis A und B
        self.email = email # info@praxis-ab.de
        self.tel = tel # 0721123456
        self.fax = fax # 0721789012
        self.web = web # praxis-ab.de
        self.address = address # type Address
        self.praxistypes = praxistypes # Zweigpraxis

    def to_csv(self):
        return ",".join([self.name,
                         ";".join(self.email),
                         ";".join(self.tel),
                         ";".join(self.fax),
                         ";".join(self.web),
                         self.address.to_csv(),
                         ";".join(self.praxistypes)])
        
class Arzt(object):
    def __init__(self,
                 degree = "",
                 name = "",
                 surname = "",
                 ids = dict(),
                 languages = list(),
                 status = "",
                 drtype = "",
                 fields = list(),
                 focus = list(),
                 permits = list(),
                 misc = list(),
                 praxis = None,
                 office_hours = list(),
                 phone_hours = list()):
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

    def to_csv(self):
        return ",".join([self.degree, self.name, self.surname,
                         ";".join(self.ids),
                         ";".join(self.languages),
                         self.status, self.drtype,
                         ";".join(self.fields),
                         ";".join(self.focus),
                         ";".join(self.permits),
                         self.praxis.to_csv(),
                         ";".join([x.to_csv() for x in self.office_hours]),
                         ";".join([x.to_csv() for x in self.phone_hours])])
