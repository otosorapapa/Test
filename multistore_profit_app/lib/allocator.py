import pandas as pd
import numpy as np

def allocate_overhead(
    overhead: pd.DataFrame,
    store_master: pd.DataFrame,
    sales_gp: pd.DataFrame,
    basis: str = "sales"
) -> pd.DataFrame:
    oh = overhead.copy()
    oh["month"] = oh["date"].dt.to_period("M").dt.to_timestamp()

    s = sales_gp.groupby(["month","store_id"], as_index=False).agg(
        revenue=("revenue","sum"),
        gross_profit=("gross_profit","sum"),
        qty=("qty","sum"),
    )
    sm = store_master.copy()
    basis = basis.lower()
    if basis == "sales":
        weights = s[["month","store_id","revenue"]].rename(columns={"revenue":"w"})
    elif basis in ("gp","gross_profit"):
        weights = s[["month","store_id","gross_profit"]].rename(columns={"gross_profit":"w"})
    elif basis == "headcount":
        weights = s[["month","store_id"]].merge(sm[["store_id","headcount"]], on="store_id", how="left").rename(columns={"headcount":"w"})
    elif basis == "area":
        weights = s[["month","store_id"]].merge(sm[["store_id","area_sqm"]], on="store_id", how="left").rename(columns={"area_sqm":"w"})
    else:
        raise ValueError("Unknown allocation basis")

    weights["w"] = weights["w"].fillna(0.0)
    weights["w_sum"] = weights.groupby("month")["w"].transform("sum")
    weights["w_norm"] = np.where(weights["w_sum"]>0, weights["w"]/weights["w_sum"], 0.0)

    dist_rows = []
    for _, row in oh.iterrows():
        m = row["month"]
        amt = row["amount"]
        tmp = weights[weights["month"]==m][["store_id","w_norm"]].copy()
        if tmp.empty:
            continue
        tmp["allocated_amount"] = tmp["w_norm"] * amt
        tmp["month"] = m
        tmp["account"] = row["account"]
        dist_rows.append(tmp[["month","store_id","account","allocated_amount"]])
    if not dist_rows:
        return pd.DataFrame(columns=["month","store_id","account","allocated_amount"])
    allocated = pd.concat(dist_rows, ignore_index=True)
    return allocated
