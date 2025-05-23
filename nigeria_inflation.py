import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
df = pd.read_csv("NigeriaInflationRates.csv")

#print(df.info)

pd.set_option("display.max_columns", 20)
# print(df)

#Checked for missing values
#print(df.isnull().sum())

#Checked for the mean price in the missing columns
crude_price = df["Crude Oil Price"].mean()
# print(crude_price)

df["Crude Oil Price"] = df["Crude Oil Price"].fillna(crude_price)
# print(df.isnull().sum())

mean_price = df["Production"].mean()
# print(mean_price)

df["Production"] = df["Production"].fillna(mean_price)
# print(df.isnull().sum())

export_price = df["Crude Oil Export"].mean()
# print(export_price)

df["Crude Oil Export"] = df["Crude Oil Export"].fillna(export_price)
# print(df.isnull().sum())

#Checked for duplicate values
#print(df.duplicated())

#Converted the numeric month column
import calendar
df["Month"] = df["Month"].apply(lambda x: calendar.month_name[int(x)])
#print(df)

#1.AVERAGE INFLATION RATE IN NIGERIA(2008 - 2024)
average_inflation = round(df[(df["Year"] >= 2008) & (df["Year"] <= 2024)] ["Inflation_Rate"].mean(), 2)
#print("The average inflation rate from 2008-2024 is:",average_inflation)

#2.HIGHEST INFLATION RATE YEAR
highest_IRY = df.groupby("Year")["Inflation_Rate"].mean() .idxmax()
#print("The highest inflation rate year is:",highest_IRY)

#3.HIGHEST INFLATION MONTH
highest_IM = df.groupby("Month")["Inflation_Rate"].mean().idxmax()
#print(f"{highest_IM} recorded the highest inflation rate among all the months reviewed")

#4.INFLATION TREND DURING OIL DROP
inflation_trend = df.groupby("Year")[["Inflation_Rate", "Crude Oil Price"]].mean()

# print("Year | Oil Price (USD) | Inflation Rate (%) | Change Observation")
# print("---------------------------------------------------------------")
# print("2008 |    101.02        |      11.53          | Reference Year")
# print("2009 |     63.90        |      12.59          | Oil ↓, Inflation ↑ ✅")
# print("2014 |    100.40        |       8.06          | Reference Year")
# print("2015 |     52.65        |       9.01          | Oil ↓, Inflation ↑ ✅")
# print("2016 |     43.81        |      15.63          | Oil ↓, Inflation ↑ ✅")
# print("2019 |     65.85        |      11.39          | Reference Year")
# print("2020 |     41.89        |      13.21          | Oil ↓, Inflation ↑ ✅")

# print("\nConclusion:")
#print("During key global oil price drops (2009, 2015, 2016, 2020), Nigeria's inflation rate consistently increased.")
#print("This suggests that falling oil prices may indirectly trigger higher inflation in Nigeria through currency depreciation or fiscal constraints.")

#5.MOST INCREASED CPI OVERTIME
cpi_columns = ["CPI_Food", "CPI_Energy","CPI_Health", "CPI_Transport", "CPI_Communication", "CPI_Education"]
cpi_change = df[cpi_columns].iloc[-1] - df[cpi_columns].iloc[0]
max_category = cpi_change.idxmax()
max_value = cpi_change.max()
#print(f"The most increased CPI Category is {max_category}, with a total of {round(max_value, 3)} increase overtime.")


#VISUALIZATIONS!!!!!!!!!
import calendar
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.collections import LineCollection

# #1.AVERAGE INFLATION RATE IN NIGERIA(2008 - 2024)
plt.style.use("dark_background")
yearly_avg = df.groupby("Year")["Inflation_Rate"].mean()
average_inflation = round(df[(df["Year"] >= 2008) & (df["Year"] <= 2024)]["Inflation_Rate"].mean(), 2)

x = np.arange(1, len(yearly_avg) + 1)
y = yearly_avg.values

points = np.array([x, y]).T.reshape(-1, 1, 2)
segments = np.concatenate([points[:-1], points[1:]], axis=1)

colors = []
for i in range(len(y) - 1):
    if y[i] < 15.0:
        colors.append("red")
    elif y[i] < 20.0:
        colors.append("orange")
    else:
        colors.append("green")


fig, ax = plt.subplots(figsize=(10, 4.5))
fig.patch.set_facecolor("green")
ax.set_facecolor("white")


lc = LineCollection(segments, colors=colors, linewidths=2)
ax.add_collection(lc)

ax.plot(x, y, 'o', color="black")

for i, (xi, yi) in enumerate(zip(x, y)):
    ax.text(xi, yi + 0.02, f"{yi:.2f}%", ha='center', va='bottom', fontsize=6, color="black")

ax.set_xticks(x)
ax.set_xticklabels(yearly_avg.index, rotation=35)

ax.set_title("Average Yearly Inflation Rate in Nigeria (2008–2024)")
ax.set_xlabel("Year")
ax.set_ylabel("Inflation Rate (%)")

plt.tight_layout()

plt.text(0.5, 0.75, 'My name is Glory Iloduba \nAnd this is my Capstone Project',
         fontsize=20,
         fontweight='bold',
         fontname='Times New Roman',
         color='black',
         alpha=0.4,
         ha='center', va='top',
         transform=plt.gcf().transFigure)

# plt.show()


#2.HIGHEST INFLATION RATE YEAR
yearly_avg = df.groupby("Year")['Inflation_Rate'].mean().sort_index()
colors = plt.cm.viridis(np.linspace(0, 1, len(yearly_avg)))

fig= plt.figure(figsize=(9, 6))
bars = plt.bar(yearly_avg.index.astype(str), yearly_avg.values, color=colors)

fig.patch.set_facecolor("#800080")

plt.title("Yearly Inflation Rate (2008–2024)", color = "white")
plt.xlabel("Year", color="white")
plt.ylabel("Inflation Rate (%)", color="white")
plt.xticks(color="white")
plt.yticks(color="white")
plt.grid(False)
plt.gca().set_facecolor('white')
plt.tight_layout()

for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, height, f"{height:.2f}%",
             ha='center', va='bottom', fontsize=9, color='black')

plt.xticks(rotation=20)
# plt.show()


#3.AVERAGE INFLATION RATE PER MONTH IN NIGERIA
monthly_avg = df.groupby("Month")["Inflation_Rate"].mean()

x = np.arange(1, 13)
y = monthly_avg.values

points = np.array([x, y]).T.reshape(-1, 1, 2)
segments = np.concatenate([points[:-1], points[1:]], axis=1)

colors = []
for i in range(len(y) - 1):
    if y[i] < 14.0:
        colors.append("red")
    elif y[i] < 14.2:
        colors.append("orange")
    else:
        colors.append("green")

fig, ax = plt.subplots(figsize=(10, 5))
ax.set_facecolor("black")
lc = LineCollection(segments, colors=colors, linewidths=2)
ax.add_collection(lc)

ax.plot(x, y, 'o', color="white")

for i, (xi, yi) in enumerate(zip(x, y)):
    ax.text(xi, yi + 0.02, f"{yi:.2f}%", ha='center', va='bottom', fontsize=7, color="white")

ax.set_xticks(x)
ax.set_xticklabels([calendar.month_name[i] for i in x], rotation=35)

ax.set_title("Average Monthly Inflation Rate (2008–2024)")
ax.set_xlabel("Months")
ax.set_ylabel("Inflation Rate (%)")

plt.tight_layout()
# plt.show()


#4. INFLATION TREND DURING OIL DROP
years = np.array([2008, 2009, 2014, 2015, 2016, 2019, 2020])
oil_prices = np.array([101.02, 63.90, 100.40, 52.65, 43.81, 65.85, 41.89])
inflation_rates = np.array([11.53, 12.59, 8.06, 9.01, 15.63, 11.39, 13.21])

fig, ax1 = plt.subplots(figsize=(9,5), facecolor='black')

def plot_segments_with_inline_labels(ax, x, y, left_color, right_color, linestyle='-', dot_color='white'):
    for i in range(len(x)-1):
        color = right_color if y[i+1] > y[i] else left_color
        # Draw line segment
        ax.plot(x[i:i+2], y[i:i+2], color=color, linestyle=linestyle, marker='o')
        # Midpoint for value label
        mid_x = (x[i] + x[i+1]) / 2
        mid_y = (y[i] + y[i+1]) / 2
        ax.text(mid_x, mid_y, f"{y[i+1]:.2f}", ha='center', va='center', fontsize=8, color='black', rotation=0)

    for i in range(len(x)):
        ax.plot(x[i], y[i], 'o', color=dot_color)

# Colors
shiny_blue = '#1E90FF'
deep_blue = '#00BFFF'
yellow = 'yellow'

# X-axis styling
ax1.set_xticks(years)
ax1.set_xlabel('Year', color="white")
ax1.tick_params(axis='x', colors="white")

# Oil price: deep blue dots, solid line, black labels on line
plot_segments_with_inline_labels(ax1, years, oil_prices, 'red', 'green', linestyle='-', dot_color=deep_blue)
ax1.set_ylabel('Oil Price (USD)', color=shiny_blue)
ax1.tick_params(axis='y', colors=shiny_blue)
ax1.set_facecolor('white')

# Inflation rate: yellow dots, dashed line, black labels on line
ax2 = ax1.twinx()
plot_segments_with_inline_labels(ax2, years, inflation_rates, 'red', 'green', linestyle='--', dot_color=yellow)
ax2.set_ylabel('Inflation Rate (%)', color='tab:red')
ax2.tick_params(axis='y', colors='tab:red')

plt.title('Oil Prices and Inflation Rates(2008–2020) in Nigeria\nRed = Decrease, Green = Increase', color='white')

# plt.show()

# #5. MOST INCREASED CPI OVERTIME
from matplotlib import colormaps

cpi_columns = [col for col in df.columns if col.startswith('CPI_')]

cpi_growth = {
    col: ((df[df['Year'] == df['Year'].max()][col].mean() -
           df[df['Year'] == df['Year'].min()][col].mean()) /
           df[df['Year'] == df['Year'].min()][col].mean()) * 100
    for col in cpi_columns
}

cpi_growth_sorted = sorted(cpi_growth.items(), key=lambda x: x[1], reverse=True)

categories = [col.replace("CPI_", "") for col, _ in cpi_growth_sorted]
growth_values = [growth for _, growth in cpi_growth_sorted]
colors = colormaps['tab20'].resampled(len(categories))(range(len(categories)))

fig, ax = plt.subplots(figsize=(10, 6))
fig.patch.set_facecolor("#FFA500")
ax.set_facecolor("white")

bars = ax.barh(categories, growth_values, color=colors)
ax.invert_yaxis()

for bar in bars:
    ax.text(bar.get_width() + 2, bar.get_y() + bar.get_height()/2,
            f"{bar.get_width():.2f}%", va='center', ha='left', color='black', fontsize=9)

ax.set_title("CPI Category Growth in Nigeria (2008–2024)", fontsize=13, fontweight='bold')
ax.set_xlabel("Growth (%)")

plt.tight_layout()
# plt.show()
