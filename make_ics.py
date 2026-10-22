#!/usr/bin/env python3
"""Build an iOS-compatible .ics of San Salvario A.S.D. matches (CSI Open M / Eccellenza B 2026/27)."""
from datetime import datetime, timedelta, timezone

TEAM = "San Salvario A.S.D."
OUT = "san_salvario_2026-27.ics"
ARRIVE_BEFORE = timedelta(hours=1)   # meeting time shown in the description only
MATCH_LENGTH = timedelta(hours=1, minutes=30)  # event runs from kick-off to 1.5h after

# key: (venue name, street address, lat, lon) -- lat/lon from OpenStreetMap; None = let iOS geocode the address
VENUES = {
    "nitti":      ("USD San Giorgio - Campo Nitti", "Via Nitti 6, 10137 Torino TO, Italia", 45.043637, 7.622731),
    "einaudi":    ("Impianto sportivo Einaudi", "Via Luigi Einaudi 42, 10024 Moncalieri TO, Italia", 44.996791, 7.686200),
    "leini":      ("La Cittadella", "Via Carlo Gremo 59, 10040 Leinì TO, Italia", 45.182366, 7.724880),
    "cus":        ("CUS Torino", "Via Milano 63, 10095 Grugliasco TO, Italia", 45.066593, 7.606064),
    "ghilardi":   ("Campo Don Luigi Ghilardi", "Strada Don Luigi Ghilardi, 10098 Rivoli TO, Italia", 45.058176, 7.523945),
    "riva":       ("Campo San Giuseppe Riva", "Piazza Falcone e Borsellino, 10020 Riva presso Chieri TO, Italia", 44.987192, 7.867950),
    "sisport":    ("Sisport", "Via Santa Cristina 1, 10036 Settimo Torinese TO, Italia", 45.126261, 7.752130),
    "vallette":   ("Orione Vallette", "Via dei Gladioli 39, 10151 Torino TO, Italia", 45.100307, 7.630503),
    "pertusa":    ("Pertusa", "Via Genova 161, 10127 Torino TO, Italia", 45.025104, 7.666658),
    "devietti":   ("Devietti Goggia", "Via Aldo Devietti Goggia 66, 10077 San Maurizio Canavese TO, Italia", None, None),
    "sanmauro":   ("Campo Luigi Einaudi", "Parco Luigi Einaudi 3/A, 10099 San Mauro Torinese TO, Italia", 45.108374, 7.767888),
    "centrocampo": ("Centrocampo", "Via Petrella 40, 10154 Torino TO, Italia", 45.089709, 7.703934),
}

# (code, round, dd/mm/yy, kick-off, home, away, venue)
MATCHES = [
    ("262A2",  "Andata giornata 1",  "03/10/26", "12:45", "Orange 11 A.S.D.", TEAM, "nitti"),
    ("262A12", "Andata giornata 2",  "09/10/26", "21:00", TEAM, "Automotive Lighting Italia Spa", "nitti"),
    ("262A17", "Andata giornata 3",  "16/10/26", "21:00", TEAM, "Oratorio Leini", "nitti"),  # swapped with return leg
    ("262A25", "Andata giornata 4",  "23/10/26", "21:00", TEAM, "Dinamo Torino", "nitti"),
    ("262A32", "Andata giornata 5",  "31/10/26", "14:30", "Andromeda", TEAM, "cus"),
    ("262A38", "Andata giornata 6",  "06/11/26", "21:00", TEAM, "Don Bosco Caselle", "nitti"),
    ("262A47", "Andata giornata 7",  "15/11/26", "11:00", "San Martino Rivoli", TEAM, "ghilardi"),
    ("262A51", "Andata giornata 8",  "20/11/26", "21:00", TEAM, "Sampigandia", "nitti"),
    ("262A62", "Andata giornata 9",  "28/11/26", "14:30", "G.S. Rivese", TEAM, "riva"),
    ("262A64", "Andata giornata 10", "11/12/26", "21:00", TEAM, "Real Benny", "nitti"),
    ("262A77", "Andata giornata 11", "22/01/27", "21:00", TEAM, "Valsalice Alfieri", "nitti"),
    ("262A78", "Andata giornata 12", "30/01/27", "15:30", "Sporting San Giuseppe A.S.D.", TEAM, "sisport"),
    ("262A90", "Andata giornata 13", "05/02/27", "21:00", TEAM, "Sportinsieme Piobesi Torinese", "nitti"),
    ("262R2",  "Ritorno giornata 1",  "12/02/27", "21:00", TEAM, "Orange 11 A.S.D.", "nitti"),
    ("262R12", "Ritorno giornata 2",  "20/02/27", "13:00", "Automotive Lighting Italia Spa", TEAM, "vallette"),
    ("262R17", "Ritorno giornata 3",  "27/02/27", "16:45", "Oratorio Leini", TEAM, "leini"),  # swapped with first leg
    ("262R25", "Ritorno giornata 4",  "06/03/27", "13:00", "Dinamo Torino", TEAM, "pertusa"),
    ("262R32", "Ritorno giornata 5",  "12/03/27", "21:00", TEAM, "Andromeda", "nitti"),
    ("262R38", "Ritorno giornata 6",  "20/03/27", "15:00", "Don Bosco Caselle", TEAM, "devietti"),
    ("262R47", "Ritorno giornata 7",  "02/04/27", "21:00", TEAM, "San Martino Rivoli", "nitti"),
    ("262R51", "Ritorno giornata 8",  "10/04/27", "12:45", "Sampigandia", TEAM, "nitti"),
    ("262R62", "Ritorno giornata 9",  "16/04/27", "21:00", TEAM, "G.S. Rivese", "nitti"),
    ("262R64", "Ritorno giornata 10", "26/04/27", "21:00", "Real Benny", TEAM, "sanmauro"),
    ("262R77", "Ritorno giornata 11", "08/05/27", "13:00", "Valsalice Alfieri", TEAM, "centrocampo"),
    ("262R78", "Ritorno giornata 12", "14/05/27", "21:00", TEAM, "Sporting San Giuseppe A.S.D.", "nitti"),
    # Ritorno giornata 13 (262R90, Sportinsieme Piobesi - San Salvario) has no date in the PDF yet.
]

VTIMEZONE = """BEGIN:VTIMEZONE
TZID:Europe/Rome
BEGIN:DAYLIGHT
TZOFFSETFROM:+0100
TZOFFSETTO:+0200
TZNAME:CEST
DTSTART:19700329T020000
RRULE:FREQ=YEARLY;BYMONTH=3;BYDAY=-1SU
END:DAYLIGHT
BEGIN:STANDARD
TZOFFSETFROM:+0200
TZOFFSETTO:+0100
TZNAME:CET
DTSTART:19701025T030000
RRULE:FREQ=YEARLY;BYMONTH=10;BYDAY=-1SU
END:STANDARD
END:VTIMEZONE""".splitlines()


def esc(s):
    return s.replace("\\", "\\\\").replace(";", "\\;").replace(",", "\\,").replace("\n", "\\n")


def fold(line):
    """Fold to 75 octets per RFC 5545 without splitting UTF-8 sequences."""
    out, cur = [], b""
    for ch in line:
        b = ch.encode()
        if len(cur) + len(b) > (75 if not out else 74):
            out.append(cur)
            cur = b""
        cur += b
    out.append(cur)
    return "\r\n ".join(x.decode() for x in out)


def local(dt):
    return dt.strftime("%Y%m%dT%H%M%S")


def event(code, rnd, date, ko, home, away, vkey, stamp):
    kickoff = datetime.strptime(f"{date} {ko}", "%d/%m/%y %H:%M")
    name, addr, lat, lon = VENUES[vkey]
    where = "Casa" if home == TEAM else "Trasferta"
    lines = [
        "BEGIN:VEVENT",
        f"UID:{code}-2026-27@san-salvario-calendar",
        f"DTSTAMP:{stamp}",
        f"DTSTART;TZID=Europe/Rome:{local(kickoff)}",
        f"DTEND;TZID=Europe/Rome:{local(kickoff + MATCH_LENGTH)}",
        f"SUMMARY:{esc(f'⚽ {home} – {away}')}",
        f"LOCATION:{esc(f'{name}, {addr}')}",
        "DESCRIPTION:" + esc(
            f"Calcio A 11 CSI – Open M / Eccellenza B\n{rnd} ({code}) – {where}\n"
            f"Calcio d'inizio: {ko}\nRitrovo: {(kickoff - ARRIVE_BEFORE):%H:%M}"
        ),
    ]
    if lat is not None:
        lines += [
            f"GEO:{lat};{lon}",
            f'X-APPLE-STRUCTURED-LOCATION;VALUE=URI;X-ADDRESS="{addr.replace(",", "")}";'
            f'X-APPLE-RADIUS=150;X-TITLE="{name}":geo:{lat},{lon}',
        ]
    for trig, label in (("-P1D", "domani"), ("-PT2H", "tra 2 ore")):
        lines += [
            "BEGIN:VALARM",
            "ACTION:DISPLAY",
            f"DESCRIPTION:{esc(f'{home} – {away} ({label})')}",
            f"TRIGGER:{trig}",
            "END:VALARM",
        ]
    lines.append("END:VEVENT")
    return lines


def main():
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    lines = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//San Salvario A.S.D.//Calendario 2026-27//IT",
        "CALSCALE:GREGORIAN",
        "METHOD:PUBLISH",
        "X-WR-CALNAME:San Salvario A.S.D. 2026/27",
        "X-WR-TIMEZONE:Europe/Rome",
        *VTIMEZONE,
    ]
    for m in MATCHES:
        lines += event(*m, stamp)
    lines.append("END:VCALENDAR")
    with open(OUT, "w", encoding="utf-8", newline="") as f:
        f.write("\r\n".join(fold(l) for l in lines) + "\r\n")
    print(f"Wrote {OUT} with {len(MATCHES)} events")


if __name__ == "__main__":
    main()
