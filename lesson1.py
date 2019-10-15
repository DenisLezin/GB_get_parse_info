import pandas as pd
import numpy as np

df = pd.DataFrame({'A': np.random.randint(10, 100, 10), 'B': np.random.randint(120, 210, 10)})

print(df)