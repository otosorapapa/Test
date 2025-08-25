import io, base64
from pathlib import Path
import pandas as pd
from dash import dcc, Input, Output, State, callback, register_page, no_update
import dash_mantine_components as dmc
from lib.data_loader import REQUIRED, save_uploaded
from lib.utils import DATA_DIR

register_page(
    __name__,
    path="/1_📥_データ取込",
    name="📥 データ取込",
    title="データ取込",
)

def layout():
    return dmc.Container([
        dmc.Title("📥 データ取込（CSV / Excel）", order=2),
        dmc.Text("sales / expenses / overhead / store_master を順にアップロードするか、サンプルデータのまま進められます。"),
        dmc.Space(h=10),
        dmc.SimpleGrid(cols=2, children=[
            _uploader_card("sales"),
            _uploader_card("expenses"),
            _uploader_card("overhead"),
            _uploader_card("store_master"),
        ]),
        dmc.Space(h=20),
        dmc.Alert("アップロード後、各ページで分析を開始できます。", color="green"),
    ], fluid=True)

def _uploader_card(kind: str):
    return dmc.Card([
        dmc.Text(f"{kind} をアップロード", weight=600),
        dmc.Text(f"必須カラム: {', '.join(REQUIRED[kind])}", size="xs", color="dimmed"),
        dmc.Space(h=5),
        dcc.Upload(id=f"upload-{kind}", children=dmc.Button("ファイルを選択", variant="light"), multiple=False),
        dmc.Space(h=8),
        dmc.Text(id=f"status-{kind}", size="sm"),
        dmc.Space(h=5),
        dmc.ScrollArea(style={"height":"200px"}, children=dmc.Code(id=f"preview-{kind}", block=True)),
    ], withBorder=True, shadow="xs", radius="md", p="md")

def _handle_upload(content, filename, kind):
    if content is None:
        return no_update, no_update
    try:
        header, b64 = content.split(",")
        decoded = base64.b64decode(b64)
        if filename.lower().endswith((".xls",".xlsx")):
            df = pd.read_excel(io.BytesIO(decoded))
            target = DATA_DIR / f"{kind}.xlsx"
        else:
            df = pd.read_csv(io.BytesIO(decoded))
            target = DATA_DIR / f"{kind}.csv"
        save_uploaded(df, target)
        head = df.head(10).to_markdown(index=False)
        return dmc.Text(f"保存しました: {target}"), head
    except Exception as e:
        return dmc.Text(f"エラー: {e}", color="red"), ""

@callback(
    Output("status-sales","children"),
    Output("preview-sales","children"),
    Input("upload-sales","contents"),
    State("upload-sales","filename"),
    prevent_initial_call=True,
)
def handle_sales(content, filename):
    return _handle_upload(content, filename, "sales")

@callback(
    Output("status-expenses","children"),
    Output("preview-expenses","children"),
    Input("upload-expenses","contents"),
    State("upload-expenses","filename"),
    prevent_initial_call=True,
)
def handle_expenses(content, filename):
    return _handle_upload(content, filename, "expenses")

@callback(
    Output("status-overhead","children"),
    Output("preview-overhead","children"),
    Input("upload-overhead","contents"),
    State("upload-overhead","filename"),
    prevent_initial_call=True,
)
def handle_overhead(content, filename):
    return _handle_upload(content, filename, "overhead")

@callback(
    Output("status-store_master","children"),
    Output("preview-store_master","children"),
    Input("upload-store_master","contents"),
    State("upload-store_master","filename"),
    prevent_initial_call=True,
)
def handle_store_master(content, filename):
    return _handle_upload(content, filename, "store_master")
