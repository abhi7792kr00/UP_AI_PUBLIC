from pathlib import Path

import pandas as pd

from sqlalchemy.orm import Session

from core.database.session import SessionLocal

from database.models.master.state import State
from database.models.master.division import Division
from database.models.master.district import District
from database.models.master.tehsil import Tehsil
from database.models.master.block import Block
from database.models.master.gram_panchayat import GramPanchayat
from database.models.master.village import Village
from database.models.master.municipal_body import MunicipalBody
from database.models.master.ward import Ward
from database.models.master.locality import Locality


DATA_DIR = Path("data/master/up")


def read_csv(name: str):
    path = DATA_DIR / name

    if not path.exists():
        raise FileNotFoundError(
            f"Required master-data file missing: {path}"
        )

    df = pd.read_csv(path)

    if df.empty:
        raise ValueError(
            f"Required master-data file is empty: {path}"
        )

    print(
        f"✓ Loaded {len(df)} rows: {path}"
    )

    return df


def seed_divisions(
    db: Session,
    df,
    state: State,
):
    if df is None:
        return

    for row in df.to_dict("records"):
        code = str(row["division_code"]).strip()
        name = str(row["division_name"]).strip()

        if not code or not name:
            continue

        exists = (
            db.query(Division)
            .filter(
                Division.division_code == code
            )
            .first()
        )

        if exists:
            continue

        db.add(
            Division(
                division_name=name,
                division_code=code,
                state_id=state.id,
            )
        )


def seed_districts(
    db: Session,
    df,
):
    if df is None:
        return

    for row in df.to_dict("records"):
        code = str(row["district_code"]).strip()
        name = str(row["district_name"]).strip()
        division_code = str(
            row["division_code"]
        ).strip()

        division = (
            db.query(Division)
            .filter(
                Division.division_code
                == division_code
            )
            .first()
        )

        if division is None:
            raise ValueError(
                f"Division not found: {division_code}"
            )

        exists = (
            db.query(District)
            .filter(
                District.district_code == code
            )
            .first()
        )

        if exists:
            continue

        db.add(
            District(
                district_name=name,
                district_code=code,
                division_id=division.id,
            )
        )


def seed_tehsils(
    db: Session,
    df,
):
    if df is None:
        return

    for row in df.to_dict("records"):
        code = str(row["tehsil_code"]).strip()
        name = str(row["tehsil_name"]).strip()
        district_code = str(
            row["district_code"]
        ).strip()

        district = (
            db.query(District)
            .filter(
                District.district_code
                == district_code
            )
            .first()
        )

        if district is None:
            raise ValueError(
                f"District not found: {district_code}"
            )

        exists = (
            db.query(Tehsil)
            .filter(
                Tehsil.tehsil_code == code
            )
            .first()
        )

        if exists:
            continue

        db.add(
            Tehsil(
                tehsil_name=name,
                tehsil_code=code,
                district_id=district.id,
            )
        )


def seed_blocks(
    db: Session,
    df,
):
    if df is None:
        return

    for row in df.to_dict("records"):
        code = str(
            row["block_code"]
        ).strip()

        name = str(
            row["block_name"]
        ).strip()

        district_code = str(
            row["district_code"]
        ).strip()

        district = (
            db.query(District)
            .filter(
                District.district_code
                == district_code
            )
            .first()
        )

        if district is None:
            raise ValueError(
                f"District not found: "
                f"{district_code}"
            )

        exists = (
            db.query(Block)
            .filter(
                Block.block_code == code
            )
            .first()
        )

        if exists:
            continue

        db.add(
            Block(
                block_name=name,
                block_code=code,
                district_id=district.id,
            )
        )

def seed_gram_panchayats(
    db: Session,
    df,
):
    if df is None:
        return

    for row in df.to_dict("records"):
        code = str(
            row["gram_panchayat_code"]
        ).strip()

        name = str(
            row["gram_panchayat_name"]
        ).strip()

        exists = (
            db.query(GramPanchayat)
            .filter(
                GramPanchayat.gram_panchayat_code
                == code
            )
            .first()
        )

        if exists:
            continue

        db.add(
            GramPanchayat(
                gram_panchayat_name=name,
                gram_panchayat_code=code,
                block_id=None,
            )
        )

def seed_villages(
    db: Session,
    df,
):
    if df is None:
        return

    for row in df.to_dict("records"):
        code = str(
            row["village_code"]
        ).strip()

        name = str(
            row["village_name"]
        ).strip()

        # Skip header-like / invalid village rows.
        if (
            not code
            or not code.isdigit()
            or code.lower()
            == "village code"
        ):
            continue

        if (
            not name
            or name.lower()
            == "village name"
        ):
            continue

        exists = (
            db.query(Village)
            .filter(
                Village.village_code == code
            )
            .first()
        )

        if exists:
            continue

        db.add(
            Village(
                village_name=name,
                village_code=code,
                gram_panchayat_id=None,
            )
        )


def seed_municipal_bodies(
    db: Session,
    ulb_df,
    district_map_df,
):
    if ulb_df is None:
        return

    if district_map_df is None:
        raise ValueError(
            "Municipal body district mapping is required."
        )

    district_by_body_code = {
        str(row["local_body_code"]).strip():
            str(row["district_code"]).strip()
        for row in district_map_df.to_dict("records")
    }

    type_map = {
        "4": "NAGAR_NIGAM",
        "5": "NAGAR_PALIKA_PARISHAD",
        "6": "NOTIFIED_AREA_COUNCIL",
        "7": "NAGAR_PANCHAYAT",
        "8": "CANTONMENT_BOARD",
    }

    expected_codes = {
        str(row["local_body_code"]).strip()
        for row in ulb_df.to_dict("records")
    }

    missing_mapping = (
        expected_codes
        - set(district_by_body_code)
    )

    if missing_mapping:
        sample = sorted(
            missing_mapping,
            key=lambda x: int(x),
        )[:20]

        raise ValueError(
            "ULB district mapping missing for "
            f"{len(missing_mapping)} bodies. "
            f"Sample: {sample}"
        )

    for row in ulb_df.to_dict("records"):
        body_code = str(
            row["local_body_code"]
        ).strip()

        body_name = str(
            row["local_body_name"]
        ).strip()

        type_code = str(
            row["local_body_type_code"]
        ).strip()

        district_code = district_by_body_code[
            body_code
        ]

        body_type_name = type_map.get(
            type_code
        )

        if body_type_name is None:
            raise ValueError(
                f"Unknown ULB type code: "
                f"{type_code} "
                f"for {body_code}"
            )

        district = (
            db.query(District)
            .filter(
                District.district_code
                == district_code
            )
            .first()
        )

        if district is None:
            raise ValueError(
                "District not found for ULB "
                f"{body_code}: {district_code}"
            )

        body_type = getattr(
            __import__(
                "database.models.master.municipal_body",
                fromlist=["MunicipalBodyType"],
            ).MunicipalBodyType,
            body_type_name,
        )

        existing = (
            db.query(MunicipalBody)
            .filter(
                MunicipalBody.body_code
                == body_code
            )
            .first()
        )

        if existing:
            existing.body_name = body_name
            existing.body_type = body_type
            existing.district_id = district.id
            continue

        db.add(
            MunicipalBody(
                body_name=body_name,
                body_code=body_code,
                body_type=body_type,
                district_id=district.id,
                headquarters=None,
            )
        )


def seed_localities(
    db: Session,
    df,
):
    if df is None:
        return

    ward_by_key = {
        (
            str(ward.municipal_body_id).strip(),
            str(ward.ward_number).strip(),
        ): ward
        for ward in db.query(Ward).all()
    }

    for row in df.to_dict("records"):
        municipal_body_id = str(
            row["municipal_body_id"]
        ).strip()

        ward_number = str(
            row["ward_number"]
        ).strip()

        locality_name = str(
            row["locality_name"]
        ).strip()

        locality_code = str(
            row["locality_code"]
        ).strip()

        pincode = str(
            row.get("pincode", "")
        ).strip() or None

        if not locality_name or not locality_code:
            continue

        key = (municipal_body_id, ward_number)

        ward = ward_by_key.get(key)

        if ward is None:
            raise ValueError(
                f"Ward not found for "
                f"municipal_body_id={municipal_body_id}, "
                f"ward_number={ward_number}"
            )

        existing = (
            db.query(Locality)
            .filter(
                Locality.locality_code
                == locality_code
            )
            .first()
        )

        if existing:
            existing.locality_name = locality_name
            existing.ward_id = ward.id
            existing.pincode = pincode
            continue

        db.add(
            Locality(
                locality_name=locality_name,
                locality_code=locality_code,
                ward_id=ward.id,
                pincode=pincode,
            )
        )


def seed_wards(
    db: Session,
    df,
):
    if df is None:
        return

    # Build ULB lookup by authoritative LGD code.
    body_by_code = {
        str(body.body_code).strip(): body
        for body in db.query(MunicipalBody).all()
    }

    for row in df.to_dict("records"):
        body_code = str(
            row["municipal_body_code"]
        ).strip()

        ward_number_raw = str(
            row["ward_number"]
        ).strip()

        ward_name = str(
            row["ward_name"]
        ).strip()

        # Ignore header-like or empty rows.
        if (
            not body_code
            or body_code.lower()
            in {
                "municipal_body_code",
                "local body code",
                "local_body_code",
            }
        ):
            continue

        if not body_code.isdigit():
            raise ValueError(
                f"Invalid municipal body code "
                f"for ward: {body_code!r}"
            )

        if body_code not in body_by_code:
            raise ValueError(
                f"Municipal body not found for "
                f"ward: {body_code}"
            )

        try:
            ward_number = int(
                float(ward_number_raw)
            )
        except (TypeError, ValueError):
            raise ValueError(
                f"Invalid ward number "
                f"{ward_number_raw!r} "
                f"for ULB {body_code}"
            )

        body = body_by_code[body_code]

        # Ward model does not currently store LGD ward_code,
        # so use ULB + ward_number as the idempotent key.
        existing = (
            db.query(Ward)
            .filter(
                Ward.municipal_body_id
                == body.id,
                Ward.ward_number
                == ward_number,
            )
            .first()
        )

        if existing:
            existing.ward_name = ward_name
            continue

        db.add(
            Ward(
                ward_name=ward_name,
                ward_number=ward_number,
                municipal_body_id=body.id,
                population=None,
            )
        )

def import_master_data():
    db = SessionLocal()

    try:
        print(
            "========== UP AI MASTER IMPORT =========="
        )

        state = (
            db.query(State)
            .filter(
                State.state_code == "UP"
            )
            .first()
        )

        if state is None:
            raise RuntimeError(
                "UP state does not exist."
            )

        seed_divisions(
            db,
            read_csv("divisions.csv"),
            state,
        )

        db.flush()

        seed_districts(
            db,
            read_csv("districts.csv"),
        )

        db.flush()

        seed_tehsils(
            db,
            read_csv("tehsils.csv"),
        )

        db.flush()

        seed_blocks(
            db,
            read_csv("blocks.csv"),
        )

        db.flush()

        seed_gram_panchayats(
            db,
            read_csv("gram_panchayats.csv"),
        )

        db.flush()

        seed_villages(
            db,
            read_csv("villages.csv"),
        )

        db.flush()

        # ------------------------------------------
        # Urban master data
        # ------------------------------------------

        seed_municipal_bodies(
            db,
            read_csv("municipal_bodies.csv"),
            read_csv(
                "municipal_body_district_mapping.csv"
            ),
        )

        db.flush()

        seed_wards(
            db,
            read_csv("wards.csv"),
        )

        db.flush()

        db.commit()

        print(
            "✅ Rural master data imported successfully."
        )

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    import_master_data()
