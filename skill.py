#Dataset: Netflix Movies and TV Shows
# Records: approximately 8,800 titles in the commonly used dataset version.
# - Columns: 12.
# - Information: movie titles, TV shows, directors, countries, ratings, release years, genres, etc.*\
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Read CSV file
df = pd.read_csv("netflix_titles.csv")

# Display first 5 records
print(df.head())

#data understanding....-
# Display number of rows and columns
print("Dataset Shape:", df.shape)

# Display column names
print(df.columns)

# Display dataset information
df.info()

# Statistical description
print(df.describe())

# Check data types
print(df.dtypes)

# Check duplicate records
print("Duplicates:", df.duplicated().sum())

#data transformation
# Remove duplicate records
df = df.drop_duplicates()

# Drop unnecessary columns
df = df.drop(columns=["description", "show_id"])

# Convert date_added into datetime format
df["date_added"] = pd.to_datetime(
    df["date_added"].str.strip(),
    errors="coerce"
)

# Extract year from date_added
df["year_added"] = df["date_added"].dt.year

# Create a new column for month
df["month_added"] = df["date_added"].dt.month

# Extract numerical duration
df["duration_num"] = pd.to_numeric(
    df["duration"].str.extract(r"(\d+)")[0],
    errors="coerce"
)

print(df.head())

#file handling null values
# Check missing values
print(df.isnull().sum())
# Mean imputation for numerical duration
df["duration_num"] = df.groupby("type")["duration_num"].transform(
    lambda x: x.fillna(x.mean())
)

# Mean imputation for release year, if missing
df["release_year"] = df["release_year"].fillna(
    df["release_year"].mean()
)

# Fill missing categorical values
df["director"] = df["director"].fillna("Unknown")
df["cast"] = df["cast"].fillna("Unknown")
df["country"] = df["country"].fillna("Unknown")
df["rating"] = df["rating"].fillna("Unknown")

print("Missing values after cleaning:")
print(df.isnull().sum())

#insight generation
#A. Count movies and TV shows
content_count = df["type"].value_counts()print(content_count)


#B. Find the top 10 countries producing content
countries = df["country"].str.split(",").explode().str.strip()top_countries = countries[    countries != "Unknown"].value_counts().head(10)print(top_countries)


#C. Find the top 10 genres
genres = df["listed_in"].str.split(",").explode().str.strip()top_genres = genres.value_counts().head(10)print(top_genres)


#D. Analyze content added each year
yearly_content = df["year_added"].value_counts().sort_index()print(yearly_content)


#E. Find the oldest and newest released content
print("Oldest release year:", df["release_year"].min())

print("Newest release year:", df["release_year"].max())


#data visualization
#visualization 1: Movies vs TV Shows
plt.figure(figsize=(7, 5))
sns.countplot(data=df, x="type")
plt.title("Movies vs TV Shows on Netflix")
plt.xlabel("Content Type")plt.ylabel("Number of Titles")plt.show()

##Visualization 3: Top 10 genres
plt.figure(figsize=(10, 5))
top_genres.plot(kind="bar", color="orange")
plt.title("Top 10 Netflix Genres")
plt.xlabel("Genre")
plt.ylabel("Number of Titles")
plt.xticks(rotation=45)
plt.show()


#Visualization 4: Content added each year
plt.figure(figsize=(10, 5))
yearly_content.plot(kind="line", marker="o")
plt.title("Netflix Content Added Over the Years")
plt.xlabel("Year")
plt.ylabel("Number of Titles")
plt.grid()plt.show()


#visualization 5: Distribution of movie duration
movies = df[df["type"] == "Movie"]

plt.figure(figsize=(8, 5))

sns.histplot(movies["duration_num"], bins=30, kde=True)

plt.title("Distribution of Movie Duration")
plt.xlabel("Duration in Minutes")
plt.ylabel("Frequency")

plt.show()