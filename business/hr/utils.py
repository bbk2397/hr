from datetime import date, timedelta


def get_age(dob):
    return int((date.today() - dob) / timedelta(days=365)) 
