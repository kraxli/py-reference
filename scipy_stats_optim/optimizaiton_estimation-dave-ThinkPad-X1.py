# import statsmodels as stats
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats as stats
from scipy.optimize import Bounds, minimize

num_sim = 10000
degrees_freedom = 3
t_loc = 0
t_scale = 1

np.random.seed(42)
draws_t_dist = stats.distributions.t.rvs(degrees_freedom, t_loc, t_scale, size=num_sim)

## default method
res01 = stats.t.fit(draws_t_dist)
# use prior knowledge for loc and scale
res02 = stats.t.fit(draws_t_dist, floc=t_loc, fscale=t_scale)


## Nelder-Mead


# Not best approach (doesn't retun object OptimizeResult) - deficiency of scipy.optimize
def optimizer_NM(func, x0=3, args=(0, 1), disp=False):
    res = minimize(func, x0, args, method="nelder-mead")
    if res.success:
        return (
            res.x
        )  # returns only the estimated degrees of freedom but not other optimization information
    raise RuntimeError("optimization routine failed")


res03 = stats.t.fit(
    draws_t_dist, method="MLE", optimizer=optimizer_NM
)  # method= MLE or MM


# Way to go / use!!
def optimizer_NM_v2(func, x0, bounds):
    return minimize(func, x0, bounds=bounds, method="nelder-mead")


bounds = dict(
    df=(0.1, 100), loc=(-100, 100), scale=(0.01, 100)
)  # x_bounds = Bounds(1, 10)
guess = dict(df=4, loc=-0.1, scale=0.5)
res_fit = stats.fit(
    stats.t, draws_t_dist, bounds=bounds, guess=guess, optimizer=optimizer_NM_v2
)
res_fit.plot()
plt.show()

## Provide manual negative log-likelihood function
res04 = minimize(
    lambda df: -np.sum(np.log(stats.t.pdf(draws_t_dist, df))),
    x0=3,
    method="Nelder-Mead",
)

print(res04)
x = 0

# TODO:
# minimize(lambda df: stats.t.nnlf(draws_t_dist, df), x0=3, method="Nelder-Mead")
# stats.t.nnlf(theta=(t_loc, t_scale), x=draws_t_dist)
# stats.t._penalized_nnlf(theta=(t_loc, t_scale), x=draws_t_dist)

# TODO:
# Gradien base optimization
# see github scipy issue 9966 (using autodiff for Jacobian and Gradient)

## Empirical maximum likelihood

# see: statsmodels
