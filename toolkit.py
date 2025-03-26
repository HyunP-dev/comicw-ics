from __future__ import annotations
from dataclasses import dataclass
from datetime import date, timedelta
import sqlite3

import requests
import vobject


sqlite3.register_adapter(date, date.isoformat)


@dataclass(frozen=True)
class Event:
    title: str
    place: str
    start_date: date
    end_date: date

    def __eq__(self, o):
        return self.title == o.title

    @staticmethod
    def from_ajax() -> set[Event]:
        res = requests.post("https://comicw.co.kr/bbs/ajax.main.php", dict(type="comic")).json()
        current_events = [Event(title=event["title"],
                        place=event["place"],
                        start_date=date.fromisoformat(event["startDate"]),
                        end_date=date.fromisoformat(event["endDate"])) for event in res]
        
        con = sqlite3.connect("comicw.db")
        cursor = con.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS comic (title TEXT, place TEXT, start_date DATE, end_date DATE);")
        con.commit()

        cursor.execute("SELECT * FROM comic;")
        saved_events = map(lambda row: Event(row[0], row[1],
                                             date.fromisoformat(row[2]),
                                             date.fromisoformat(row[3])), cursor.fetchall())
        
        current_events = set(current_events)
        saved_events = set(saved_events)

        for event in current_events - saved_events:
            cursor.execute("INSERT INTO comic VALUES (?, ?, ?, ?)", (event.title, event.place, event.start_date, event.end_date))
            con.commit()

        return saved_events | current_events

    @staticmethod
    def to_ical() -> vobject.base.Component:
        cal = vobject.iCalendar()
        for event in Event.from_ajax():
            vevent = cal.add("vevent")
            vevent.add("summary").value = event.title
            vevent.add("location").value = event.place
            vevent.add('dtstart').value = event.start_date
            vevent.add('dtend').value = event.end_date + timedelta(1)
        return cal
