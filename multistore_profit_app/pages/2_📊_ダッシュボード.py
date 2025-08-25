import pandas as pd
from dash import dcc, register_page
import dash_mantine_components as dmc
import plotly.express as px
from lib.data_loader import load_all
from lib.metrics import compute_sales_gp, monthly_kpis

register_page(
    __name__,
    path="/2_📊_ダッシュボード",
    name="📊 ダッシュボード",
    title="ダッシュボード",
)

def layout():
    sales, expenses, overhead, store_master = load_all()
    sgp = compute_sales_gp(sales)
    kpi = monthly_kpis(sgp)
    if kpi.empty:
        return dmc.Container([dmc.Text("データが不足しています。データ取込から開始してください。", color="red")], fluid=True)
    cards = dmc.SimpleGrid(cols=3, spacing="md", children=[
        _metric_card("売上", f"{kpi['revenue'].iloc[-1]:,.0f} 円"),
        _metric_card("粗利", f"{kpi['gross_profit'].iloc[-1]:,.0f} 円"),
        _metric_card("粗利率", f"{kpi['gp_margin'].iloc[-1]*100:.1f} %"),
    ])
    fig_rev = px.line(kpi, x="month", y="revenue", title="月次売上")
    fig_gp = px.line(kpi, x="month", y="gross_profit", title="月次粗利")
    return dmc.Container([
        dmc.Title("📊 主要KPI", order=2),
        dmc.Space(h=5),
        cards,
        dmc.Space(h=20),
        dmc.SimpleGrid(cols=2, children=[
            dcc.Graph(figure=fig_rev),
            dcc.Graph(figure=fig_gp),
        ]),
    ], fluid=True)

def _metric_card(label, value):
    return dmc.Card([
        dmc.Text(label, size="sm", color="dimmed"),
        dmc.Title(value, order=3)
    ], withBorder=True, shadow="xs", radius="md", p="md")
