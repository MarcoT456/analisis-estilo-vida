# 🌆 City Lifestyle Segmentation Dataset

## 📋 Overview

This dataset simulates **global city profiles** to explore urban lifestyles through unsupervised machine learning techniques. It reflects how income, pollution, digital infrastructure, and environmental factors shape well-being across diverse urban landscapes — from dense megacities to eco-friendly small towns.

**Perfect for:** Clustering analysis, dimensionality reduction (PCA/t-SNE), correlation studies, and geographic data visualization.

---

## 🎯 Key Features

- **300 synthetic cities** across 6 major geographic regions
- **10 carefully correlated features** representing economic, environmental, and social dimensions
- **No missing values** - ready for immediate analysis
- **Realistic distributions** based on real-world urban data patterns
- **Designed for clustering** - naturally forms 4-5 distinct lifestyle archetypes

---

## 📊 Dataset Structure

### Columns Description

| Column | Type | Range | Description |
|--------|------|-------|-------------|
| `city_name` | string | - | Unique synthetic city identifier |
| `country` | string | 6 regions | Geographic region (Europe, Asia, North America, South America, Africa, Oceania) |
| `population_density` | int | 100 - 25,000 | Population per km² |
| `avg_income` | float | 300 - 7,000 | Average monthly household income (USD) |
| `internet_penetration` | float | 30 - 100 | Percentage of households with internet access |
| `avg_rent` | float | 150 - 3,000 | Average monthly apartment rent (USD) |
| `air_quality_index` | int | 20 - 180 | Air Quality Index (lower = cleaner air) |
| `public_transport_score` | float | 10 - 95 | Quality of public transportation (0-100 scale) |
| `happiness_score` | float | 2 - 9 | Subjective life satisfaction (0-10 scale) |
| `green_space_ratio` | float | 2 - 60 | Percentage of city area covered by parks/green spaces |

### File Information
- **Filename:** `city_lifestyle_dataset.csv`
- **Size:** ~300 rows × 10 columns
- **Format:** UTF-8 encoded CSV with header row
- **Missing Values:** None

---

## 🔗 Feature Correlations

The dataset is designed with realistic inter-feature relationships:

### Strong Positive Correlations (r > 0.7)
- `avg_income` ↔ `avg_rent` (+0.8) - Wealthier cities have higher housing costs
- `avg_income` ↔ `internet_penetration` (+0.7) - Digital access grows with wealth
- `population_density` ↔ `public_transport_score` (+0.7) - Dense cities invest in transit

### Moderate Correlations (0.4 < r < 0.7)
- `avg_income` ↔ `happiness_score` (+0.6) - Higher income correlates with life satisfaction
- `population_density` ↔ `air_quality_index` (+0.6) - Density increases pollution
- `green_space_ratio` ↔ `happiness_score` (+0.5) - Nature access improves well-being

### Negative Correlations
- `green_space_ratio` ↔ `air_quality_index` (-0.6) - Green spaces improve air quality
- `avg_income` ↔ `air_quality_index` (-0.4) - Wealthier cities tend to be cleaner
- `population_density` ↔ `green_space_ratio` (-0.5) - Dense cities have less green space

---

## 🌍 Regional Characteristics

Each region has distinct baseline characteristics:

| Region | Cities | Avg Income | Density | Internet % | Air Quality |
|--------|--------|------------|---------|------------|-------------|
| **Europe** | 60 | $3,500 | Medium | 88% | Good (55) |
| **Asia** | 80 | $2,500 | High | 72% | Moderate (95) |
| **North America** | 50 | $4,200 | Medium | 90% | Good (60) |
| **South America** | 40 | $1,800 | Medium-High | 65% | Moderate (75) |
| **Africa** | 35 | $900 | Low-Medium | 45% | Poor (85) |
| **Oceania** | 35 | $3,800 | Low | 92% | Excellent (40) |

---

## 🎯 Expected Clusters

The dataset naturally forms **4-5 distinct lifestyle archetypes**:

### 1️⃣ Metropolitan Tech Hubs
- **Characteristics:** High income, high density, expensive rent, excellent transport
- **Indicators:** `avg_income > $4,000`, `population_density > 7,000`, `avg_rent > $1,200`
- **Examples:** Major financial centers, tech capitals

### 2️⃣ Developing Urban Centers
- **Characteristics:** Medium density, mid-income, growing internet, poor air quality
- **Indicators:** `population_density: 3,000-8,000`, `avg_income: $1,500-$4,000`
- **Examples:** Emerging market cities

### 3️⃣ Low-Income Suburban Cities
- **Characteristics:** Low income, low density, weak infrastructure
- **Indicators:** `population_density < 1,500`, `avg_income < $1,000`, `internet_penetration < 50%`
- **Examples:** Rural/developing regions

### 4️⃣ Eco-Friendly Small Cities
- **Characteristics:** Low density, high green space, clean air, high happiness
- **Indicators:** `population_density < 2,000`, `air_quality_index < 60`, `happiness_score > 7`
- **Examples:** Sustainable Nordic towns, eco-cities

### 5️⃣ Industrial Mega-Cities
- **Characteristics:** Very high density, poor air quality, moderate income
- **Indicators:** `population_density > 10,000`, `air_quality_index > 120`, `happiness_score < 5`
- **Examples:** Manufacturing hubs, overpopulated metros

---

## 💡 Use Cases

### 🔬 Machine Learning Applications
- **K-Means Clustering:** Identify optimal number of clusters (k=4 or 5)
- **Hierarchical Clustering:** Build dendrograms to visualize city relationships
- **DBSCAN:** Detect outlier cities with unusual characteristics
- **PCA/t-SNE:** Visualize high-dimensional city data in 2D/3D space
- **Feature Engineering:** Create composite indices (e.g., livability score)

### 📈 Data Analysis Projects
- Correlation analysis between economic and environmental factors
- Regional comparison studies
- Sustainability assessment frameworks
- Urban planning insights
- Quality of life indicators

### 🗺️ Visualization Examples
- Geographic scatter maps (color by cluster/happiness)
- Correlation heatmaps
- Parallel coordinates plots
- Bubble charts (income vs. rent sized by density)
- Interactive dashboards with Plotly/Dash

---

## 🚀 Quick Start

```python
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

# Load dataset
df = pd.read_csv('city_lifestyle_dataset.csv')

# Basic exploration
print(df.head())
print(df.describe())
print(df.info())

# Correlation heatmap
plt.figure(figsize=(10, 8))
sns.heatmap(df.select_dtypes(include='number').corr(), 
            annot=True, cmap='coolwarm', center=0)
plt.title('Feature Correlation Matrix')
plt.tight_layout()
plt.show()

# Prepare data for clustering
X = df.drop(['city_name', 'country'], axis=1)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# K-Means clustering
kmeans = KMeans(n_clusters=5, random_state=42)
df['cluster'] = kmeans.fit_predict(X_scaled)

# PCA visualization
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)

plt.figure(figsize=(10, 6))
scatter = plt.scatter(X_pca[:, 0], X_pca[:, 1], 
                     c=df['cluster'], cmap='viridis', 
                     alpha=0.6, edgecolors='k', s=50)
plt.xlabel(f'PC1 ({pca.explained_variance_ratio_[0]:.2%})')
plt.ylabel(f'PC2 ({pca.explained_variance_ratio_[1]:.2%})')
plt.title('City Clusters - PCA Visualization')
plt.colorbar(scatter, label='Cluster')
plt.show()

# Cluster profiling
print(df.groupby('cluster')[X.columns].mean())
```

---

## 📚 Suggested Analyses

1. **Optimal Cluster Analysis**
   - Use Elbow Method and Silhouette Score to determine best k value
   - Compare K-Means, Agglomerative, and DBSCAN results

2. **Dimensionality Reduction**
   - Apply PCA and analyze explained variance
   - Try t-SNE for non-linear visualization
   - Create biplots to understand feature contributions

3. **Regional Patterns**
   - Group by `country` and analyze regional trends
   - Test statistical significance of regional differences (ANOVA)

4. **Predictive Modeling**
   - Predict `happiness_score` using other features (regression)
   - Build classification models for cluster assignment

5. **Outlier Detection**
   - Identify cities with unusual feature combinations
   - Analyze what makes certain cities unique

---

## 📖 Methodology

### Data Generation Process
1. **Regional Baseline:** Each region assigned characteristic base values
2. **Correlated Generation:** Features generated using multivariate normal distributions with target correlation structure
3. **Realistic Constraints:** Values clamped to realistic ranges based on global urban data
4. **Noise Injection:** 10-15% random noise added for natural variation
5. **Validation:** Correlation matrix verified against target specifications

### Quality Assurance
✅ All correlations within ±0.1 of target values  
✅ No impossible value combinations  
✅ Regional distributions match real-world patterns  
✅ Cluster separability validated through silhouette analysis  

---

## 🛠️ Tools & Libraries

**Recommended Python Stack:**
```
pandas >= 1.3.0
numpy >= 1.21.0
scikit-learn >= 1.0.0
matplotlib >= 3.4.0
seaborn >= 0.11.0
plotly >= 5.0.0 (for interactive visualizations)
```

---

## 📄 License

This dataset is released under the **Creative Commons Attribution-ShareAlike 4.0 International License (CC BY-SA 4.0)**.

You are free to:
- **Share** — copy and redistribute the material
- **Adapt** — remix, transform, and build upon the material

Under the following terms:
- **Attribution** — You must give appropriate credit
- **ShareAlike** — Derivatives must use the same license

---

## 🙏 Acknowledgments

This synthetic dataset was designed for educational purposes in machine learning and data science. While city names and values are synthetic, correlation patterns reflect real-world urban development research.

---

## 📧 Contact & Contributions

Found an interesting pattern? Have suggestions for improvements? Feel free to:
- Open an issue on the dataset discussion board
- Share your analysis notebooks
- Contribute to the community with your findings

---

## 🏆 Citation

If you use this dataset in your research or projects, please cite:

```
City Lifestyle Segmentation Dataset (2024)
Synthetic Urban Data for Clustering Analysis
Available at: https://www.kaggle.com/datasets/[your-username]/city-lifestyle-segmentation
```

---

**Happy Clustering! 🎉**

*Explore how the world's cities cluster based on lifestyle, economy, and environment.*