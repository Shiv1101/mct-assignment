
import xml.etree.ElementTree as ET


def parse_tally_xml(content: str):

    root = ET.fromstring(content)

    company = root.find(".//COMPANY")

    if company is None:
        raise Exception("Invalid Tally XML")

    company_name = company.attrib.get("NAME")

    period_start = company.findtext(
        "CURRENTPERIODSTART"
    )

    period_end = company.findtext(
        "CURRENTPERIODEND"
    )

    cash_balance = int(
        float(
            company.findtext(
                "CASHLEDGER/CLOSINGBALANCE",
                "0"
            )
        )
    )

    debtors = []

    for ledger in company.findall(
        "SUNDRYDEBTORS/LEDGER"
    ):

        debtor = {
            "name": ledger.attrib.get("NAME"),

            "amount": int(
                float(
                    ledger.findtext(
                        "CLOSINGBALANCE",
                        "0"
                    )
                )
            )
        }

        debtors.append(debtor)

    debtors.sort(
        key=lambda x: x["amount"],
        reverse=True
    )

    total_debtors = sum(
        debtor["amount"]
        for debtor in debtors
    )

    revenue = int(
        float(
            company.findtext(
                "PROFITANDLOSS/REVENUE",
                "0"
            )
        )
    )

    raw_material = int(
        float(
            company.findtext(
                "PROFITANDLOSS/RAWMATERIAL",
                "0"
            )
        )
    )

    direct_labour = int(
        float(
            company.findtext(
                "PROFITANDLOSS/DIRECTLABOUR",
                "0"
            )
        )
    )

    overhead = int(
        float(
            company.findtext(
                "PROFITANDLOSS/OVERHEAD",
                "0"
            )
        )
    )

    net_profit = int(
        float(
            company.findtext(
                "PROFITANDLOSS/NETPROFIT",
                "0"
            )
        )
    )

    gross_profit = (
        revenue
        - raw_material
        - direct_labour
        - overhead
    )

    gross_margin_pct = round(
        (gross_profit / revenue) * 100,
        2
    )

    net_margin_pct = round(
        (net_profit / revenue) * 100,
        2
    )

    return {

        "company_name": company_name,

        "period": {
            "start": period_start,
            "end": period_end
        },

        "cash_balance": cash_balance,

        "top_debtors": debtors,

        "total_debtors": total_debtors,

        "pl_summary": {

            "revenue": revenue,

            "raw_material": raw_material,

            "gross_profit": gross_profit,

            "gross_margin_pct": gross_margin_pct,

            "net_profit": net_profit,

            "net_margin_pct": net_margin_pct
        }
    }

