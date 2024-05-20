# Import libraries
import pandas as pd, panel as pn
import hvplot.pandas # noqa

# Data loading and cleaning
df = pd.read_csv('omoku_data.csv', usecols=['Date', 'Power_time', 'Outages'], index_col='Date', parse_dates=True)

day_order = {
    0: 'Monday',
    1: 'Tuesday',
    2: 'Wednesday',
    3: 'Thursday',
    4: 'Friday',
    5: 'Saturday',
    6: 'Sunday'
    }
days = list(day_order.values())

daily_average = df['Power_time'].mean()
max_power = df['Power_time'].max()
min_power = df['Power_time'].min()

df['Day'] = df.index.dayofweek.map(day_order)
df['Power_time'] = df['Power_time'].fillna(daily_average).round(1)
df['Outages'] = df['Outages'].fillna((24-daily_average)).round(1)

# Plots
box_plot = df.hvplot.box(xlabel="Variables", ylabel="Number of hours", grid=True, title="Box Plot of Power Time and Outages")
line_plot = df.hvplot.line(y='Power_time', ylabel='Number of hours', title='Daily power supply')
density_plot = df.hvplot.kde('Power_time', xlabel='Number of hours', xlim=(0,24), yaxis=None, hover=False,
                                 title='Density distribution of power supply').opts(padding=(0,0))
weekly_group = df.groupby('Day', sort=False).mean().reindex(days)
weekly_plot = weekly_group.hvplot.bar(stacked=True, rot=45, ylabel='Number of hours', title='Average power supply by week day')

# Dashboard
pn.extension('tabulator', sizing_mode="stretch_width")

ACCENT = "#4099da"
BRAND_COLOR = ACCENT
BRAND_TEXT_ON_COLOR = "white"
CARD_STYLE = {
  "box-shadow": "rgba(50, 50, 93, 0.25) 0px 6px 12px -2px, rgba(0, 0, 0, 0.3) 0px 3px 7px -3px",
  "padding": "10px",
  "border-radius": "5px"
}
number_format = "{value:,.1f}"
styles = {
    "box-shadow": "rgba(50, 50, 93, 0.25) 0px 6px 12px -2px, rgba(0, 0, 0, 0.3) 0px 3px 7px -3px",
    "border-radius": "4px",
    "padding": "10px",
}

indicators = pn.FlexBox(
    pn.indicators.Number(
        value=daily_average,
        name="Average daily supply (Hrs)",
        default_color="gray",
        format=number_format,
        styles=styles
    ),
    pn.indicators.Number(
        value=max_power,
        name="Highest daily supply (Hrs)",
        default_color="green",
        format=number_format,
        styles=styles,
    ),
    pn.indicators.Number(
        value=min_power,
        name="Lowest daily supply (Hrs)",
        default_color="red",
        format=number_format,
        styles=styles,
    ),
)

table = pn.widgets.Tabulator(df.head(10), sizing_mode="stretch_width", name="Table")
tabs = pn.Tabs(('Daily total', line_plot), ('Weekly average', weekly_plot), ('Box plot', box_plot), ('Density distribution', density_plot), 
               styles=styles, sizing_mode="scale_both", margin=10)
logo = '<img src="https://panel.pyviz.org/_static/logo_stacked.png" width=180 height=150>'

text = f"""This is a [Panel](https://panel.holoviz.org) dashboard that shows the number of hours of power supply in Omoku, Rivers State, Nigeria.

Omoku is divided into three (3) areas in terms of power supply and this data was collected at one of the three areas.

The data was collected by calculating the total number of hours during which there was no power and subtracting it from 24 hours. 

This data was collected consecutively over a period of `{len(df)}` days."""
                        
template = pn.template.FastListTemplate(
    title="Power supply dashboard",
    sidebar=[logo, text],
    sidebar_width=250,
    main=[pn.Column('# Data Summary', indicators, '# Sample Data', table, '# Plots', tabs, sizing_mode="stretch_both")],
    main_layout=None,
    accent=ACCENT,
)

template.servable()