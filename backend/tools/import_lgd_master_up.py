from __future__ import annotations

import argparse
import csv
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database.models.master.division import Division
from database.models.master.district import District
from database.models.master.tehsil import Tehsil
from database.models.master.block import Block
from database.models.master.gram_panchayat import GramPanchayat
from database.models.master.village import Village


BASE = Path("data/master/up")

FILES = {
    "divisions": BASE / "divisions.csv",
    "district_divisions": BASE / "district_divisions.csv",
    "districts": BASE / "districts.csv",
    "tehsils": BASE / "tehsils.csv",
    "blocks": BASE / "blocks.csv",
    "gram_panchayats": BASE / "gram_panchayats.csv",
    "villages": BASE / "villages.csv",
    "gp_block_mapping": Path(
        "data/source/up/reconciliation/"
        "final_gp_block_mapping.csv"
    ),
    "village_gp_mapping": BASE
    / "village_gram_panchayat_mapping.csv",
}


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise FileNotFoundError(path)

    with path.open(
        newline="",
        encoding="utf-8-sig",
    ) as f:
        return list(csv.DictReader(f))


def clean(value: object) -> str:
    if value is None:
        return ""
    return str(value).strip()


def require_unique(
    rows: list[dict[str, str]],
    key: str,
    name: str,
) -> None:
    values = [clean(row.get(key)) for row in rows]

    if any(not value for value in values):
        raise ValueError(
            f"{name}: empty {key} found"
        )

    duplicates = len(values) - len(set(values))

    if duplicates:
        raise ValueError(
            f"{name}: {duplicates} duplicate {key} values"
        )


def load_data() -> dict[str, list[dict[str, str]]]:
    data = {
        name: read_csv(path)
        for name, path in FILES.items()
    }

    require_unique(
        data["divisions"],
        "division_code",
        "divisions",
    )
    require_unique(
        data["districts"],
        "district_code",
        "districts",
    )
    require_unique(
        data["tehsils"],
        "tehsil_code",
        "tehsils",
    )
    require_unique(
        data["blocks"],
        "block_code",
        "blocks",
    )
    require_unique(
        data["gram_panchayats"],
        "gram_panchayat_code",
        "gram_panchayats",
    )
    require_unique(
        data["villages"],
        "village_code",
        "villages",
    )
    require_unique(
        data["gp_block_mapping"],
        "gram_panchayat_code",
        "gp_block_mapping",
    )

    return data


def validate_data(
    data: dict[str, list[dict[str, str]]],
) -> dict[str, object]:
    division_codes = {
        clean(row["division_code"])
        for row in data["divisions"]
    }

    district_codes = {
        clean(row["district_code"])
        for row in data["districts"]
    }

    tehsil_codes = {
        clean(row["tehsil_code"])
        for row in data["tehsils"]
    }

    block_codes = {
        clean(row["block_code"])
        for row in data["blocks"]
    }

    gp_codes = {
        clean(row["gram_panchayat_code"])
        for row in data["gram_panchayats"]
    }

    village_codes = {
        clean(row["village_code"])
        for row in data["villages"]
    }

    district_division = {
        clean(row["district_code"]):
            clean(row["division_code"])
        for row in data["district_divisions"]
    }

    if set(district_division) != district_codes:
        raise ValueError(
            "District → Division coverage mismatch"
        )

    if any(
        division not in division_codes
        for division in district_division.values()
    ):
        raise ValueError(
            "District → Division contains unknown division"
        )

    if any(
        clean(row["district_code"])
        not in district_codes
        for row in data["tehsils"]
    ):
        raise ValueError(
            "Tehsil references unknown district"
        )

    if any(
        clean(row["district_code"])
        not in district_codes
        for row in data["blocks"]
    ):
        raise ValueError(
            "Block references unknown district"
        )

    if any(
        clean(row["district_code"])
        not in district_codes
        for row in data["gram_panchayats"]
    ):
        raise ValueError(
            "Gram Panchayat references unknown district"
        )

    invalid_gp_block = [
        row
        for row in data["gp_block_mapping"]
        if (
            clean(row["gram_panchayat_code"])
            not in gp_codes
            or clean(row["block_code"])
            not in block_codes
        )
    ]

    if invalid_gp_block:
        raise ValueError(
            f"Invalid GP → Block mappings: "
            f"{len(invalid_gp_block)}"
        )

    village_gp_map = {
        clean(row["village_code"]):
            clean(row["gram_panchayat_code"])
        for row in data["village_gp_mapping"]
    }

    invalid_village_gp = [
        row
        for row in data["village_gp_mapping"]
        if (
            clean(row["village_code"])
            not in village_codes
            or clean(row["gram_panchayat_code"])
            not in gp_codes
        )
    ]

    if invalid_village_gp:
        raise ValueError(
            f"Invalid Village → GP mappings: "
            f"{len(invalid_village_gp)}"
        )

    return {
        "division_codes": division_codes,
        "district_codes": district_codes,
        "tehsil_codes": tehsil_codes,
        "block_codes": block_codes,
        "gp_codes": gp_codes,
        "village_codes": village_codes,
        "district_division": district_division,
        "village_gp_map": village_gp_map,
    }


def dry_run(
    data: dict[str, list[dict[str, str]]],
    validation: dict[str, object],
) -> None:
    village_gp_map = validation["village_gp_map"]

    mapped_villages = len(village_gp_map)
    unmapped_villages = (
        len(data["villages"])
        - mapped_villages
    )

    print(
        "========== LGD MASTER IMPORT =========="
    )
    print("DIVISIONS:", len(data["divisions"]))
    print("DISTRICTS:", len(data["districts"]))
    print("TEHSILS:", len(data["tehsils"]))
    print("BLOCKS:", len(data["blocks"]))
    print(
        "GRAM PANCHAYATS:",
        len(data["gram_panchayats"]),
    )
    print("VILLAGES:", len(data["villages"]))
    print(
        "VALID GP → BLOCK:",
        len(data["gp_block_mapping"]),
    )
    print(
        "VALID VILLAGE → GP:",
        mapped_villages,
    )
    print(
        "UNMAPPED VILLAGES:",
        unmapped_villages,
    )
    print()
    print(
        "BLOCK → TEHSIL: "
        "SKIPPED — authoritative "
        "crosswalk unavailable"
    )
    print()
    print("DRY-RUN: no database changes made.")


def get_or_create_division(
    db,
    row,
    state_id: int,
    stats: dict[str, int],
):
    code = clean(row["division_code"])
    name = clean(row["division_name"])

    obj = (
        db.query(Division)
        .filter(
            Division.division_code == code
        )
        .first()
    )

    if obj is None:
        obj = Division(
            division_code=code,
            division_name=name,
            state_id=state_id,
        )
        db.add(obj)
        db.flush()
        stats["divisions_inserted"] += 1
    else:
        stats["divisions_reused"] += 1

        if obj.division_name != name:
            obj.division_name = name

        if obj.state_id != state_id:
            obj.state_id = state_id
            stats["divisions_updated"] += 1

    return obj


def get_or_create_district(
    db,
    row,
    division_id: int,
    stats: dict[str, int],
):
    code = clean(row["district_code"])
    name = clean(row["district_name"])

    obj = (
        db.query(District)
        .filter(
            District.district_code == code
        )
        .first()
    )

    if obj is None:
        obj = District(
            district_code=code,
            district_name=name,
            division_id=division_id,
        )
        db.add(obj)
        db.flush()
        stats["districts_inserted"] += 1
    else:
        stats["districts_reused"] += 1

        if obj.district_name != name:
            obj.district_name = name
            stats["districts_updated"] += 1

        if obj.division_id != division_id:
            obj.division_id = division_id
            stats["districts_updated"] += 1

    return obj


def get_or_create_tehsil(
    db,
    row,
    district_id: int,
    stats: dict[str, int],
):
    code = clean(row["tehsil_code"])
    name = clean(row["tehsil_name"])

    obj = (
        db.query(Tehsil)
        .filter(
            Tehsil.tehsil_code == code
        )
        .first()
    )

    if obj is None:
        obj = Tehsil(
            tehsil_code=code,
            tehsil_name=name,
            district_id=district_id,
        )
        db.add(obj)
        db.flush()
        stats["tehsils_inserted"] += 1
    else:
        stats["tehsils_reused"] += 1

        if obj.tehsil_name != name:
            obj.tehsil_name = name
            stats["tehsils_updated"] += 1

        if obj.district_id != district_id:
            obj.district_id = district_id
            stats["tehsils_updated"] += 1

    return obj


def get_or_create_block(
    db,
    row,
    district_id,
    stats,
):
    code = clean(row["block_code"])
    name = clean(row["block_name"])

    obj = (
        db.query(Block)
        .filter(
            Block.block_code == code
        )
        .first()
    )

    if obj is None:
        obj = Block(
            block_code=code,
            block_name=name,
            district_id=district_id,
        )
        db.add(obj)
        db.flush()
        stats["blocks_inserted"] += 1
    else:
        stats["blocks_reused"] += 1

        changed = False

        if obj.block_name != name:
            obj.block_name = name
            changed = True

        if obj.district_id != district_id:
            obj.district_id = district_id
            changed = True

        if changed:
            stats["blocks_updated"] += 1

    return obj


def get_or_create_gp(
    db,
    row,
    stats: dict[str, int],
):
    code = clean(
        row["gram_panchayat_code"]
    )
    name = clean(
        row["gram_panchayat_name"]
    )

    obj = (
        db.query(GramPanchayat)
        .filter(
            GramPanchayat
            .gram_panchayat_code == code
        )
        .first()
    )

    if obj is None:
        obj = GramPanchayat(
            gram_panchayat_code=code,
            gram_panchayat_name=name,
            block_id=None,
        )
        db.add(obj)
        db.flush()
        stats["gps_inserted"] += 1
    else:
        stats["gps_reused"] += 1

        if obj.gram_panchayat_name != name:
            obj.gram_panchayat_name = name
            stats["gps_updated"] += 1

    return obj


def get_or_create_village(
    db,
    row,
    stats: dict[str, int],
):
    code = clean(row["village_code"])
    name = clean(row["village_name"])

    obj = (
        db.query(Village)
        .filter(
            Village.village_code == code
        )
        .first()
    )

    if obj is None:
        obj = Village(
            village_code=code,
            village_name=name,
            gram_panchayat_id=None,
        )
        db.add(obj)
        db.flush()
        stats["villages_inserted"] += 1
    else:
        stats["villages_reused"] += 1

        if obj.village_name != name:
            obj.village_name = name
            stats["villages_updated"] += 1

    return obj


def apply_import(
    data: dict[str, list[dict[str, str]]],
    validation: dict[str, object],
    db_path: str,
):
    db_file = Path(db_path).expanduser().resolve()

    if not db_file.exists():
        raise FileNotFoundError(
            f"Database file not found: {db_file}"
        )

    engine = create_engine(
        f"sqlite:///{db_file}",
        echo=True,
    )

    Session = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine,
    )

    db = Session()

    stats = {
        "divisions_inserted": 0,
        "divisions_reused": 0,
        "divisions_updated": 0,
        "districts_inserted": 0,
        "districts_reused": 0,
        "districts_updated": 0,
        "tehsils_inserted": 0,
        "tehsils_reused": 0,
        "tehsils_updated": 0,
        "blocks_inserted": 0,
        "blocks_reused": 0,
        "blocks_updated": 0,
        "gps_inserted": 0,
        "gps_reused": 0,
        "gps_updated": 0,
        "villages_inserted": 0,
        "villages_reused": 0,
        "villages_updated": 0,
        "gp_block_updated": 0,
        "village_gp_updated": 0,
    }

    try:
        print(
            "========== APPLYING LGD MASTER =========="
        )

        state = (
            db.query(
                __import__(
                    "database.models.master.state",
                    fromlist=["State"],
                ).State
            )
            .filter_by(
                state_code="UP"
            )
            .first()
        )

        if state is None:
            raise RuntimeError(
                "UP state not found."
            )

        division_by_code = {}

        for row in data["divisions"]:
            division = get_or_create_division(
                db,
                row,
                state.id,
                stats,
            )
            division_by_code[
                clean(row["division_code"])
            ] = division

        district_division = validation[
            "district_division"
        ]

        district_by_code = {}

        for row in data["districts"]:
            division = division_by_code[
                district_division[
                    clean(row["district_code"])
                ]
            ]

            district = get_or_create_district(
                db,
                row,
                division.id,
                stats,
            )

            district_by_code[
                clean(row["district_code"])
            ] = district

        for row in data["tehsils"]:
            district = district_by_code[
                clean(row["district_code"])
            ]

            get_or_create_tehsil(
                db,
                row,
                district.id,
                stats,
            )

        block_by_code = {}

        for row in data["blocks"]:
            district = district_by_code[
                clean(row["district_code"])
            ]

            block = get_or_create_block(
                db,
                row,
                district.id,
                stats,
            )

            block_by_code[
                clean(row["block_code"])
            ] = block

        gp_by_code = {}

        for row in data["gram_panchayats"]:
            gp = get_or_create_gp(
                db,
                row,
                stats,
            )

            gp_by_code[
                clean(
                    row["gram_panchayat_code"]
                )
            ] = gp

        village_by_code = {}

        for row in data["villages"]:
            village = get_or_create_village(
                db,
                row,
                stats,
            )

            village_by_code[
                clean(row["village_code"])
            ] = village

        # ------------------------------------------
        # GP → Block
        # ------------------------------------------

        for row in data["gp_block_mapping"]:
            gp = gp_by_code[
                clean(
                    row["gram_panchayat_code"]
                )
            ]

            block = block_by_code[
                clean(row["block_code"])
            ]

            if gp.block_id != block.id:
                gp.block_id = block.id
                stats["gp_block_updated"] += 1

        # ------------------------------------------
        # Village → GP
        # ------------------------------------------

        village_gp_map = validation[
            "village_gp_map"
        ]

        for village_code, gp_code in (
            village_gp_map.items()
        ):
            village = village_by_code[
                village_code
            ]

            gp = gp_by_code[
                gp_code
            ]

            if (
                village.gram_panchayat_id
                != gp.id
            ):
                village.gram_panchayat_id = gp.id
                stats[
                    "village_gp_updated"
                ] += 1

        db.flush()
        db.commit()

        print(
            "\n========== IMPORT COMPLETE =========="
        )

        for key in sorted(stats):
            print(
                f"{key:25} {stats[key]}"
            )

        print()
        print(
            "Block → Tehsil relations:"
            " NOT modified"
        )

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--apply",
        action="store_true",
        help="Apply validated data to DB",
    )

    parser.add_argument(
        "--db",
        help=(
            "SQLite database file for --apply. "
            "Required when applying."
        ),
    )

    args = parser.parse_args()

    if args.apply and not args.db:
        parser.error(
            "--db is required with --apply"
        )

    data = load_data()
    validation = validate_data(data)

    if not args.apply:
        dry_run(
            data,
            validation,
        )
        return

    apply_import(
        data,
        validation,
        args.db,
    )


if __name__ == "__main__":
    main()
