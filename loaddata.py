import pandas as pd

df1 = pd.read_csv('fullstack_1.csv')
df2 = pd.read_csv('fullstack_2.csv')

df = pd.concat([df1, df2], ignore_index=True)

df.groupby('Location').size().sort_values(ascending=False)

import matplotlib.pyplot as plt

counts = df.groupby('Location').size().sort_values(ascending=False)
counts.plot(kind='bar', figsize=(10, 5))
plt.title('Number of Job Postings by Location')
plt.xlabel('Location')
plt.ylabel('Count')
plt.show()

df.groupby('Job Title').size().sort_values(ascending=False)

counts = df.groupby('Job Title').size().sort_values(ascending=False)
counts.plot(kind='pie', figsize=(10, 5), autopct='%1.1f%%')
plt.title('Percentage of Job Postings by Title')
plt.ylabel('')
plt.show()