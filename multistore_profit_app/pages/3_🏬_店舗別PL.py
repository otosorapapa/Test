from dash import dcc, register_page
import dash_mantine_components as dmc
import plotly.express as px
from lib.data_loader import load_all
from lib.metrics import compute_sales_gp, store_pl
from lib.allocator import allocate_overhead

register_page(
    __name__,
    path="/3_🏬_店舗別PL",
    name="🏬 店舗別PL",
    title="店舗別PL",
)

def layout():
    sales, expenses, overhead, store_master = load_all()
    sgp = compute_sales_gp(sales)
    allocated = allocate_overhead(overhead, store_master, sgp, basis="sales")
    pl = store_pl(sgp, expenses, allocated)
    fig = px.bar(pl, x="store_name", y="ebit", color="month", title="店舗別EBIT")
    table = dmc.ScrollArea(style={"height":"350px"}, children=dmc.Table(
        [
            dmc.TableThead(dmc.TableTr([dmc.TableTh(c) for c in ["month","store_name","revenue","gross_profit","direct_opex","allocated_amount","ebit","ebit_margin"]])),
            dmc.TableTbody([
                dmc.TableTr([
                    dmc.TableTd(str(row["month"].date())),
                    dmc.TableTd(row["store_name"]),
                    dmc.TableTd(f"{row['revenue']:,.0f}"),
                    dmc.TableTd(f"{row['gross_profit']:,.0f}"),
                    dmc.TableTd(f"{row['direct_opex']:,.0f}"),
                    dmc.TableTd(f"{row['allocated_amount']:,.0f}"),
                    dmc.TableTd(f"{row['ebit']:,.0f}"),
                    dmc.TableTd(f"{row['ebit_margin']*100:.1f}%"),
                ]) for _, row in pl.sort_values(["month","store_name"]).iterrows()
            ])
        ],
        striped=True, highlightOnHover=True, withBorder=True, withColumnBorders=True
    ))
    return dmc.Container([
        dmc.Title("🏬 店舗別P/L", order=2),
        dmc.Text("配賦はデフォルトで売上基準。詳細は『間接費配賦』ページで調整可能です。", size="sm", color="dimmed"),
        dmc.Space(h=10),
        dcc.Graph(figure=fig),
        dmc.Space(h=10),
        table,
    ], fluid=True)
