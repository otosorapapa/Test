import pandas as pd
import numpy as np

def compute_sales_gp(sales: pd.DataFrame) -> pd.DataFrame:
    df = sales.copy()
    df["revenue"] = (df["qty"] * df["unit_price"]) - df["discount"].fillna(0)
    df["cogs"] = df["qty"] * df["unit_cost"]
    df["gross_profit"] = df["revenue"] - df["cogs"]
    df["month"] = df["date"].dt.to_period("M").dt.to_timestamp()
    return df

def monthly_kpis(sales_gp: pd.DataFrame) -> pd.DataFrame:
    g = sales_gp.groupby("month", as_index=False).agg(
        revenue=("revenue","sum"),
        gross_profit=("gross_profit","sum"),
        qty=("qty","sum"),
    )
    g["gp_margin"] = np.where(g["revenue"]!=0, g["gross_profit"]/g["revenue"], np.nan)
    return g

def store_pl(sales_gp: pd.DataFrame, expenses: pd.DataFrame, allocated: pd.DataFrame) -> pd.DataFrame:
    exp = expenses.copy()
    exp["month"] = exp["date"].dt.to_period("M").dt.to_timestamp()
    direct = exp[exp["di_type"].str.lower()=="direct"].groupby(["month","store_id"], as_index=False)["amount"].sum()
    s = sales_gp.groupby(["month","store_id","store_name"], as_index=False).agg(
        revenue=("revenue","sum"),
        cogs=("cogs","sum"),
        qty=("qty","sum"),
        gross_profit=("gross_profit","sum"),
    )
    alloc = allocated.groupby(["month","store_id"], as_index=False)["allocated_amount"].sum()
    out = s.merge(direct, on=["month","store_id"], how="left").rename(columns={"amount":"direct_opex"})
    out["direct_opex"] = out["direct_opex"].fillna(0.0)
    out = out.merge(alloc, on=["month","store_id"], how="left")
    out["allocated_amount"] = out["allocated_amount"].fillna(0.0)
    out["ebit"] = out["gross_profit"] - out["direct_opex"] - out["allocated_amount"]
    out["gp_margin"] = np.where(out["revenue"]!=0, out["gross_profit"]/out["revenue"], np.nan)
    out["ebit_margin"] = np.where(out["revenue"]!=0, out["ebit"]/out["revenue"], np.nan)
    return out

def basic_quality_checks(sales: pd.DataFrame, expenses: pd.DataFrame) -> pd.DataFrame:
    issues = []
    bad_qty = sales[(sales["qty"]<=0) & (sales["unit_price"]>0)]
    if not bad_qty.empty:
        issues.append({"type":"sales_qty","rows":len(bad_qty),"sample_index":int(bad_qty.index[0])})
    bad_exp = expenses[(expenses["di_type"].str.lower()=="direct") & (expenses["store_id"].isna())]
    if not bad_exp.empty:
        issues.append({"type":"direct_expense_missing_store","rows":len(bad_exp),"sample_index":int(bad_exp.index[0])})
    return pd.DataFrame(issues)
