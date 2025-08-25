from dash import dcc, Input, Output, callback, register_page
import dash_mantine_components as dmc
import plotly.express as px
from lib.data_loader import load_all
from lib.metrics import compute_sales_gp, store_pl
from lib.allocator import allocate_overhead

register_page(
    __name__,
    path="/4_🧮_間接費配賦",
    name="🧮 間接費配賦",
    title="間接費配賦",
)

def layout():
    return dmc.Container([
        dmc.Title("🧮 HQ間接費の配賦", order=2),
        dmc.Text("基準: 売上 / 粗利 / 人員 / 面積 から選択。", size="sm", color="dimmed"),
        dmc.Space(h=10),
        dmc.SegmentedControl(
            id="alloc-basis",
            data=[
                {"label":"売上", "value":"sales"},
                {"label":"粗利", "value":"gp"},
                {"label":"人員", "value":"headcount"},
                {"label":"面積", "value":"area"},
            ],
            value="sales",
            fullWidth=True,
        ),
        dmc.Space(h=10),
        dcc.Loading(dcc.Graph(id="alloc-fig")),
    ], fluid=True)

@callback(
    Output("alloc-fig","figure"),
    Input("alloc-basis","value"),
)
def update_fig(basis):
    sales, expenses, overhead, store_master = load_all()
    sgp = compute_sales_gp(sales)
    allocated = allocate_overhead(overhead, store_master, sgp, basis=basis)
    pl = store_pl(sgp, expenses, allocated)
    fig = px.bar(pl, x="store_name", y="ebit", color="month", barmode="group",
                 title=f"店舗別EBIT（配賦基準: {basis}）")
    return fig
