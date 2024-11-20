import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_csv('https://storage.googleapis.com/courses_data/Assignment%20CSV/finance_liquor_sales.csv')

# get data for time range
df = df[(df['date'] >= '2016-01-01') & (df['date'] <= '2019-12-31')]


# Popular Items
# group by zip code
popularsItems = df.groupby(['zip_code','item_number']).agg({'bottles_sold':'sum'})

# find most populars times
popularsItems = popularsItems.groupby(['zip_code']).max().reset_index()

# plt for popular Items
plt.subplot(2, 1, 1)

plt.scatter(popularsItems.index.values,popularsItems['bottles_sold'])
plt.xlabel("Zip Code")
plt.ylabel("Bottles Sold")
plt.title("Bottles Sold")

# Sales per store
storeSales = df.groupby(['store_name']).agg({'sale_dollars':'sum'})

totalSales = storeSales.sum()

sumarr = (storeSales * 100 )/ totalSales

sumarr = sumarr[sumarr['sale_dollars'] >= 2]

sumarr = sumarr.sort_values('sale_dollars')

# plt for sales
plt.subplot(2, 1, 2)
plt.barh(sumarr.index.values, sumarr['sale_dollars'] )

for i, value in enumerate(sumarr["sale_dollars"]):
    plt.text(value + 0.2, i - 0.2, "%.2f" % value,)

plt.xlabel("%Sales")
plt.ylabel("Store Name")
plt.title("%Sales By Store")

plt.tight_layout()
plt.show()

