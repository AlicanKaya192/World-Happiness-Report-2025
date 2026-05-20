<div align="center">

# 🌍 World Happiness Report 2025 — Data Analysis

**A comprehensive statistical analysis and visualization of global happiness patterns across 147 countries**

[![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)
[![Kaggle Dataset](https://img.shields.io/badge/Kaggle-Dataset-20BEFF?style=for-the-badge&logo=kaggle&logoColor=white)](https://www.kaggle.com/datasets/rmarbun/world-happiness-report-2025/data)
[![Matplotlib](https://img.shields.io/badge/Matplotlib-Visualizations-11557C?style=for-the-badge&logo=plotly&logoColor=white)](#-visualizations)
[![Status](https://img.shields.io/badge/Status-Complete-brightgreen?style=for-the-badge)](#)

---

*What makes a nation happy? Which factors matter most? Can money truly buy happiness?*
*This project dives deep into the data to find out.*

</div>

---

## 📖 Table of Contents

- [Overview](#-overview)
- [Key Findings](#-key-findings)
- [Visualizations](#-visualizations)
- [Methodology](#-methodology)
- [Dataset](#-dataset)
- [Project Structure](#-project-structure)
- [Prerequisites](#-prerequisites)
- [Installation & Setup](#-installation--setup)
- [Usage](#-usage)
- [Technologies](#-technologies)
- [Contributing](#-contributing)
- [License](#-license)
- [Credits & Acknowledgments](#-credits--acknowledgments)

---

## 🔭 Overview

This project performs an in-depth exploratory data analysis (EDA) of the **World Happiness Report 2025**, published by the United Nations Sustainable Development Solutions Network. The analysis examines happiness scores and their underlying determinants across **147 countries**, spanning **10 world regions**.

The pipeline reads the raw dataset, engineers custom regional classifications, computes statistical metrics, and produces **6 publication-ready visualizations** that tell a compelling story about global well-being.

> **Highlights at a glance:**
> - 📊 6 high-resolution, professionally styled charts
> - 🌐 147 countries classified into 10 geographic regions
> - 📈 Pearson correlation analysis with significance testing
> - 🔍 Z-score–based happiness paradox detection
> - 🇹🇷 Türkiye is tracked and highlighted across every visualization

---

## 🏆 Key Findings

| # | Finding | Detail |
|:-:|---------|--------|
| 🥇 | **Finland leads the world** | Finland retains its position as the happiest country on Earth |
| 💰 | **GDP is the strongest predictor** | GDP per capita shows the highest correlation with happiness (*r* ≈ 0.78+) |
| 🤝 | **Social support matters deeply** | Social support ranks as the second-strongest factor driving happiness |
| 🎁 | **Generosity ≠ Happiness** | Generosity shows the weakest correlation with national happiness scores |
| 🌍 | **Regional divides are stark** | Western Europe and North America & ANZ lead; Sub-Saharan Africa lags but shows high internal variation |
| 🔀 | **The Happiness Paradox is real** | Several countries punch well above — or below — what their GDP would predict |

### Spotlight: The Happiness Paradox 🧩

> Some nations are significantly happier than their economic output would suggest, while others — despite considerable wealth — report lower satisfaction. This analysis identifies the top outliers on both sides using z-score residual analysis, revealing that **culture, freedom, social bonds, and governance** often matter more than GDP alone.

---

## 📊 Visualizations

The analysis script generates **6 professional visualizations**, all saved to the `results/` directory at 180 DPI:

### 1. 🌟 Top 20 & Bottom 20 Happiness Rankings
**`happiness_rankings_top_bottom_20.png`**

Side-by-side horizontal bar charts displaying the 20 happiest and 20 unhappiest countries. Each bar is color-coded by region and includes 95% confidence interval error bars. Exact ladder scores are annotated alongside each bar.

---

### 2. 📦 Factor Breakdown — Top 30 Countries
**`happiness_factor_breakdown_top30.png`**

A stacked horizontal bar chart decomposing the happiness score of each top-30 country into its constituent factors: **GDP per Capita**, **Social Support**, **Healthy Life Expectancy**, **Freedom**, **Generosity**, **Low Corruption**, and **Baseline (Dystopia + Residual)**. This reveals *why* the happiest countries score high — and where they differ.

---

### 3. 🗺️ Regional Happiness Distribution
**`happiness_regional_distribution.png`**

Box-and-whisker plots for each of the 10 world regions, ordered by median happiness. Individual country data points are overlaid as scatter dots, and a dashed red line marks the global average. Sample sizes are displayed beneath each region.

---

### 4. 💵 GDP vs. Happiness Scatter Plot
**`happiness_vs_gdp_scatter.png`**

A scatter plot of GDP contribution versus Happiness Score for all 147 countries, with each point colored by region. A linear trend line is fitted, and the **Pearson correlation coefficient** is displayed in the title. Notable countries (Finland, USA, Afghanistan, Costa Rica, etc.) are labeled for context.

---

### 5. 📈 Factor Correlation Analysis
**`happiness_factor_correlations.png`**

A horizontal bar chart showing the Pearson correlation (*r*) of each of the six happiness factors with the overall happiness score. Statistical significance is indicated with stars (`*** p<0.001`, `** p<0.01`, `* p<0.05`).

---

### 6. 🔀 The Happiness Paradox — Wealth Outliers
**`happiness_paradox_wealth_outliers.png`**

A dual-panel bar chart identifying the 10 countries that are **happier than their GDP predicts** and the 10 countries that are **less happy than their GDP predicts**. The paradox score is computed as the difference between standardized happiness and standardized GDP (z-scores).

---

## 🔬 Methodology

The analysis follows a structured, reproducible pipeline:

```
Raw Data (WHR_2025.xls)
    │
    ├─ 1. Data Ingestion & Cleaning
    │       • Read Excel via xlrd engine
    │       • Standardize column names
    │       • Assign 10-region classification via custom mapping
    │
    ├─ 2. Descriptive Analysis
    │       • Rank all 147 countries by ladder score
    │       • Compute regional medians, IQRs, and distributions
    │
    ├─ 3. Correlation Analysis
    │       • Pearson correlation of each factor with happiness
    │       • p-value significance testing (scipy.stats.pearsonr)
    │       • Linear regression trend fitting (numpy.polyfit)
    │
    ├─ 4. Paradox Detection
    │       • Z-score standardization of GDP and happiness
    │       • Residual analysis: paradox = z(happiness) − z(GDP)
    │       • Top/bottom 10 outlier identification
    │
    └─ 5. Visualization (6 charts)
            • Consistent style: warm off-white palette (#FAFAF8)
            • Region-aware color coding (10-color palette)
            • Annotated labels, confidence intervals, significance markers
            • 180 DPI export for print-quality resolution
```

### Statistical Techniques

| Technique | Purpose | Library |
|-----------|---------|---------|
| Pearson Correlation | Measure linear association between factors and happiness | `scipy.stats` |
| p-Value Testing | Assess statistical significance of correlations | `scipy.stats` |
| Z-Score Standardization | Normalize GDP and happiness for paradox analysis | `scipy.stats.zscore` |
| Linear Regression | Fit GDP–happiness trend line | `numpy.polyfit` |
| Confidence Intervals | Visualize uncertainty in country rankings | Dataset-provided |

---

## 📁 Dataset

| Property | Detail |
|----------|--------|
| **Source** | [World Happiness Report 2025 — Kaggle](https://www.kaggle.com/datasets/rmarbun/world-happiness-report-2025/data) |
| **File** | `WHR_2025.xls` |
| **Format** | Excel (.xls) |
| **Countries** | 147 |
| **Key Columns** | Ladder Score, Log GDP per Capita, Social Support, Healthy Life Expectancy, Freedom, Generosity, Perceptions of Corruption, Dystopia + Residual, Upper/Lower Whiskers |

### Region Classification

Countries are grouped into **10 custom-defined regions** for geographic analysis:

```
Western Europe          │  North America & ANZ     │  Latin America
Eastern Europe          │  East Asia               │  South Asia
Middle East & N. Africa │  Sub-Saharan Africa      │  Southeast Asia
Central Asia            │                          │
```

---

## 🗂️ Project Structure

```
2025-Happiness-Report/
│
├── README.md                   # This file
├── analysis.py                 # Main analysis & visualization script
├── WHR_2025.xls                # Raw dataset (147 countries)
│
└── results/                    # Generated visualizations (180 DPI)
    ├── happiness_rankings_top_bottom_20.png
    ├── happiness_factor_breakdown_top30.png
    ├── happiness_regional_distribution.png
    ├── happiness_vs_gdp_scatter.png
    ├── happiness_factor_correlations.png
    └── happiness_paradox_wealth_outliers.png
```

---

## ⚙️ Prerequisites

- **Python 3.8+** (tested with Python 3.x)
- **pip** or any Python package manager

---

## 🚀 Installation & Setup

1. **Clone the repository**

   ```bash
   git clone https://github.com/your-username/2025-Happiness-Report.git
   cd 2025-Happiness-Report
   ```

2. **Create a virtual environment** *(recommended)*

   ```bash
   python -m venv .venv
   source .venv/bin/activate        # macOS / Linux
   .venv\Scripts\activate           # Windows
   ```

3. **Install dependencies**

   ```bash
   pip install pandas numpy matplotlib scipy xlrd
   ```

---

## ▶️ Usage

Run the full analysis pipeline with a single command:

```bash
python analysis.py
```

**Expected output:**

```
Loaded 147 countries
   country  happiness           region
0  Finland      7.736  Western Europe
...

🇹🇷 Türkiye  #87/147 — 5.324

Chart 1 saved → results/happiness_rankings_top_bottom_20.png
Chart 2 saved → results/happiness_factor_breakdown_top30.png
Chart 3 saved → results/happiness_regional_distribution.png
Chart 4 saved → results/happiness_vs_gdp_scatter.png
Chart 5 saved → results/happiness_factor_correlations.png
Chart 6 saved → results/happiness_paradox_wealth_outliers.png

All 6 charts saved to results/
```

All visualizations are saved to the `results/` folder as high-resolution PNG files.

---

## 🛠️ Technologies

| Package | Version | Purpose |
|---------|---------|---------|
| [pandas](https://pandas.pydata.org/) | latest | Data loading, wrangling, and transformation |
| [NumPy](https://numpy.org/) | latest | Numerical operations and array math |
| [Matplotlib](https://matplotlib.org/) | latest | Publication-quality chart generation |
| [SciPy](https://scipy.org/) | latest | Pearson correlation, p-values, z-scores |
| [xlrd](https://xlrd.readthedocs.io/) | latest | Legacy Excel `.xls` file reading |

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to:

1. **Fork** this repository
2. **Create** a feature branch (`git checkout -b feature/amazing-analysis`)
3. **Commit** your changes (`git commit -m 'Add new regional deep-dive'`)
4. **Push** to the branch (`git push origin feature/amazing-analysis`)
5. **Open** a Pull Request

> **Suggestions for contribution:**
> - Add time-series analysis comparing WHR 2024 → 2025 trends
> - Build an interactive dashboard (Plotly / Streamlit)
> - Add per-region deep-dive sub-analyses
> - Integrate additional datasets (e.g., HDI, Gini coefficient)

---

## 📄 License

This project is licensed under the **MIT License** — see below for details.

```
MIT License

Copyright (c) 2025

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 🙏 Credits & Acknowledgments

- **Dataset:** [World Happiness Report 2025](https://www.kaggle.com/datasets/rmarbun/world-happiness-report-2025/data) published on Kaggle by [rmarbun](https://www.kaggle.com/rmarbun)
- **Original Report:** [World Happiness Report](https://worldhappiness.report/) — an annual publication by the UN Sustainable Development Solutions Network
- **Research Foundation:** The WHR uses data from the Gallup World Poll, which surveys respondents in ~150 countries on life satisfaction (Cantril Self-Anchoring Scale)

---

> **⚠️ Disclaimer:** This project is an independent analysis created for educational and research purposes. The dataset is sourced from Kaggle and is based on the publicly available World Happiness Report 2025. The findings, interpretations, and visualizations presented here are solely those of the author and do not represent the views of the United Nations, Gallup, or any affiliated organization. The region classifications used in this analysis are custom-defined and may differ from official UN designations.

---

<div align="center">

**Made with ❤️ and Python**

*If you found this analysis insightful, consider giving it a ⭐*

</div>
