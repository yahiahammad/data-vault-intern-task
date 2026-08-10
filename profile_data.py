"""Profiling for the three T24 source extracts.

Reads data/fbnk_customer.csv, data/fbnk_account.csv, data/fbnk_stmt_entry.csv,
runs the checks docs/deliverables.md and docs/source_dictionary.md ask for
(empty columns, grain vs identifier, version churn, referential gaps between
tables, value checks against what source_dictionary.md claims), and writes
one HTML report per table plus a cross-table report into profile_reports/.

Run: python profile_data.py
"""
import html
from pathlib import Path

import pandas as pd

DATA_DIR = Path(__file__).resolve().parent / "data"
OUT_DIR = Path(__file__).resolve().parent / "profile_reports"


def load(name: str) -> pd.DataFrame:
    return pd.read_csv(DATA_DIR / name, dtype=str, keep_default_na=False)


# ---------------------------------------------------------------------------
# profiling primitives -- each returns plain data (dict / list), no printing
# ---------------------------------------------------------------------------

def empty_columns(df: pd.DataFrame) -> list[dict]:
    n = len(df)
    rows = []
    for col in df.columns:
        empty = int((df[col] == "").sum())
        if empty == 0:
            continue
        rows.append({
            "column": col,
            "empty": empty,
            "of": n,
            "pct": round(empty / n * 100),
            "status": "always empty" if empty == n else "partial",
        })
    rows.sort(key=lambda r: -r["pct"])
    return rows


def grain(df: pd.DataFrame, id_col: str, key_fn=None) -> tuple[dict, pd.Series]:
    keys = df[id_col].map(key_fn) if key_fn else df[id_col]
    repeats = keys.value_counts()
    repeats = repeats[repeats > 1]
    stats = {
        "rows": len(df),
        f"distinct {id_col}": int(keys.nunique()),
        "ids with more than one row": len(repeats),
    }
    return stats, keys, repeats.to_dict()


def no_op_versions(df: pd.DataFrame, key: pd.Series, order_col: str, ignore_cols: set) -> list:
    payload_cols = [c for c in df.columns if c not in ignore_cols]
    tmp = df.assign(_key=key)
    flagged = []
    for k, group in tmp.groupby("_key"):
        if len(group) < 2:
            continue
        group = group.sort_values(order_col)
        same_as_prev = (group[payload_cols] == group[payload_cols].shift()).all(axis=1)
        if same_as_prev.iloc[1:].any():
            flagged.append(k)
    return flagged


def value_check(df: pd.DataFrame, col: str, allowed: set) -> list:
    return sorted(set(df[col]) - allowed - {""})


def date_check(df: pd.DataFrame, col: str) -> list[dict]:
    non_empty = df[df[col] != ""]
    bad = non_empty[pd.to_datetime(non_empty[col], format="%Y%m%d", errors="coerce").isna()]
    return bad[["recid", col]].to_dict("records")


def referential_gap(child_values: pd.Series, parent_values: set) -> list:
    return sorted({v for v in child_values if v and v not in parent_values})


# ---------------------------------------------------------------------------
# tiny HTML renderer -- generic dispatch on the shape of the data above
# ---------------------------------------------------------------------------

class Raw(str):
    """Marks a string as already-built HTML, so it's emitted as-is."""


def esc(v) -> str:
    return html.escape("" if v is None else str(v))


def render_table(rows: list[dict]) -> str:
    cols = list(rows[0].keys())
    head = "".join(f"<th>{esc(c)}</th>" for c in cols)
    body = []
    for row in rows:
        cls = {"always empty": "row-bad", "partial": "row-warn"}.get(row.get("status"), "")
        cells = "".join(f"<td>{esc(row.get(c, ''))}</td>" for c in cols)
        body.append(f'<tr class="{cls}">{cells}</tr>' if cls else f"<tr>{cells}</tr>")
    return f'<table><thead><tr>{head}</tr></thead><tbody>{"".join(body)}</tbody></table>'


def render_bar_table(counts: dict) -> str:
    if not counts:
        return '<p class="muted">no values</p>'
    top = max(counts.values())
    rows = []
    for k, v in sorted(counts.items(), key=lambda kv: -kv[1]):
        pct = round(v / top * 100)
        label = esc(k) if k else "(empty)"
        rows.append(
            f'<tr><td class="bar-label">{label}</td>'
            f'<td class="bar-cell"><div class="bar" style="width:{pct}%"></div>'
            f'<span class="bar-value">{v}</span></td></tr>'
        )
    return f'<table class="bar-table"><tbody>{"".join(rows)}</tbody></table>'


def render_any(content) -> str:
    if isinstance(content, Raw):
        return content
    if isinstance(content, list) and content and isinstance(content[0], dict):
        return render_table(content)
    if isinstance(content, dict):
        items = "".join(f"<dt>{esc(k)}</dt><dd>{esc(v)}</dd>" for k, v in content.items())
        return f"<dl>{items}</dl>"
    if isinstance(content, list):
        if not content:
            return '<p class="muted">none</p>'
        return "<ul>" + "".join(f"<li>{esc(i)}</li>" for i in content) + "</ul>"
    return f"<p>{esc(content)}</p>"


def is_empty(content) -> bool:
    if isinstance(content, Raw):
        return False
    return content in ({}, [], "", None)


def section(heading: str, content, flag: bool = False) -> str:
    """flag=True: empty content renders as a green OK line, non-empty as a red callout.
    flag=False: content is informational, rendered plainly either way."""
    if flag:
        body = '<p class="ok">&#10003; none found</p>' if is_empty(content) else (
            f'<div class="flagged">{render_any(content)}</div>'
        )
    else:
        body = render_any(content)
    return f"<section><h2>{esc(heading)}</h2>{body}</section>"


CSS = """
:root { color-scheme: light dark; }
* { box-sizing: border-box; }
body {
  font-family: -apple-system, Segoe UI, Roboto, sans-serif;
  margin: 0; padding: 2rem 3rem 4rem;
  background: #f6f7f9; color: #1f2328;
}
@media (prefers-color-scheme: dark) {
  body { background: #0d1117; color: #e6edf3; }
  section, .card { background: #161b22 !important; border-color: #30363d !important; }
  table { border-color: #30363d !important; }
  th { background: #21262d !important; }
  tr.row-bad { background: #3b1418 !important; }
  tr.row-warn { background: #3a2e12 !important; }
  .flagged { background: #3b1418 !important; border-color: #cf222e !important; }
  .bar { background: #2f81f7 !important; }
  a { color: #58a6ff !important; }
}
header { margin-bottom: 1.5rem; }
h1 { margin: 0 0 .25rem; }
.subtitle { color: #656d76; margin: 0; }
nav { margin-bottom: 2rem; }
nav a { margin-right: 1rem; font-weight: 600; text-decoration: none; }
.stat-row { display: flex; gap: 1rem; flex-wrap: wrap; margin-bottom: 2rem; }
.card {
  background: #fff; border: 1px solid #d0d7de; border-radius: 8px;
  padding: .9rem 1.2rem; min-width: 160px;
}
.card .n { font-size: 1.6rem; font-weight: 700; display: block; }
.card .label { color: #656d76; font-size: .8rem; }
section {
  background: #fff; border: 1px solid #d0d7de; border-radius: 8px;
  padding: 1.2rem 1.5rem; margin-bottom: 1.3rem;
}
h2 { font-size: 1.05rem; margin: 0 0 .8rem; }
table { border-collapse: collapse; width: 100%; font-size: .9rem; }
th, td { text-align: left; padding: .35rem .6rem; border-bottom: 1px solid #eaeef2; }
th { background: #f6f8fa; }
tr.row-bad { background: #ffebe9; }
tr.row-warn { background: #fff8c5; }
.bar-table td { border: none; padding: .25rem .6rem; }
.bar-label { width: 12rem; white-space: nowrap; }
.bar-cell { position: relative; }
.bar { display: inline-block; height: .9rem; background: #2563eb; border-radius: 3px; vertical-align: middle; }
.bar-value { margin-left: .5rem; font-size: .8rem; color: #656d76; }
.flagged {
  background: #ffebe9; border: 1px solid #cf222e; border-radius: 6px; padding: .6rem 1rem;
}
.ok { color: #1a7f37; font-weight: 600; margin: 0; }
.muted { color: #8b949e; margin: 0; }
ul { margin: .3rem 0; padding-left: 1.3rem; }
footer { color: #8b949e; font-size: .8rem; margin-top: 2rem; }
"""

NAV = (
    '<nav><a href="index.html">Overview</a>'
    '<a href="customer.html">Customer</a>'
    '<a href="account.html">Account</a>'
    '<a href="stmt_entry.html">Statement entry</a>'
    '<a href="cross_table.html">Cross-table</a></nav>'
)


def page(title: str, subtitle: str, stat_cards: list[tuple[str, str]], sections_html: list[str]) -> str:
    cards = "".join(
        f'<div class="card"><span class="n">{esc(n)}</span><span class="label">{esc(l)}</span></div>'
        for n, l in stat_cards
    )
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{esc(title)}</title>
<style>{CSS}</style>
</head>
<body>
<header><h1>{esc(title)}</h1><p class="subtitle">{esc(subtitle)}</p></header>
{NAV}
<div class="stat-row">{cards}</div>
{"".join(sections_html)}
<footer>Generated by profile_data.py</footer>
</body>
</html>"""


def main() -> None:
    OUT_DIR.mkdir(exist_ok=True)

    customer = load("fbnk_customer.csv")
    account = load("fbnk_account.csv")
    stmt = load("fbnk_stmt_entry.csv")

    meta_cols = {
        "curr_no", "update_date", "date_last_update", "inputter", "authoriser",
        "source_system", "source_table", "ingested_ts", "created_ts", "created_dt",
        "online_actual_bal", "online_cleared_bal", "open_actual_bal",
        "working_balance", "prev_bal",
    }

    # ---- Customer ----------------------------------------------------
    cust_empty = empty_columns(customer)
    cust_grain_stats, cust_no, cust_repeats = grain(customer, "recid", key_fn=lambda v: v.split(";")[0])
    cust_no_op = no_op_versions(customer, cust_no, "curr_no", meta_cols | {"recid"})

    customer_sections = [
        section("Empty columns", cust_empty),
        section("Grain: recid = customer_no;curr_no", cust_grain_stats),
        section("Repeated customer numbers (versions)", cust_repeats),
        section("No-op versions (payload identical to previous version)", cust_no_op, flag=True),
        section("genders unexpected values", value_check(customer, "genders", {"M", "F"}), flag=True),
        section("peps unexpected values", value_check(customer, "peps", {"YES", "NO"}), flag=True),
        section("id_type unexpected values", value_check(customer, "id_type", {"NATID", "COMMREG"}), flag=True),
        section("birth_incorp_date not a valid YYYYMMDD date", date_check(customer, "birth_incorp_date"), flag=True),
        section("sector distribution", Raw(render_bar_table(customer["sector"].value_counts().to_dict()))),
        section("customer_status distribution", Raw(render_bar_table(customer["customer_status"].value_counts().to_dict()))),
        section("risk_rate distribution", Raw(render_bar_table(customer["risk_rate"].value_counts().to_dict()))),
        section("profession distribution", Raw(render_bar_table(customer["profession"].value_counts().to_dict()))),
    ]
    (OUT_DIR / "customer.html").write_text(page(
        "fbnk_customer profiling",
        "One row per customer version (recid = customer_no;curr_no).",
        [(len(customer), "rows"), (cust_grain_stats["distinct recid"], "distinct customers"),
         (len(cust_no_op), "no-op versions"), (len(cust_empty), "columns with blanks")],
        customer_sections,
    ), encoding="utf-8")

    # ---- Account ---------------------------------------------------------
    acct_empty = empty_columns(account)
    acct_grain_stats, acct_no, acct_repeats = grain(account, "recid")
    acct_no_op = no_op_versions(account, acct_no, "curr_no", meta_cols | {"recid"})
    internal = account[account["customer"] == ""]

    account_sections = [
        section("Empty columns", acct_empty),
        section("Grain: recid (no version suffix, unlike customer)", acct_grain_stats),
        section("Repeated account numbers (versions)", acct_repeats),
        section("No-op versions (payload identical to previous version)", acct_no_op, flag=True),
        section("alt_acct_type_1 unexpected values", value_check(account, "alt_acct_type_1", {"IBAN", "OLDACC"}), flag=True),
        section("alt_acct_type_2 unexpected values", value_check(account, "alt_acct_type_2", {"IBAN", "OLDACC"}), flag=True),
        section("record_status unexpected values", value_check(account, "record_status", {"CLOSED"}), flag=True),
        section("closed_online unexpected values", value_check(account, "closed_online", {"Y"}), flag=True),
        section("inactiv_marker unexpected values", value_check(account, "inactiv_marker", {"Y"}), flag=True),
        section("closure_date not a valid YYYYMMDD date", date_check(account, "closure_date"), flag=True),
        section("Internal accounts (customer empty)", {
            "count": len(internal), "categories used": ", ".join(sorted(internal["category"].unique())),
        }),
        section("category distribution", Raw(render_bar_table(account["category"].value_counts().to_dict()))),
        section("posting_restrict distribution", Raw(render_bar_table(account["posting_restrict"].value_counts().to_dict()))),
        section("balance columns (min / max / negative count)", [
            {
                "column": col,
                "min": pd.to_numeric(account[col]).min(),
                "max": pd.to_numeric(account[col]).max(),
                "negative_count": int((pd.to_numeric(account[col]) < 0).sum()),
            }
            for col in ["online_actual_bal", "online_cleared_bal", "open_actual_bal", "working_balance", "prev_bal"]
        ]),
    ]
    (OUT_DIR / "account.html").write_text(page(
        "fbnk_account profiling",
        "One row per account version; recid repeats across versions (no suffix).",
        [(len(account), "rows"), (acct_grain_stats["distinct recid"], "distinct accounts"),
         (len(acct_no_op), "no-op versions"), (len(internal), "internal accounts")],
        account_sections,
    ), encoding="utf-8")

    # ---- Statement entry ---------------------------------------------------
    stmt_empty = empty_columns(stmt)
    stmt_grain_stats, stmt_id, _ = grain(stmt, "recid")

    stmt_amt = stmt.assign(amount_lcy=pd.to_numeric(stmt["amount_lcy"]))
    per_ref = stmt_amt.groupby("our_reference").agg(legs=("recid", "count"), net=("amount_lcy", "sum"))
    unbalanced = per_ref[per_ref["net"].round(2) != 0].reset_index().to_dict("records")

    reversal_rows = stmt[stmt["trans_reference"] != ""]
    reversal_gap = referential_gap(reversal_rows["trans_reference"], set(stmt["recid"]))

    fcy_mismatch = stmt[(stmt["amount_fcy"] == "") != (stmt["exchange_rate"] == "")][
        ["recid", "amount_fcy", "exchange_rate"]
    ].to_dict("records")

    stmt_sections = [
        section("Empty columns", stmt_empty),
        section("Grain: recid (never amended, no version)", stmt_grain_stats),
        section("reversal_marker unexpected values", value_check(stmt, "reversal_marker", {"R"}), flag=True),
        section("booking_date not a valid YYYYMMDD date", date_check(stmt, "booking_date"), flag=True),
        section("value_date not a valid YYYYMMDD date", date_check(stmt, "value_date"), flag=True),
        section("Double-entry: our_reference groups that don't net to 0", unbalanced, flag=True),
        section("Reversal linkage: trans_reference with no matching recid", reversal_gap, flag=True),
        section("amount_fcy / exchange_rate set on only one side (should be both or neither)", fcy_mismatch, flag=True),
        section("transaction_code distribution", Raw(render_bar_table(stmt["transaction_code"].value_counts().to_dict()))),
        section("product_category distribution", Raw(render_bar_table(stmt["product_category"].value_counts().to_dict()))),
        section("system_id distribution", Raw(render_bar_table(stmt["system_id"].value_counts().to_dict()))),
    ]
    (OUT_DIR / "stmt_entry.html").write_text(page(
        "fbnk_stmt_entry profiling",
        "One row per accounting entry; never amended, reversed instead.",
        [(len(stmt), "rows"), (stmt_grain_stats["distinct recid"], "distinct recid"),
         (len(per_ref), "our_reference groups"), (len(unbalanced), "double-entry flags")],
        stmt_sections,
    ), encoding="utf-8")

    # ---- Cross-table referential checks -----------------------------------
    customer_nos = set(cust_no)
    account_nos = set(acct_no)

    gap_acct_cust = referential_gap(account["customer"], customer_nos)
    gap_stmt_cust = referential_gap(stmt["customer_id"], customer_nos)
    gap_stmt_acct = referential_gap(stmt["account_number"], account_nos)

    orphan_customers = sorted(customer_nos - set(account["customer"]) - {c for c in stmt["customer_id"] if c})
    orphan_accounts = sorted(account_nos - set(stmt["account_number"]))

    acct_customer = account.drop_duplicates("recid", keep="last").set_index("recid")["customer"]
    mismatches = []
    for _, row in stmt.iterrows():
        current = acct_customer.get(row["account_number"])
        if row["customer_id"] and current not in (None, "") and row["customer_id"] != current:
            mismatches.append({
                "stmt_recid": row["recid"], "account_number": row["account_number"],
                "customer_id_on_entry": row["customer_id"], "account's_current_customer": current,
            })

    cross_sections = [
        section("account.customer -> customer number (missing)", gap_acct_cust, flag=True),
        section("stmt_entry.customer_id -> customer number (missing)", gap_stmt_cust, flag=True),
        section("stmt_entry.account_number -> account.recid (missing)", gap_stmt_acct, flag=True),
        section("Customers with no account and no statement entry", orphan_customers, flag=True),
        section("Accounts with no statement entry", orphan_accounts, flag=True),
        section("stmt_entry.customer_id vs account's current customer (dictionary flags a mismatch)", mismatches, flag=True),
    ]
    (OUT_DIR / "cross_table.html").write_text(page(
        "Cross-table referential checks",
        "Foreign key gaps between fbnk_customer, fbnk_account and fbnk_stmt_entry.",
        [(len(gap_acct_cust) + len(gap_stmt_cust) + len(gap_stmt_acct), "missing FK values"),
         (len(orphan_customers), "orphan customers"), (len(orphan_accounts), "orphan accounts"),
         (len(mismatches), "customer_id mismatches")],
        cross_sections,
    ), encoding="utf-8")

    # ---- Index --------------------------------------------------------
    index_body = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Source data profiling</title>
<style>{CSS}</style>
</head>
<body>
<header><h1>Source data profiling</h1><p class="subtitle">fbnk_customer, fbnk_account, fbnk_stmt_entry</p></header>
{NAV}
<div class="stat-row">
  <div class="card"><span class="n">{len(customer)}</span><span class="label">customer rows</span></div>
  <div class="card"><span class="n">{len(account)}</span><span class="label">account rows</span></div>
  <div class="card"><span class="n">{len(stmt)}</span><span class="label">stmt_entry rows</span></div>
</div>
<section><h2>Reports</h2>
<ul>
  <li><a href="customer.html">fbnk_customer</a> - empty columns, grain, no-op versions, value checks</li>
  <li><a href="account.html">fbnk_account</a> - empty columns, grain, no-op versions, value checks</li>
  <li><a href="stmt_entry.html">fbnk_stmt_entry</a> - empty columns, double-entry balance, reversal linkage</li>
  <li><a href="cross_table.html">Cross-table</a> - referential gaps between all three tables</li>
</ul>
</section>
<footer>Generated by profile_data.py</footer>
</body>
</html>"""
    (OUT_DIR / "index.html").write_text(index_body, encoding="utf-8")

    print(f"Wrote {len(list(OUT_DIR.glob('*.html')))} HTML reports to {OUT_DIR}")


if __name__ == "__main__":
    main()
