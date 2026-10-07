import pandas as pd



df=pd.read_csv("earthquakes1.csv")
print(df)


df.isnull().sum()



df.info()

df["longitude"] = df["longitude"].round(4)
df["latitude"] = df["latitude"].round(4)
df["depth"] = df["depth"].round(2)

print(df)

def classify_risk(mag):
    if mag < 3:
        return "Low"
    elif 3 <= mag < 5:
        return "Medium"
    else:
        return "High"

df["risk_level"] = df["magnitude"].apply(classify_risk)

print(df)
print("\n")
print("_____________________________________")
print("\n")
print("Data cleaned successfully")
print("\n")
print("_____________________________________")
print("\n")

df.isnull().sum()

df.describe()
