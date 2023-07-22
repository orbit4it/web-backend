import datetime


def get_greeting():
    current_hour = datetime.datetime.now().hour

    if 5 <= current_hour < 12:
        return "Selamat pagi!"
    elif 12 <= current_hour < 15:
        return "Selamat siang!"
    elif 15 <= current_hour < 18:
        return "Selamat sore!"
    else:
        return "Selamat malam!"
