
import pandas as pd
import plotnine as p9
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# -------------------------------------------------------
# load and prepare data
# -------------------------------------------------------

wd = Path('__file__').parent.absolute()

infl_shocks = pd.read_csv(Path(wd, 'data', 'infl_shocks.csv'))

method_quantiles = 'inverted_cdf'
quantiles = [0.95, .99]
infl_shock_quantiles = np.nanquantile(infl_shocks, q=quantiles, axis=0, method=method_quantiles)

# -------------------------------------------------------
# plotnine
# -------------------------------------------------------

data_p9 = infl_shocks[['CPILFESL_SHOCK_EXPWMA', 'CPILFESL_SHOCK_EXPSIMPLE']].dropna(axis=0)
data_p9 = data_p9.stack().reset_index()
data_p9.columns = ['Date', 'Timeseries', 'Value']
data_p9.Timeseries = data_p9['Timeseries'].replace({'CPILFESL_SHOCK_EXPWMA': 'expectation by WMA',
                        'CPILFESL_SHOCK_EXPSIMPLE': 'expectation by RW'})

plot583 = (
    p9.ggplot(data=data_p9, mapping=p9.aes(x='Date', y='Value', color='Timeseries'))
    + p9.geom_line()
    + p9.theme_538()
    # + p9.ggtitle("Unexpected US Inflation Rates")
    + p9.labs(title="Unexpected US Inflation Rates")  # , caption="This is a sample caption"
    + p9.ylab("") 
    + p9.theme(title=p9.element_text(ha='right'))
    # + p9.theme(caption=p9.element_text(
    #     size=8,
    #     margin={'r': -120, 't': -30}
    # ))
    # + p9.theme(plot_title = p9.element_text(ha="left"))
)

print(plot583)
plt.show()
