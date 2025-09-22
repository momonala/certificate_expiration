import logging
import re
from datetime import datetime
from glob import glob
from zoneinfo import ZoneInfo

import requests

from gcal import (AppCertInfo, create_or_update_calendar_event, load_event_ids,
                  save_event_ids)
from values import telegram_api_token, telegram_chat_id
logger = logging.getLogger(__name__)
telegrap_api_uri = f'https://api.telegram.org/bot{telegram_api_token}/sendMessage'

certs = glob("/Users/mnalavadi/Library/Developer/Xcode/UserData/Provisioning Profiles/*mobileprovision")
certs = glob("/Users/mohit/Library/Developer/Xcode/UserData/Provisioning Profiles/*mobileprovision")
BERLIN_TZ = ZoneInfo("Europe/Berlin")


def extract_app_name(_certificate: str) -> tuple[str, datetime]:
    # Define the regular expression pattern
    # line_with_app_name = d[5].decode("utf-8")
    identifier = "XC mnalavadi "
    lines = [x.decode("utf-8") for x in _certificate[4:7]]
    line_with_app_name = [x for x in lines if identifier in x][0]
    pattern = fr'<string>{identifier}(.*?)</string>'
    match = re.search(pattern, line_with_app_name)
    if not match:
        print(f"ERROR: Could not find app name in: {line_with_app_name}")
        return None, None
    app_name = match.group(1)
    if "test" in app_name.lower() or "widget" in app_name.lower():
        return None, None

    date_string = [x for x in _certificate if b"date" in x][1].decode("utf-8")
    date_time_str = date_string.split('<date>')[1].split('</date>')[0]
    # Convert UTC to Berlin time
    expiration_date = datetime.strptime(date_time_str, '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=ZoneInfo("UTC")).astimezone(BERLIN_TZ)

    return app_name, expiration_date


def send_telegram_message(app_name: str, expiration_date: datetime):
    formatted_expiriation = expiration_date.strftime("%a %d %b at %H:%M %Z")

    current_datetime = datetime.now(BERLIN_TZ)
    time_difference = expiration_date - current_datetime
    days = time_difference.days
    hours, remainder = divmod(time_difference.seconds, 3600)
    minutes, _ = divmod(remainder, 60)

    l1 = f"Expiration Date: {formatted_expiriation}"
    l2 = f'Expires in: {days}d {hours}h {minutes}m'
    telegram_msg = f"{app_name}\n{l1}\n{l2}"
    print(telegram_msg, "\n")

    json = {'chat_id': telegram_chat_id, 'text': f"```---{telegram_msg}```", 'parse_mode': 'Markdown'}
    resp = requests.post(telegrap_api_uri, json=json)
    if resp.status_code != 200:
        logger.error(resp.text)


def main():

    for cert in certs:
        with open(cert, "rb") as f:
            _certificate = f.readlines()

        app_name, expiration_date = extract_app_name(_certificate)
        if not app_name:
            continue

        # Create or update calendar event
        app_info = AppCertInfo(app_name=app_name, expiration_date=expiration_date, cert_path=cert)
        event_mapping = load_event_ids()
        event_id = event_mapping.get(app_name)
        new_event_id = create_or_update_calendar_event(app_info, event_id)
        if new_event_id:
            event_mapping[app_name] = new_event_id
        save_event_ids(event_mapping)

        # Send Telegram notification
        send_telegram_message(app_name, expiration_date)


if __name__ == "__main__":
    main()
