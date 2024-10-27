# import os
# import copulas
import pandas as pd
import numpy as np
import plotnine as p9
import matplotlib.pyplot as plt
from matplotlib.dates import date2num
from datetime import datetime as dt

# from fredapi import Fred
from pathlib import Path

# from scipy import stats

plt.rcParams["figure.figsize"] = [15, 10]
plt.style.use("fivethirtyeight")

data_dir = Path(__file__).resolve().parent.parent.joinpath("data")
# fred_data_filename = Path(data_dir, dt.now().strftime('%Y-%m') + '_inflation_data.xlsx')
fred_data_filename = Path(data_dir, "2022-05_inflation_data.xlsx")


ts_frame = pd.read_excel(fred_data_filename, index_col=0)
# ts_frame.index = ts_frame.index.to_datetime()
ts_frame.index.name = "date"
ts_frame.columns.name = "ticker"

data = ts_frame
data = data.stack().reset_index()
data.rename(columns={0: "values"}, inplace=True)
data.ticker = data.ticker.astype("string")
print(data.head())

gg = (
    p9.ggplot(data=data, mapping=p9.aes(x="date", y="values"))
    + p9.geom_line()
    + p9.geom_rect(
        xmin=date2num(dt.strptime("1939-06-01", "%Y-%m-%d")),
        xmax=date2num(dt.strptime("1945-06-01", "%Y-%m-%d")),
        ymin=-np.inf,
        ymax=np.inf,
        alpha=0.01,
        fill="#595959",
        color=None,
    )
)
print(gg)

# fig, axs = gg.draw(return_ggplot=True)  # what is axs: axes or axis?
fig = gg.draw()

# ax = fig.axes[0].axvspan('1980-01-01', '1999-01-01', color="blue", alpha=0.3)
ax = fig.axes[0]
ax = ax.axvspan(
    dt.datetime(1990, 3, 1),
    dt.datetime(2019, 3, 31),
    label="March",
    color="crimson",
    alpha=0.3,
)
plt.show()


# color a single bar
# https://towardsdatascience.com/introduction-to-plotnine-as-the-alternative-of-data-visualization-package-in-python-46011ebef7fe


# ?? axs = fig.get_axes()

# ax.axvspan()
# ax.axvspan(date2num(datetime(2019,3,1)), date2num(datetime(2019,3,31)), label="March", color="crimson", alpha=0.3)

# p9.geom_rect

# color line segments / areas


# color single bar in barplot only -> todo in plotting/plotnine
