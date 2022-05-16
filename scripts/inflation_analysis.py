
import os
import copulas
import pandas as pd
import numpy as np
import plotnine as p9
import matplotlib.pyplot as plt
from datetime import datetime as dt
from datetime import timedelta
from fredapi import Fred
from pathlib import Path
from scipy import stats

# -------------------------------------------------------
# general settings
# -------------------------------------------------------

# %matplotlib
plt.rcParams['figure.figsize'] = [15, 10]
plt.style.use('fivethirtyeight')

data_dir = Path(__file__).resolve().parent.parent.joinpath('data')
fred_data_filename = Path(data_dir, dt.now().strftime('%Y-%m') + '_inflation_data.xlsx')

# -------------------------------------------------------
# set up Fred and time series ids
# -------------------------------------------------------
ts_ids = {'CPILFESL': 'core-cpi' , 'COMPNFB': 'wage', 'CUUR0000SA0R': 'purchasing-power', 'CPIAUCSL': 'headline-cpi'}

if not Path(fred_data_filename).is_file():

    print('file does not exists')

    fred_key = os.environ['FRED_API_KEY']
    fred = Fred(fred_key)


    # Core CPI (seasonaly adjusted): CPILFESL
    # Wage: COMPNFB
    # Health Care: ...
    #   HC: per capita overall Heath Care Expenditure (from Total National Health Expenditure study, file "National Health Expenditure by type of service and source of funds, CY")
    # FM 5-Year Breakeven inflation rates: T5YIE
    # Headline CPI: CPIAUCSL (seasonaly adjusted)

    # Wikipedia inflation:
    # English: Chart of M2 money supply growth and inflation as measured by the GNP price deflator. Data from 1875 to 1959 are taken from Appendix B of The American Business Cycle: Continuity and Change (edited by Robert Gordon). Data available here: http://www.nber.org/data/abc/. Data from 1959 onward are taken from the Fred database. Series IDs GNPDEF and MSNS. See for similar charts: http://research.stlouisfed.org/publications/review/98/11/9811wd.pdf and https://www.clevelandfed.org/Research/Commentary/1999/0801.pdf
    # Data from:
    #     NBER
    #         https://www.nber.org/research/data/tables-american-business-cycle
    #     FRED
    #         https://fred.stlouisfed.org/series/GDPDEF
    #         https://fred.stlouisfed.org/series/M2SL
    #
    # https://www.usinflationcalculator.com/inflation/historical-inflation-rates/
    # https://toewscorp.com/the-history-of-inflation-in-the-united-states/

    time_series_dict = {id: pd.DataFrame(fred.get_series(id), columns=[id]) for id in ts_ids.keys()}

    ts_frame = pd.DataFrame()
    for id in time_series_dict.keys():
        ts_frame = pd.concat([ts_frame, time_series_dict[id]], axis=1)

    ts_frame.to_excel(fred_data_filename)

else:
    ts_frame = pd.read_excel(fred_data_filename, index_col=0)


# -------------------------------------------------------
# get annual data / resample / downsample:
#
#   - https://towardsdatascience.com/resample-function-of-pandas-79b17ec82a78
#   - https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html
# -------------------------------------------------------

ts_ids.update({'PP_INV': 'headline-infl'})
# ts_frame.resample('Y').mean().tail()
# ts_frame.resample('A').last().tail()
ts_frame['PP_INV'] = ts_frame.loc[ts_frame.index[0],'CUUR0000SA0R'] / ts_frame['CUUR0000SA0R']
ts_frame.drop(['CUUR0000SA0R'], axis=1, inplace=True)

ts_annual = ts_frame.resample('AS').first()
infl_rates_annual = np.log(ts_annual).diff()
infl_rates_annual *= 100

# -------------------------------------------------------
# Plot level rates
# -------------------------------------------------------
def add_hist_event(event):

    vert_descr_level = 6
    color_text = '#43464b'  # "gray"  "black"  '#6F7378' '#43464b' '#4C4E52'
    color_range = "grey" #  "blue"  "grey"
    if isinstance(hist_dates[event], list):
        ax.axvspan(hist_dates[event][0], hist_dates[event][1], color=color_range, alpha=0.3)  # label="2009 Recession"
        plt.text(hist_dates[event][0], vert_descr_level , event,  rotation=90, verticalalignment='center', color=color_text)
    else:
        ax.axvline(hist_dates[event], color="black", linestyle="--")
        plt.text(hist_dates[event], vert_descr_level , event,  rotation=90, verticalalignment='center', color=color_text)

# .........................................................

sel_ts = ['CPILFESL', 'PP_INV']; sel_ts.append('CPIAUCSL')

ax = infl_rates_annual[sel_ts].rename(columns=ts_ids).plot()
hist_dates = {
        "World War I": ['1914-07-28', '1918-11-11'],
        "World War II": ['1939-09-01', '1945-08-15'],
        "Great inflation": ['1965-01-01', '1982-01-01'],  # https://www.federalreservehistory.org/essays/great-inflation
        "Russian invasion in Ukraine": "2022-02-24",  #  Russia invaded Ukraine on 24 February 2022
        }

add_hist_event("Russian invasion in Ukraine")
add_hist_event("Great inflation")
add_hist_event("World War II")
add_hist_event("World War I")

scen_1pc = 12
scen_5pc = 7
ax.axhline(scen_1pc, color="grey", linestyle="--")
plt.text('1925-01-01', scen_1pc , '1% scenario',  rotation=0, verticalalignment='bottom', color='black')
ax.axhline(scen_5pc, color="grey", linestyle="--")
plt.text('1925-01-01', scen_5pc , '5% scenario',  rotation=0, verticalalignment='bottom', color='black')

ax.set_ylabel('Unexpected Inflation Rates in %', color = '#43464b')

plt.style.use('fivethirtyeight')
# plt.show()

# -------------------------------------------------------
# Unexpected inflation
# -------------------------------------------------------

# col_names_ts = infl_rates_annual.columns
col_names_ts = sel_ts
infl_rates_annual = infl_rates_annual[col_names_ts]
col_names_exp_simple = [c + '_EXP_SIMPLE' for c in col_names_ts]
col_names_exp_wma = [c + '_EXP_WMA' for c in col_names_ts]
col_names_shock_expsimple = [c + '_SHOCK_EXPSIMPLE' for c in col_names_ts]
col_names_shock_expwma = [c + '_SHOCK_EXPWMA' for c in col_names_ts]

infl_rates_annual[col_names_exp_simple] = infl_rates_annual.shift()  # diff()
weights = np.arange(1, 4)[::-1]
weights = weights / weights.sum()
infl_rates_annual[col_names_exp_wma] = infl_rates_annual[col_names_ts].rolling(3, center=False).apply(lambda slice: np.dot(slice, weights))

infl_rates_annual[col_names_shock_expsimple] = infl_rates_annual[col_names_ts] - infl_rates_annual[col_names_exp_simple].values
infl_rates_annual[col_names_shock_expwma] = infl_rates_annual[col_names_ts] - infl_rates_annual[col_names_exp_wma].values

infl_rates_annual['spread-core-headline-infl'] = infl_rates_annual.CPIAUCSL - infl_rates_annual.CPILFESL

# -------------------------------------------------------
# unexpected inflation rates / shocks
# -------------------------------------------------------

is_cols_shocks = infl_rates_annual.columns[infl_rates_annual.columns.str.contains('_SHOCK')]
infl_shocks = infl_rates_annual[is_cols_shocks]


method_quantiles = 'inverted_cdf'
quantiles = [0.95, .99]
infl_quantiles = np.nanquantile(infl_rates_annual[col_names_ts], q=quantiles, axis=0, method=method_quantiles)
infl_shock_quantiles = np.nanquantile(infl_shocks, q=quantiles, axis=0, method=method_quantiles)

pd.DataFrame(infl_quantiles, index=quantiles, columns=col_names_ts)
pd.DataFrame(infl_shock_quantiles, index=quantiles, columns=infl_shocks.columns)

# Tests:
# infl_shocks[['CPILFESL_SHOCK_EXPWMA', 'CPILFESL_SHOCK_EXPSIMPLE']].hist(bins=40)

t_test_shocks = stats.ttest_1samp(infl_shocks[['CPILFESL_SHOCK_EXPWMA', 'CPILFESL_SHOCK_EXPSIMPLE']], 0, nan_policy='omit', axis=0)
t_test_shocks.pvalue

# ts_frame['PP_INV'].plot()

# interpolated = upsampled.interpolate(method='linear')
# interpolated = upsampled.interpolate(method='spline', order=2)
# see also: pad() / bfill

# -------------------------------------------------------
# Copula estimation
#   https://pypi.org/project/copulas/
#   https://github.com/sdv-dev/Copulas
# -------------------------------------------------------
