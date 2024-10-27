#
import pandas as pd
import plotnine as p9
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.dates import date2num
from datetime import datetime as dt

years = 100
data1 = np.random.normal(size=years).cumsum() # You can use other random functions to generate values with constraints
data2 = np.random.normal(size=years).cumsum() # You can use other random functions to generate values with constraints
tidx = pd.date_range('1920-01-01', periods=years, freq='A')
data = pd.DataFrame(data=zip(data1, data2), columns=['s1', 's2'], index=tidx)
data.columns.name = 'series'
data.index.name = 'date'
data = data.stack().reset_index()
data.rename(columns={0: 'values'}, inplace=True)


x_min1 = dt.strptime('1930-06-01', '%Y-%m-%d')  # date2num()
x_max1 = dt.strptime('1940-06-01', '%Y-%m-%d')
x_min = dt.strptime('1980-06-01', '%Y-%m-%d')
x_max = dt.strptime('2000-06-01', '%Y-%m-%d')
y_min = -1000
y_max = 1000

gg = (p9.ggplot(data=data, mapping=p9.aes(x='date', y='values'))
      + p9.geom_line(p9.aes(color='series'))

      # + p9.annotate(p9.geom_rect, xmin=x_min,
      + p9.annotate('rect', xmin=x_min,
                    xmax=x_max,
                    ymin=-np.inf, ymax=np.inf,
                    alpha=.3, fill='#595959', color=None)  #  
        )

# print(gg)

fig, _ = gg.draw(return_ggplot=True)
axes = fig.get_axes()
axs = axes[0]

axs.axvspan(xmin=x_min1, xmax=x_max1, ymin=y_min, ymax=y_max, alpha=0.1, color='blue')
axs.axhline(y = 0, color = 'black', linewidth = 1.3, alpha = .7)

# plt.draw()
plt.show()

