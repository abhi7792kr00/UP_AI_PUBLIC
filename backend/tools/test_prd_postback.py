from __future__ import annotations

import re
import requests
from bs4 import BeautifulSoup

URL = (
    "https://prdfinance.up.gov.in/"
    "PRD_reports/"
    "gangaactionplan_pr_sbm_plan_gpdata_public.aspx"
)

HEADERS = {
    "User-Agent": "Mozilla/5.0",
}


def hidden_fields(soup):
    data = {}

    for inp in soup.find_all(
        "input",
        type="hidden",
    ):
        name = inp.get("name")

        if not name:
            continue

        data[name] = inp.get("value", "")

    return data


def parse_select(
    soup,
    element_id: str,
):
    select = soup.find(
        "select",
        id=element_id,
    )

    if select is None:
        return []

    return [
        (
            option.get("value", ""),
            option.get_text(
                " ",
                strip=True,
            ),
        )
        for option in select.find_all("option")
    ]


def main():
    session = requests.Session()

    try:
        response = session.get(
            URL,
            timeout=(10, 30),
            headers=HEADERS,
        )
    except Exception as exc:
        print("INITIAL REQUEST ERROR:")
        print(repr(exc))
        return

    print("INITIAL STATUS:", response.status_code)
    print("FINAL URL:", response.url)
    print("CONTENT:", len(response.content))

    response.raise_for_status()

    soup = BeautifulSoup(
        response.text,
        "html.parser",
    )

    print("\n===== HIDDEN FIELDS =====")

    hidden = hidden_fields(soup)

    for key, value in hidden.items():
        print(
            key,
            "=",
            value[:120],
        )

    print("\n===== DISTRICT OPTIONS =====")

    districts = parse_select(
        soup,
        "ddlDistrict",
    )

    print(
        "COUNT:",
        len(districts),
    )

    for value, text in districts[:20]:
        print(
            repr(value),
            "|",
            text,
        )

    if not districts:
        print(
            "\nNo district options in initial response."
        )
        print(
            "The page may populate them on a first "
            "server event/session initialization."
        )
        return

    district_value, district_text = (
        districts[0]
    )

    print(
        "\nTEST DISTRICT:",
        repr(district_value),
        "|",
        district_text,
    )

    # -----------------------------------------------------
    # ASP.NET WebForms postback for ddlDistrict
    # -----------------------------------------------------

    payload = hidden.copy()

    payload.update(
        {
            "__EVENTTARGET": "ddlDistrict",
            "__EVENTARGUMENT": "",
            "ddlDistrict": district_value,
        }
    )

    try:
        post = session.post(
            URL,
            data=payload,
            timeout=(10, 30),
            headers={
                **HEADERS,
                "Referer": URL,
            },
        )
    except Exception as exc:
        print(
            "\nPOSTBACK ERROR:"
        )
        print(repr(exc))
        return

    print(
        "\nPOST STATUS:",
        post.status_code,
    )

    print(
        "POST FINAL URL:",
        post.url,
    )

    print(
        "POST CONTENT:",
        len(post.content),
    )

    post.raise_for_status()

    post_soup = BeautifulSoup(
        post.text,
        "html.parser",
    )

    print(
        "\n===== BLOCK OPTIONS AFTER DISTRICT ====="
    )

    blocks = parse_select(
        post_soup,
        "drdp_block",
    )

    print(
        "COUNT:",
        len(blocks),
    )

    for value, text in blocks[:30]:
        print(
            repr(value),
            "|",
            text,
        )

    print(
        "\n===== GP OPTIONS ====="
    )

    gps = parse_select(
        post_soup,
        "drdp_GramPanchayat",
    )

    print(
        "COUNT:",
        len(gps),
    )

    for value, text in gps[:20]:
        print(
            repr(value),
            "|",
            text,
        )


if __name__ == "__main__":
    main()
