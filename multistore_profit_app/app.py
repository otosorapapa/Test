import os, sys
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()

BASE = Path(__file__).resolve().parent
sys.path.append(str(BASE))

from dash import Dash, html, dcc, page_container
import dash_mantine_components as dmc

app = Dash(__name__, use_pages=True, suppress_callback_exceptions=True, title="Multi-Store Profitability")
server = app.server

app.layout = dmc.MantineProvider(
    theme={
        "fontFamily": "Inter, system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial, sans-serif",
        "primaryColor": "indigo",
    },
    children=dmc.Container([
        dmc.Header(height=60, children=dmc.Group([
            dmc.Text("🏪 Multi-Store Profitability", size="lg", weight=700),
            dmc.Divider(orientation="vertical"),
            dmc.Anchor("データ取込", href="/1_%F0%9F%93%A5_%E3%83%87%E3%83%BC%E3%82%BF%E5%8F%96%E8%BE%BC"),
            dmc.Anchor("ダッシュボード", href="/2_%F0%9F%93%8A_%E3%83%80%E3%83%83%E3%82%B7%E3%83%A5%E3%83%9C%E3%83%BC%E3%83%89"),
            dmc.Anchor("店舗別PL", href="/3_%F0%9F%8F%AC_%E5%BA%97%E8%88%97%E5%88%A5PL"),
            dmc.Anchor("間接費配賦", href="/4_%F0%9F%A7%AE_%E9%96%93%E6%8E%A5%E8%B2%BB%E9%85%8D%E8%B3%A6"),
            dmc.Anchor("シミュレーション", href="/5_%F0%9F%A7%AA_%E3%82%B7%E3%83%9F%E3%83%A5%E3%83%AC%E3%83%BC%E3%82%B7%E3%83%A7%E3%83%B3"),
        ], position="apart")),
        dmc.Space(h=10),
        dcc.Location(id="url"),
        dmc.Paper(dmc.Container([
            dcc.Loading(dmc.Group([
                dmc.Text("ページ読込中...", id="page-status", size="sm", color="dimmed")
            ], position="center"), type="circle"),
            dcc.Loading(dmc.Container(page_container)),
        ], fluid=True), p="md", radius="md", shadow="sm"),
        dmc.Space(h=20),
        dmc.Center(dmc.Text("© 2025 Multi-Store Analytics", size="xs", color="dimmed")),
    ], fluid=True)
)

if __name__ == "__main__":
    port = int(os.getenv("PORT", "8050"))
    host = os.getenv("HOST", "127.0.0.1")
    app.run_server(debug=True, host=host, port=port)
