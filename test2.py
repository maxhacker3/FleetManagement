import pandas as pd

df = pd.DataFrame(columns=["Car index", "queue"])
df = pd.DataFrame(columns=["Car index", "queue"])

# Assign values using .loc
df.loc[0] = [1, [4, 2, 6]]
print(df)