import pandas as pd
import numpy as np

def simulate_sales(
    sales: pd.DataFrame,
    price_pct: float = 0.0,
    volume_pct: float = 0.0,
    cost_pct: float = 0.0,
    mix_shift: float = 0.0,
    mix_key: str = "product_category"
) -> pd.DataFrame:
    """
    Apply simple what-if: price, volume, cost, and a linear mix shift toward the
    highest gross-profit category.
    """
    df = sales.copy()
    df["unit_price_sim"] = df["unit_price"] * (1 + price_pct/100.0)
    df["unit_cost_sim"] = df["unit_cost"] * (1 + cost_pct/100.0)
    df["qty_sim"] = df["qty"] * (1 + volume_pct/100.0)

    if mix_key in df.columns and mix_shift != 0:
        gp_by_cat = df.groupby(mix_key).apply(
            lambda x: ((x["unit_price"]-x["unit_cost"]) * x["qty"]).sum()
        ).sort_values(ascending=False)
        if not gp_by_cat.empty:
            top_cat = gp_by_cat.index[0]
            mask_top = df[mix_key]==top_cat
            move = (df.loc[~mask_top,"qty_sim"] * (mix_shift/100.0)).sum()
            df.loc[~mask_top,"qty_sim"] *= (1 - mix_shift/100.0)
            top_total = df.loc[mask_top,"qty_sim"].sum()
            if top_total > 0 and move > 0:
                df.loc[mask_top,"qty_sim"] += move * (df.loc[mask_top,"qty_sim"] / top_total)

    df["revenue_sim"] = df["qty_sim"] * df["unit_price_sim"] - df["discount"].fillna(0)
    df["cogs_sim"] = df["qty_sim"] * df["unit_cost_sim"]
    df["gross_profit_sim"] = df["revenue_sim"] - df["cogs_sim"]
    df["month"] = pd.to_datetime(df["date"]).dt.to_period("M").dt.to_timestamp()
    return df

def break_even_point(revenue: float, fixed_cost: float, gp_margin: float) -> float:
    """
    Return required revenue to break even given fixed cost and GP margin.
    """
    if gp_margin <= 0:
        return float("inf")
    return fixed_cost / gp_margin
