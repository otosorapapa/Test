from dash import dcc, Input, Output, State, callback, register_page
import dash_mantine_components as dmc
import plotly.express as px
from lib.data_loader import load_all
from lib.metrics import compute_sales_gp, store_pl
from lib.allocator import allocate_overhead
from lib.simulator import simulate_sales, break_even_point

register_page(
    __name__,
    path="/5_🧪_シミュレーション",
    name="🧪 シミュレーション",
    title="シミュレーション",
)

def layout():
    return dmc.Container([
        dmc.Title("🧪 価格×数量×コスト×ミックス：感度分析", order=2),
        dmc.SimpleGrid(cols=4, children=[
            dmc.NumberInput(label="価格変動（%）", value=0, id="sim-price"),
            dmc.NumberInput(label="数量変動（%）", value=0, id="sim-volume"),
            dmc.NumberInput(label="コスト変動（%）", value=0, id="sim-cost"),
            dmc.NumberInput(label="ミックス転換（%）", value=0, id="sim-mix"),
        ]),
        dmc.Space(h=10),
        dmc.Button("再計算", id="sim-run", variant="filled"),
        dmc.Space(h=10),
        dcc.Loading(dmc.SimpleGrid(cols=2, children=[
            dmc.Paper(dmc.Stack([dmc.Text("売上/粗利（シミュレーション）"), dcc.Graph(id="sim-fig-rev")]), p="md"),
            dmc.Paper(dmc.Stack([dmc.Text("EBIT（配賦後）"), dcc.Graph(id="sim-fig-ebit")]), p="md"),
        ])),
        dmc.Space(h=10),
        dmc.Alert(id="sim-bep", color="blue"),
    ], fluid=True)

@callback(
    Output("sim-fig-rev","figure"),
    Output("sim-fig-ebit","figure"),
    Output("sim-bep","children"),
    Input("sim-run","n_clicks"),
    State("sim-price","value"),
    State("sim-volume","value"),
    State("sim-cost","value"),
    State("sim-mix","value"),
    prevent_initial_call=True
)
def run_sim(n, price, volume, cost, mix):
    sales, expenses, overhead, store_master = load_all()
    ssim = simulate_sales(sales, price_pct=price or 0, volume_pct=volume or 0, cost_pct=cost or 0, mix_shift=mix or 0)
    sgp_sim = ssim.copy()
    alloc = allocate_overhead(
        overhead.assign(date=overhead["date"]),
        store_master,
        sgp_sim.rename(columns={"revenue_sim":"revenue","gross_profit_sim":"gross_profit","qty_sim":"qty","unit_price_sim":"unit_price","unit_cost_sim":"unit_cost"}),
        basis="sales"
    )
    pl_sim = store_pl(
        sgp_sim.rename(columns={"revenue_sim":"revenue","gross_profit_sim":"gross_profit","qty_sim":"qty"}),
        expenses,
        alloc
    )
    kpi_rev = sgp_sim.groupby("month", as_index=False).agg(revenue=("revenue_sim","sum"), gp=("gross_profit_sim","sum"))
    fig_rev = px.line(kpi_rev, x="month", y=["revenue","gp"], title="月次：売上・粗利（Sim）")
    fig_ebit = px.bar(pl_sim.groupby("store_name", as_index=False)["ebit"].sum(), x="store_name", y="ebit", title="店舗別EBIT（Sim）")
    latest = kpi_rev.iloc[-1]
    gp_margin = latest["gp"]/latest["revenue"] if latest["revenue"] != 0 else 0
    fixed_cost_val = float(expenses[expenses["fv_type"].str.lower()=="fixed"]["amount"].sum())
    bep = break_even_point(latest["revenue"], fixed_cost_val, gp_margin)
    bep_msg = f"最新月の概算BEP（売上）: {bep:,.0f} 円（粗利率 {gp_margin*100:.1f}%、固定費 {fixed_cost_val:,.0f} 円）"
    return fig_rev, fig_ebit, bep_msg
