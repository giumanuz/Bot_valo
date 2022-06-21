from datetime import date, timedelta


class Prodigit:
    LOGIN_URL = "https://prodigit.uniroma1.it/names.nsf?Login"
    PRENOTATION_URL = "https://prodigit.uniroma1.it/prenotazioni/prenotaaule.nsf/prenotaposto-aula-lezioni" \
                      "?OpenForm&Seq=5"
    EXAM_PRENOTATION_URL = "https://prodigit.uniroma1.it/prenotazioni/prenotaaule.nsf/prenotaposto-in-aula-esame" \
                           "?OpenForm&Seq=5"

    @staticmethod
    def get_sundays_count(day1: date, day2: date) -> int:
        count = 0
        while day1 <= day2:
            if day1.weekday() == 6:
                count += 1
                day1 += timedelta(days=7)
            else:
                day1 += timedelta(days=1)
        return count

    @staticmethod
    def get_prenotation_day(day: date) -> int:
        today = date.today()
        days_difference = (day - today).days + 1
        return days_difference - Prodigit.get_sundays_count(today, day)
