from pathlib import Path
from typing import Dict, Optional, Tuple
import pandas as pd
from .utils import DATA_DIR, ensure_dir

REQUIRED = {
    "sales": ["date","store_id","store_name","product_id","product_category","channel","qty","unit_price","unit_cost","discount"],
    "expenses": ["date","store_id","account","subaccount","amount","fv_type","di_type"],
    "overhead": ["date","account","amount","allocation_basis"],
    "store_master": ["store_id","store_name","area_sqm","headcount","open_date","region"],
}

DEFAULT_PATHS = {
    "sales": DATA_DIR / "sample" / "sales.csv",
    "expenses": DATA_DIR / "sample" / "expenses.csv",
    "overhead": DATA_DIR / "sample" / "overhead.csv",
    "store_master": DATA_DIR / "sample" / "store_master.csv",
}

def _read_any(path: Path) -> pd.DataFrame:
    suffix = path.suffix.lower()
    if suffix in (".xls",".xlsx"):
        return pd.read_excel(path)
    return pd.read_csv(path)

def load_all(
    files: Optional[Dict[str, Path]] = None,
    coerce_dates: bool = True,
):
    files = files or {}
    dfs = {}
    for key in ["sales","expenses","overhead","store_master"]:
        p = Path(files.get(key) or DEFAULT_PATHS[key])
        if not p.exists():
            raise FileNotFoundError(f"Missing file for {key}: {p}")
        df = _read_any(p)
        df.columns = [c.strip() for c in df.columns]
        missing = set(REQUIRED[key]) - set(df.columns)
        if missing:
            raise ValueError(f"{key}: missing columns {missing} in {p.name}")
        if coerce_dates and "date" in df.columns:
            df["date"] = pd.to_datetime(df["date"])
        dfs[key] = df
    return dfs["sales"], dfs["expenses"], dfs["overhead"], dfs["store_master"]

def save_uploaded(df: pd.DataFrame, target: Path) -> Path:
    target = ensure_dir(target)
    if target.suffix.lower() in (".xls",".xlsx"):
        df.to_excel(target, index=False)
    else:
        df.to_csv(target, index=False)
    return target
