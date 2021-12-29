import random
from pandas import DataFrame, Series
import statsmodels.formula.api as smf
import math


coin = ['H', 'T']

# make empty DataFrame
df = DataFrame(index=range(100))
df

# now fill it with a "guess"
df['guess'] = [random.choice(coin) for _ in range(100)]

# and flip
df['result'] = [random.choice(coin) for _ in range(100)]

# did we get it right or not?
df['right'] = (df['guess'] == df['result']).astype(int)

model = smf.ols(formula='right ~ C(guess)', data=df)
results = model.fit()
results.summary2()
results.pvalues[1]

random.randint(1, 10)

###########
# Exercises
###########

# 7.2
# a)
def run_sim_get_pvalue(n = 100):
    df = DataFrame(index = range(n))
    df['guess'] = [random.choice(coin) for _ in range(n)]
    df['result'] = [random.choice(coin) for _ in range(n)]
    df['right'] = (df['guess'] == df['result']).astype(int)
    model = smf.ols(data = df, formula = 'right ~ C(guess)')
    results = model.fit()
    return results.pvalues['C(guess)[T.T]']
# TEST:
run_sim_get_pvalue(10)    
# b)
pvalues = [run_sim_get_pvalue() for _ in range(1000)]
pvalues = Series(pvalues)
pvalues.mean()
# c)
def runs_till_threshold(i, p = 0.05):
    pvalue = run_sim_get_pvalue()
    if pvalue < p:
        return i
    else:
        return(runs_till_threshold(i + 1, p))
iterations = Series([runs_till_threshold(1) for _ in range(100)])
# d)
# ANS: mean is 1/p and median is -1/(log_2(1 - p)) , which evaluate to 20 and 13.51, respectively, and are reasonably close but not exactly what our model gives (gets closer for more iterations)
iterations.describe()
p = 0.05
g_mean = 1 / p
g_median = -1 / math.log(1 - p, 2)

g_mean, g_median

g_mean - iterations.mean()
g_median - iterations.median()
