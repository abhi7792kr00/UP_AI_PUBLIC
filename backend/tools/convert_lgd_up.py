from __future__ import annotations

import csv
import re
import xml.etree.ElementTree as ET
from collections import defaultdict
from pathlib import Path


SOURCE = Path("data/source/lgd/up/extracted")
OUTPUT = Path("data/master/up")

NS = {
    "ss": "urn:schemas-microsoft-com:office:spreadsheet"
}


DISTRICT_GLOB = "districtofSpecificState*.xls"
TEHSIL_GLOB = "subDistrictofSpecificState*.xls"
BLOCK_GLOB = "blockofspecificState*.xls"
PRI_GLOB = "priLbSpecificState*.xls"
ULB_GLOB = "ulbSpecificState*.xls"
WARD_GLOB = "uLBWardforState*.xls"
VILLAGE_GLOB = "villageofSpecificState*.xls"
MAPPING_GLOB = "villageGramPanchayatMapping*.xls"


def clean(value: str | None) -> str:
    if value is None:
        return ""

    value = value.replace("\xa0", " ")
    return re.sub(r"\s+", " ", value).strip()


def find_file(pattern: str) -> Path:
    files = sorted(SOURCE.glob(pattern))

    if not files:
        raise FileNotFoundError(
            f"LGD source file not found: {pattern}"
        )

    return files[0]


def row_values(row):
    """
    Read an Excel 2003 XML row while honoring ss:Index.

    LGD exports may omit empty cells and use ss:Index to
    indicate the real column position. Without handling that,
    all later columns shift left and mappings become wrong.
    """
    values = []
    next_index = 1

    for cell in row.findall("ss:Cell", NS):
        index_attr = cell.attrib.get(
            f"{{{NS['ss']}}}Index"
        )

        if index_attr:
            next_index = int(index_attr)

        while len(values) < next_index - 1:
            values.append("")

        data = cell.find("ss:Data", NS)

        value = clean(
            None
            if data is None
            else data.text
        )

        values.append(value)

        next_index += 1

    return values


def iter_rows(
    path: Path,
    sheet_names: set[str] | None = None,
):
    """
    Stream rows from one or more Excel 2003 XML worksheets.

    sheet_names=None:
        read all worksheets.

    sheet_names={"Report"}:
        read only Report.

    sheet_names={"Report", "Report1"}:
        read both sheets.
    """

    context = ET.iterparse(
        path,
        events=("start", "end"),
    )

    active = False
    table_depth = 0

    for event, elem in context:
        tag = elem.tag.split("}")[-1]

        if event == "start":

            if tag == "Worksheet":
                name = elem.attrib.get(
                    f"{{{NS['ss']}}}Name",
                    "",
                )

                active = (
                    sheet_names is None
                    or name in sheet_names
                )

            elif (
                tag == "Table"
                and active
            ):
                table_depth += 1

            continue

        # END event

        if (
            active
            and tag == "Row"
            and table_depth > 0
        ):
            yield row_values(elem)
            elem.clear()

        elif (
            active
            and tag == "Table"
            and table_depth > 0
        ):
            table_depth -= 1

        elif tag == "Worksheet":
            active = False
            elem.clear()

def write_csv(
    path: Path,
    fieldnames: list[str],
    rows,
):
    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    count = 0

    with path.open(
        "w",
        newline="",
        encoding="utf-8-sig",
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames,
        )

        writer.writeheader()

        for row in rows:
            writer.writerow(row)
            count += 1

    print(
        f"✓ {path.name}: {count} rows"
    )

    return count


# ============================================================
# DISTRICTS
# ============================================================

def convert_districts():
    path = find_file(DISTRICT_GLOB)

    output_rows = []

    for values in iter_rows(
        path,
        sheet_names={"Report"},
    ):
        if len(values) < 4:
            continue

        # LGD observed structure:
        # [S.No, District Code, ..., District Name, ...]
        code = clean(values[1])
        name = clean(values[3])

        if not code.isdigit():
            continue

        if not name:
            continue

        output_rows.append(
            {
                "district_code": code,
                "district_name": name,
            }
        )

    # Deduplicate by LGD code.
    unique = {}

    for row in output_rows:
        unique[row["district_code"]] = row

    rows = [
        unique[key]
        for key in sorted(
            unique,
            key=lambda x: int(x),
        )
    ]

    return write_csv(
        OUTPUT / "districts.csv",
        [
            "district_code",
            "district_name",
        ],
        rows,
    )


# ============================================================
# TEHSILS / SUBDISTRICTS
# ============================================================

def convert_tehsils():
    path = find_file(TEHSIL_GLOB)

    rows = []

    for values in iter_rows(
        path,
        sheet_names={"Report"},
    ):
        if len(values) < 6:
            continue

        # Observed:
        # 0 S.No
        # 1 District Code
        # 2 District Name
        # 3 Subdistrict Code
        # 4 ...
        # 5 Subdistrict Name

        district_code = clean(values[1])
        tehsil_code = clean(values[3])
        tehsil_name = clean(values[5])

        if not district_code.isdigit():
            continue

        if not tehsil_code:
            continue

        if not tehsil_name:
            continue

        rows.append(
            {
                "tehsil_code": tehsil_code,
                "tehsil_name": tehsil_name,
                "district_code": district_code,
            }
        )

    unique = {}

    for row in rows:
        unique[row["tehsil_code"]] = row

    rows = list(unique.values())

    rows.sort(
        key=lambda r: (
            int(r["district_code"]),
            r["tehsil_name"],
        )
    )

    return write_csv(
        OUTPUT / "tehsils.csv",
        [
            "tehsil_code",
            "tehsil_name",
            "district_code",
        ],
        rows,
    )


# ============================================================
# BLOCKS
# ============================================================

def convert_blocks():
    path = find_file(BLOCK_GLOB)

    rows = []

    for values in iter_rows(
        path,
        sheet_names={"Report"},
    ):
        if len(values) < 6:
            continue

        # Observed:
        # 0 S.No
        # 1 District Code
        # 2 District Name
        # 3 Block Code
        # 4 ...
        # 5 Block Name

        district_code = clean(values[1])
        block_code = clean(values[3])
        block_name = clean(values[5])

        if not district_code.isdigit():
            continue

        if not block_code:
            continue

        if not block_name:
            continue

        rows.append(
            {
                "block_code": block_code,
                "block_name": block_name,
                "district_code": district_code,
            }
        )

    unique = {}

    for row in rows:
        unique[row["block_code"]] = row

    rows = list(unique.values())

    rows.sort(
        key=lambda r: (
            int(r["district_code"]),
            r["block_name"],
        )
    )

    return write_csv(
        OUTPUT / "blocks.csv",
        [
            "block_code",
            "block_name",
            "district_code",
        ],
        rows,
    )


# ============================================================
# PRI LOCAL BODIES
# ============================================================

def convert_pri():
    path = find_file(PRI_GLOB)

    rows = []

    for values in iter_rows(
        path,
        sheet_names={"Report"},
    ):
        if len(values) < 8:
            continue

        # Observed:
        # 0 S.No
        # 1 Localbody Type Code
        # 2 Localbody Type Name
        # 3 Localbody Code
        # 4 District Code
        # 5 Localbody Name
        # 6 English Name
        # 7 Parent Localbody Code

        body_type_code = clean(values[1])
        body_type = clean(values[2])
        body_code = clean(values[3])
        district_code = clean(values[4])
        body_name = clean(values[5])
        parent_code = clean(values[7])

        if body_type not in {
            "Zilla Panchayat",
            "Kshetra Panchayat",
            "Gram Panchayat",
        }:
            continue

        if not body_code:
            continue

        rows.append(
            {
                "local_body_type_code": body_type_code,
                "local_body_type": body_type,
                "local_body_code": body_code,
                "local_body_name": body_name,
                "district_code": district_code,
                "parent_local_body_code": parent_code,
            }
        )

    unique = {}

    for row in rows:
        unique[
            (
                row["local_body_type_code"],
                row["local_body_code"],
            )
        ] = row

    rows = list(unique.values())

    rows.sort(
        key=lambda r: (
            int(r["district_code"])
            if r["district_code"].isdigit()
            else 9999,
            r["local_body_type"],
            r["local_body_name"],
        )
    )

    return write_csv(
        OUTPUT / "pri_local_bodies.csv",
        [
            "local_body_type_code",
            "local_body_type",
            "local_body_code",
            "local_body_name",
            "district_code",
            "parent_local_body_code",
        ],
        rows,
    )


# ============================================================
# GRAM PANCHAYATS
# ============================================================

def convert_gram_panchayats():
    path = find_file(PRI_GLOB)

    rows = []

    for values in iter_rows(
        path,
        sheet_names={"Report"},
    ):
        if len(values) < 8:
            continue

        if clean(values[2]) != "Gram Panchayat":
            continue

        gp_code = clean(values[3])
        district_code = clean(values[4])
        gp_name = clean(values[5])
        parent_kp_code = clean(values[7])

        if not gp_code:
            continue

        rows.append(
            {
                "gram_panchayat_code": gp_code,
                "gram_panchayat_name": gp_name,
                "district_code": district_code,
                "parent_kp_code": parent_kp_code,
            }
        )

    unique = {}

    for row in rows:
        unique[
            row["gram_panchayat_code"]
        ] = row

    rows = list(unique.values())

    rows.sort(
        key=lambda r: (
            int(r["district_code"])
            if r["district_code"].isdigit()
            else 9999,
            r["gram_panchayat_name"],
        )
    )

    return write_csv(
        OUTPUT / "gram_panchayats.csv",
        [
            "gram_panchayat_code",
            "gram_panchayat_name",
            "district_code",
            "parent_kp_code",
        ],
        rows,
    )


# ============================================================
# VILLAGES
# ============================================================

def convert_villages():
    path = find_file(VILLAGE_GLOB)

    rows = []

    for values in iter_rows(
        path,
        sheet_names={"Report", "Report1"},
    ):
        if len(values) < 13:
            continue

        # Observed village structure:
        # 1 District Code
        # 2 District Name
        # 3 Subdistrict Code
        # 4 Subdistrict Name
        # 5 Village Code
        # 7 Village Name
        # 10 Census / other code
        # 11 LGD Village Code

        district_code = clean(values[1])
        tehsil_code = clean(values[3])
        village_code = clean(values[5])
        village_name = clean(values[7])

        if not village_code:
            continue

        if not village_name:
            continue

        rows.append(
            {
                "village_code": village_code,
                "village_name": village_name,
                "district_code": district_code,
                "tehsil_code": tehsil_code,
            }
        )

    unique = {}

    for row in rows:
        unique[
            row["village_code"]
        ] = row

    rows = list(unique.values())

    rows.sort(
        key=lambda r: (
            int(r["district_code"])
            if r["district_code"].isdigit()
            else 9999,
            r["village_name"],
        )
    )

    return write_csv(
        OUTPUT / "villages.csv",
        [
            "village_code",
            "village_name",
            "district_code",
            "tehsil_code",
        ],
        rows,
    )


# ============================================================
# VILLAGE → GRAM PANCHAYAT MAPPING
# ============================================================

def convert_village_gp_mapping():
    path = find_file(MAPPING_GLOB)

    rows = []

    for values in iter_rows(
        path,
        sheet_names={"Report", "Report1"},
    ):
        if len(values) < 15:
            continue

        # Observed mapping:
        # 1 District Code
        # 2 District Name
        # 5 Subdistrict Code
        # 6 Subdistrict Name
        # 9 Village Code
        # 10 Village Name
        # 13 Gram Panchayat Code
        # 14 Gram Panchayat Name

        district_code = clean(values[1])
        tehsil_code = clean(values[5])
        village_code = clean(values[9])
        village_name = clean(values[10])
        gp_code = clean(values[13])
        gp_name = clean(values[14])

        if not village_code:
            continue

        if not gp_code:
            continue

        rows.append(
            {
                "district_code": district_code,
                "tehsil_code": tehsil_code,
                "village_code": village_code,
                "village_name": village_name,
                "gram_panchayat_code": gp_code,
                "gram_panchayat_name": gp_name,
            }
        )

    unique = {}

    for row in rows:
        unique[
            (
                row["village_code"],
                row["gram_panchayat_code"],
            )
        ] = row

    rows = list(unique.values())

    rows.sort(
        key=lambda r: (
            int(r["district_code"])
            if r["district_code"].isdigit()
            else 9999,
            r["village_name"],
        )
    )

    return write_csv(
        OUTPUT / "village_gram_panchayat_mapping.csv",
        [
            "district_code",
            "tehsil_code",
            "village_code",
            "village_name",
            "gram_panchayat_code",
            "gram_panchayat_name",
        ],
        rows,
    )


# ============================================================
# URBAN LOCAL BODIES
# ============================================================

def convert_ulbs():
    path = find_file(ULB_GLOB)

    rows = []

    for values in iter_rows(
        path,
        sheet_names={"Report"},
    ):
        if len(values) < 6:
            continue

        local_body_type_code = clean(values[1])
        local_body_type = clean(values[2])
        local_body_code = clean(values[3])
        local_body_name = clean(values[5])

        if not local_body_code.isdigit():
            continue

        if not local_body_name:
            continue

        rows.append(
            {
                "local_body_type_code":
                    local_body_type_code,
                "local_body_type":
                    local_body_type,
                "local_body_code":
                    local_body_code,
                "local_body_name":
                    local_body_name,
            }
        )

    unique = {}

    for row in rows:
        unique[
            row["local_body_code"]
        ] = row

    rows = list(unique.values())

    rows.sort(
        key=lambda r: (
            r["local_body_type"],
            r["local_body_name"],
        )
    )

    return write_csv(
        OUTPUT / "municipal_bodies.csv",
        [
            "local_body_type_code",
            "local_body_type",
            "local_body_code",
            "local_body_name",
        ],
        rows,
    )

def convert_wards():
    path = find_file(WARD_GLOB)

    rows = []

    for values in iter_rows(
        path,
        sheet_names={"Report"},
    ):
        if len(values) < 6:
            continue

        body_code = clean(values[1])
        ward_code = clean(values[3])
        ward_number = clean(values[4])
        ward_name = clean(values[5])

        if not body_code:
            continue

        if not ward_code:
            continue

        rows.append(
            {
                "municipal_body_code": body_code,
                "ward_code": ward_code,
                "ward_number": ward_number,
                "ward_name": ward_name,
            }
        )

    unique = {}

    for row in rows:
        unique[
            row["ward_code"]
        ] = row

    rows = list(unique.values())

    rows.sort(
        key=lambda r: (
            r["municipal_body_code"],
            r["ward_number"],
        )
    )

    return write_csv(
        OUTPUT / "wards.csv",
        [
            "municipal_body_code",
            "ward_code",
            "ward_number",
            "ward_name",
        ],
        rows,
    )


# ============================================================
# VALIDATION
# ============================================================

def count_csv(name: str):
    path = OUTPUT / name

    with path.open(
        newline="",
        encoding="utf-8-sig",
    ) as file:
        return sum(
            1
            for _ in csv.DictReader(file)
        )


def validate_outputs():
    print("\n========== VALIDATION ==========")

    expected = {
        "districts.csv": 75,
        "tehsils.csv": 350,
        "blocks.csv": 826,
        "gram_panchayats.csv": 57694,
        "villages.csv": 44746,
        "village_gram_panchayat_mapping.csv": 44747,
    }

    for filename, expected_count in expected.items():
        actual = count_csv(filename)

        status = (
            "OK"
            if actual == expected_count
            else "CHECK"
        )

        print(
            f"{filename}: "
            f"{actual} "
            f"(expected {expected_count}) "
            f"[{status}]"
        )

    # PRI type counts
    pri_path = OUTPUT / "pri_local_bodies.csv"

    counts = defaultdict(int)

    with pri_path.open(
        newline="",
        encoding="utf-8-sig",
    ) as file:
        for row in csv.DictReader(file):
            counts[
                row["local_body_type"]
            ] += 1

    print("\nPRI TYPES:")

    for key in sorted(counts):
        print(
            f"{key}: {counts[key]}"
        )


# ============================================================
# MAIN
# ============================================================

def main():
    print(
        "========== LGD UP NORMALIZER =========="
    )

    OUTPUT.mkdir(
        parents=True,
        exist_ok=True,
    )

    convert_districts()
    convert_tehsils()
    convert_blocks()
    convert_pri()
    convert_gram_panchayats()
    convert_villages()
    convert_village_gp_mapping()

    # Urban files are normalized separately.
    convert_ulbs()
    convert_wards()

    validate_outputs()

    print(
        "\n✅ LGD normalization complete."
    )

    print(
        "\nNOTE:"
    )

    print(
        "Block -> Tehsil is intentionally NOT "
        "invented from LGD files."
    )

    print(
        "Gram Panchayat -> Block is also NOT "
        "invented from Kshetra Panchayat codes."
    )


if __name__ == "__main__":
    main()
