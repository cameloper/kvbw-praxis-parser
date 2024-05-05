class Arzt(object):
    def __init__(self, degree, name, surname, ids, languages, status, field, permits, misc, praxis, office_hours, phone_hours):
        self.degree = degree # Dr. med.
        self.name = name # Max
        self.surname = surname # Mustermann
        self.ids = ids # {"LANR": 817957768, "BSNR": 526920700, "HBSNR": 526920700}
        self.languages = languages # ["en", "tr"]
        self.status = status # zugelassener Psychotherapeut
        self.field = field # Psychologischer Psychotherapeut
        self.permits = permits # ["Verhaltenstherapeutische Einzeltherapie – Erwachsene", "Verhaltenstherapeutische Gruppentherapie – Erwachsene"]
        self.misc = misc # ["Psychoanalyse"]
        self.praxis = praxis # type Praxis
        self.office_hours = office_hours # type [Time]
        self.phone_hours = phone_hours # type [Time]
