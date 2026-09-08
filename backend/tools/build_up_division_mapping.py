from __future__ import annotations

import csv
import re
from pathlib import Path


DISTRICTS = Path(
    "data/master/up/districts.csv"
)

DIVISIONS = Path(
    "data/master/up/divisions.csv"
)

DISTRICT_DIVISIONS = Path(
    "data/master/up/district_divisions.csv"
)


def norm(value: str) -> str:
    value = value.lower().strip()
    value = value.replace("&", "and")
    value = re.sub(r"[\(\)\-_,.]", " ", value)
    value = re.sub(r"\s+", " ", value)
    return value


DIVISION_MAP = {
    # Agra
    "agra": "AGRA",
    "firozabad": "AGRA",
    "mainpuri": "AGRA",
    "mathura": "AGRA",

    # Aligarh
    "aligarh": "ALIGARH",
    "etah": "ALIGARH",
    "hathras": "ALIGARH",
    "kasganj": "ALIGARH",

    # Ayodhya
    "ambedkar nagar": "AYODHYA",
    "amethi": "AYODHYA",
    "ayodhya": "AYODHYA",
    "bara banki": "AYODHYA",
    "barabanki": "AYODHYA",
    "sultanpur": "AYODHYA",

    # Azamgarh
    "azamgarh": "AZAMGARH",
    "ballia": "AZAMGARH",
    "mau": "AZAMGARH",

    # Bareilly
    "bareilly": "BAREILLY",
    "budaun": "BAREILLY",
    "pil ibhit": "BAREILLY",
    "pilibhit": "BAREILLY",
    "shahjahanpur": "BAREILLY",

    # Basti
    "basti": "BASTI",
    "sant kabeer nagar": "BASTI",
    "sant kabir nagar": "BASTI",
    "siddharth nagar": "BASTI",
    "siddharthnagar": "BASTI",

    # Chitrakoot
    "banda": "CHITRAKOOT",
    "chitrakoot": "CHITRAKOOT",
    "hamirpur": "CHITRAKOOT",
    "mahoba": "CHITRAKOOT",

    # Devipatan
    "bahraich": "DEVIPATAN",
    "balrampur": "DEVIPATAN",
    "gonda": "DEVIPATAN",
    "shrawasti": "DEVIPATAN",
    "shravasti": "DEVIPATAN",

    # Gorakhpur
    "deoria": "GORAKHPUR",
    "gorakhpur": "GORAKHPUR",
    "kushinagar": "GORAKHPUR",
    "kushi nagar": "GORAKHPUR",
    "maharajganj": "GORAKHPUR",
    "mahrajganj": "GORAKHPUR",

    # Jhansi
    "jalaun": "JHANSI",
    "jhansi": "JHANSI",
    "lalitpur": "JHANSI",

    # Kanpur
    "auraiya": "KANPUR",
    "etawah": "KANPUR",
    "farrukhabad": "KANPUR",
    "kannauj": "KANPUR",
    "kanpur dehat": "KANPUR",
    "kanpur nagar": "KANPUR",

    # Lucknow
    "hardoi": "LUCKNOW",
    "kheri": "LUCKNOW",
    "lakhimpur kheri": "LUCKNOW",
    "lucknow": "LUCKNOW",
    "rae bareli": "LUCKNOW",
    "raebareli": "LUCKNOW",
    "sitapur": "LUCKNOW",
    "unnao": "LUCKNOW",

    # Meerut
    "baghpat": "MEERUT",
    "bulandshahr": "MEERUT",
    "gautam buddha nagar": "MEERUT",
    "ghaziabad": "MEERUT",
    "hapur": "MEERUT",
    "meerut": "MEERUT",

    # Mirzapur
    "mirzapur": "MIRZAPUR",
    "sant ravidas nagar": "MIRZAPUR",
    "bhadohi": "MIRZAPUR",
    "sonbhadra": "MIRZAPUR",

    # Moradabad
    "amroha": "MORADABAD",
    "bijnor": "MORADABAD",
    "moradabad": "MORADABAD",
    "rampur": "MORADABAD",
    "sambhal": "MORADABAD",

    # Prayagraj
    "prayagraj": "PRAYAGRAJ",
    "kaushambi": "PRAYAGRAJ",
    "fatehpur": "PRAYAGRAJ",
    "pratapgarh": "PRAYAGRAJ",

    # Saharanpur
    "muzaffarnagar": "SAHARANPUR",
    "saharanpur": "SAHARANPUR",
    "shamli": "SAHARANPUR",

    # Varanasi
    "chandauli": "VARANASI",
    "ghazipur": "VARANASI",
    "jaunpur": "VARANASI",
    "varanasi": "VARANASI",
}


DIVISION_NAMES = {
    "AGRA": "Agra",
    "ALIGARH": "Aligarh",
    "AYODHYA": "Ayodhya",
    "AZAMGARH": "Azamgarh",
    "BAREILLY": "Bareilly",
    "BASTI": "Basti",
    "CHITRAKOOT": "Chitrakoot",
    "DEVIPATAN": "Devipatan",
    "GORAKHPUR": "Gorakhpur",
    "JHANSI": "Jhansi",
    "KANPUR": "Kanpur",
    "LUCKNOW": "Lucknow",
    "MEERUT": "Meerut",
    "MIRZAPUR": "Mirzapur",
    "MORADABAD": "Moradabad",
    "PRAYAGRAJ": "Prayagraj",
    "SAHARANPUR": "Saharanpur",
    "VARANASI": "Varanasi",
}


def main():
    with DISTRICTS.open(
        newline="",
        encoding="utf-8-sig",
    ) as f:
        districts = list(csv.DictReader(f))

    resolved = []
    unresolved = []

    for district in districts:
        code = district["district_code"].strip()
        name = district["district_name"].strip()

        division_code = DIVISION_MAP.get(
            norm(name)
        )

        if division_code is None:
            unresolved.append(
                district
            )
            continue

        resolved.append({
            "district_code": code,
            "district_name": name,
            "division_code": division_code,
            "division_name": DIVISION_NAMES[
                division_code
            ],
        })

    DIVISIONS.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with DIVISIONS.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "division_code",
                "division_name",
            ],
        )
        writer.writeheader()

        for code, name in DIVISION_NAMES.items():
            writer.writerow({
                "division_code": code,
                "division_name": name,
            })

    with DISTRICT_DIVISIONS.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "district_code",
                "district_name",
                "division_code",
                "division_name",
            ],
        )
        writer.writeheader()
        writer.writerows(resolved)

    print("DIVISIONS:", len(DIVISION_NAMES))
    print("DISTRICTS RESOLVED:", len(resolved))
    print("DISTRICTS UNRESOLVED:", len(unresolved))

    if unresolved:
        print("\nUNRESOLVED:")
        for row in unresolved:
            print(
                row["district_code"],
                "|",
                row["district_name"],
            )


if __name__ == "__main__":
    main()
