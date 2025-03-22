# Import libraries
import pandas as pd, panel as pn
import hvplot.pandas # noqa

# Data loading and manipulation
df = pd.read_csv(
    "omoku_data.csv",
    parse_dates=['Date'],
    index_col="Date",
    dtype={"Remark":pd.api.types.CategoricalDtype()}
    )
df['Day'] = df.index.day_name().astype('category')

recorded = df[df['Power_time'].notna()]
record_days = len(recorded)

days_with_power = len(recorded[recorded['Power_time'] != 0])
power_issues = recorded[recorded['Remark'].str.contains('Repairs|Maintenance', case=False, na=False)]

percent_avai = round(days_with_power/record_days *100, 1)
daily_average = recorded['Power_time'].mean()

days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
weekly_group = recorded.groupby('Day', sort=False, observed=True)[['Power_time']].mean().reindex(days)

monthly_avg = recorded['Power_time'].resample("ME").mean().reset_index().set_index("Date")
monthly_avg['Month'] = monthly_avg.index.month_name()

# Plots
line_plot = recorded.hvplot.line(y='Power_time', ylabel='Number of hours', title='Total daily power supply')
density_plot = recorded['Power_time'].hvplot.kde('Power_time', xlabel='Number of hours', xlim=(0,24), yaxis=None, hover=False,
                                                 title='Density distribution of power supply')
weekly_plot = weekly_group.hvplot.bar(rot=45, ylabel='Number of hours', title='Average power supply by week day')
monthly_plot = monthly_avg.hvplot.bar(rot=45, hover_tooltips=['Month', 'Power_time'], hover_cols=['Month'], title="Monthly average power supply")

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
        value=record_days,
        name="Number of days recorded",
        default_color="blue",
        styles=styles,
    ),
    pn.indicators.Number(
        value=daily_average,
        name="Average daily supply (Hrs)",
        default_color="gray",
        format=number_format,
        styles=styles
    ),
    pn.indicators.Number(
        value=percent_avai,
        name="Power availability rate",
        default_color="green",
        format=f"{number_format}%",
        styles=styles,
    ),
    pn.indicators.Number(
    value=len(power_issues),
    name="Days in repairs or maintenance",
    default_color="red",
    styles=styles,
    ),
)

table = pn.widgets.Tabulator(df.head(10), sizing_mode="stretch_width", name="Table")
tabs = pn.Tabs(('Daily total', line_plot), ('Monthly average', monthly_plot),
               ('Weekly average',weekly_plot), ('Density distribution', density_plot),
               styles=styles, sizing_mode="scale_both", margin=10)
logo = '<img src="https://panel.holoviz.org/_static/logo_stacked.png" width=180 height=150>'

text = f"""This is a [Panel](https://panel.holoviz.org) dashboard that shows the number of hours of power supply in Omoku, Rivers State, Nigeria.

Omoku is divided into three (3) areas in terms of power supply and this data was collected at one of the three areas.

The data was collected by calculating the total number of hours during which there was no power and subtracting it from 24 hours.

This data was collected consecutively over a period of `{len(df)}` days."""

template = pn.template.FastListTemplate(
    title="Power supply dashboard",
    sidebar=[logo, text],
    sidebar_width=250,
    main=[pn.Column('# Data Summary', indicators, '# Sample Data', table, '# Plots', tabs)],
    main_layout=None,
    accent=ACCENT,
)

template.servable()
