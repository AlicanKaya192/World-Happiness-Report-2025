#!/usr/bin/env python3
"""
World Happiness Report 2025 — Exploratory Data Analysis
========================================================

This script performs a comprehensive visual and statistical analysis of
the 2025 World Happiness Report dataset (147 countries). It generates
six publication-quality charts that explore global happiness rankings,
the underlying factor decomposition, regional disparities, the
GDP-happiness relationship, factor correlations, and the so-called
"happiness paradox" where some nations outperform or underperform
their economic standing.

Dataset : https://www.kaggle.com/datasets/rmarbun/world-happiness-report-2025/data
Author  : Data Analysis Project
Date    : 2025
"""

import os
import sys

# Force UTF-8 encoding on stdout to avoid UnicodeEncodeError on Windows
# consoles that default to a legacy code page (e.g., cp1254 for Turkish locale).
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from scipy import stats
from scipy.stats import zscore
import warnings

# Suppress non-critical warnings (e.g., font substitution, deprecation)
# to keep the console output clean during chart generation.
warnings.filterwarnings('ignore')

# Ensure the output directory exists before we try to save any figures.
os.makedirs('results', exist_ok=True)

# ─── Global Matplotlib Theme ─────────────────────────────────────────────────
# We override the default matplotlib style to give every chart a cohesive,
# modern, editorial look: soft off-white background, thin gridlines,
# no top/right spines, and muted text colors for a clean feel.
plt.rcParams.update({
    'font.family':        'DejaVu Sans',
    'axes.spines.top':    False,
    'axes.spines.right':  False,
    'figure.facecolor':   '#FAFAF8',
    'axes.facecolor':     '#FAFAF8',
    'axes.grid':          True,
    'grid.color':         '#E8E8E3',
    'grid.linewidth':     0.6,
    'axes.labelcolor':    '#333333',
    'xtick.color':        '#555555',
    'ytick.color':        '#555555',
    'text.color':         '#222222',
})

# ─── Region Color Palette ────────────────────────────────────────────────────
# A hand-picked color for each of the 10 world regions. Chosen for
# distinctiveness in scatter plots and bar charts while remaining
# color-blind-friendly enough for most common forms of color blindness.
REGION_COLORS = {
    'Western Europe':              '#2196F3',
    'North America & ANZ':         '#4CAF50',
    'Latin America':               '#FF9800',
    'Eastern Europe':              '#9C27B0',
    'East Asia':                   '#F44336',
    'South Asia':                  '#FF5722',
    'Middle East & North Africa':  '#795548',
    'Sub-Saharan Africa':          '#607D8B',
    'Southeast Asia':              '#009688',
    'Central Asia':                '#E91E63',
}

# ─── Country-to-Region Mapping ───────────────────────────────────────────────
# The original dataset does not include a region column, so we manually
# assign each of the 147 countries to one of 10 macro-regions. This
# mapping is loosely based on the UN geoscheme with a few practical
# adjustments (e.g., Türkiye grouped with Middle East & North Africa,
# Greece with Eastern Europe for cultural proximity on this metric).
REGION_MAP = {
    'Finland':'Western Europe','Denmark':'Western Europe','Iceland':'Western Europe',
    'Sweden':'Western Europe','Netherlands':'Western Europe','Norway':'Western Europe',
    'Luxembourg':'Western Europe','Australia':'North America & ANZ',
    'New Zealand':'North America & ANZ','Switzerland':'Western Europe',
    'Belgium':'Western Europe','Ireland':'Western Europe','Austria':'Western Europe',
    'Germany':'Western Europe','United Kingdom':'Western Europe',
    'France':'Western Europe','Spain':'Western Europe','Italy':'Western Europe',
    'Portugal':'Western Europe','Malta':'Western Europe','Cyprus':'Western Europe',
    'Slovenia':'Eastern Europe','Czechia':'Eastern Europe','Lithuania':'Eastern Europe',
    'Poland':'Eastern Europe','Serbia':'Eastern Europe','Romania':'Eastern Europe',
    'Estonia':'Eastern Europe','Slovakia':'Eastern Europe','Latvia':'Eastern Europe',
    'Hungary':'Eastern Europe','Croatia':'Eastern Europe','Bulgaria':'Eastern Europe',
    'North Macedonia':'Eastern Europe','Bosnia and Herzegovina':'Eastern Europe',
    'Kosovo':'Eastern Europe','Albania':'Eastern Europe','Montenegro':'Eastern Europe',
    'Republic of Moldova':'Eastern Europe','Greece':'Eastern Europe',
    'Canada':'North America & ANZ','United States':'North America & ANZ',
    'Costa Rica':'Latin America','Mexico':'Latin America','Uruguay':'Latin America',
    'Brazil':'Latin America','El Salvador':'Latin America','Argentina':'Latin America',
    'Guatemala':'Latin America','Chile':'Latin America','Nicaragua':'Latin America',
    'Paraguay':'Latin America','Panama':'Latin America','Colombia':'Latin America',
    'Ecuador':'Latin America','Honduras':'Latin America','Peru':'Latin America',
    'Bolivia':'Latin America','Dominican Republic':'Latin America',
    'Jamaica':'Latin America','Trinidad and Tobago':'Latin America',
    'Venezuela':'Latin America','Belize':'Latin America',
    'United Arab Emirates':'Middle East & North Africa',
    'Kuwait':'Middle East & North Africa','Saudi Arabia':'Middle East & North Africa',
    'Bahrain':'Middle East & North Africa','Oman':'Middle East & North Africa',
    'Israel':'Middle East & North Africa','State of Palestine':'Middle East & North Africa',
    'Libya':'Middle East & North Africa','Algeria':'Middle East & North Africa',
    'Iran':'Middle East & North Africa','Iraq':'Middle East & North Africa',
    'Morocco':'Middle East & North Africa','Tunisia':'Middle East & North Africa',
    'Egypt':'Middle East & North Africa','Jordan':'Middle East & North Africa',
    'Lebanon':'Middle East & North Africa','Yemen':'Middle East & North Africa',
    'Mauritania':'Middle East & North Africa',
    'Taiwan Province of China':'East Asia','Japan':'East Asia',
    'Republic of Korea':'East Asia','China':'East Asia',
    'Hong Kong SAR of China':'East Asia','Mongolia':'East Asia',
    'Singapore':'Southeast Asia','Thailand':'Southeast Asia',
    'Malaysia':'Southeast Asia','Viet Nam':'Southeast Asia',
    'Philippines':'Southeast Asia','Indonesia':'Southeast Asia',
    'Lao PDR':'Southeast Asia','Cambodia':'Southeast Asia','Myanmar':'Southeast Asia',
    'Kazakhstan':'Central Asia','Uzbekistan':'Central Asia',
    'Kyrgyzstan':'Central Asia','Tajikistan':'Central Asia',
    'Azerbaijan':'Central Asia','Georgia':'Central Asia','Armenia':'Central Asia',
    'Russian Federation':'Eastern Europe','Ukraine':'Eastern Europe',
    'Türkiye':'Middle East & North Africa',
    'India':'South Asia','Pakistan':'South Asia','Nepal':'South Asia',
    'Bangladesh':'South Asia','Sri Lanka':'South Asia',
    'Nigeria':'Sub-Saharan Africa','Ghana':'Sub-Saharan Africa',
    'Kenya':'Sub-Saharan Africa','Ethiopia':'Sub-Saharan Africa',
    'Tanzania':'Sub-Saharan Africa','Uganda':'Sub-Saharan Africa',
    'Cameroon':'Sub-Saharan Africa','Senegal':'Sub-Saharan Africa',
    'Zambia':'Sub-Saharan Africa','Zimbabwe':'Sub-Saharan Africa',
    'Botswana':'Sub-Saharan Africa','South Africa':'Sub-Saharan Africa',
    'Mauritius':'Sub-Saharan Africa','Mozambique':'Sub-Saharan Africa',
    'Gabon':'Sub-Saharan Africa','Congo':'Sub-Saharan Africa',
    "Côte d'Ivoire":'Sub-Saharan Africa','Guinea':'Sub-Saharan Africa',
    'Namibia':'Sub-Saharan Africa','Niger':'Sub-Saharan Africa',
    'Chad':'Sub-Saharan Africa','Burkina Faso':'Sub-Saharan Africa',
    'Benin':'Sub-Saharan Africa','Somalia':'Sub-Saharan Africa',
    'Mali':'Sub-Saharan Africa','Togo':'Sub-Saharan Africa',
    'Liberia':'Sub-Saharan Africa','Madagascar':'Sub-Saharan Africa',
    'Eswatini':'Sub-Saharan Africa','Lesotho':'Sub-Saharan Africa',
    'Comoros':'Sub-Saharan Africa','DR Congo':'Sub-Saharan Africa',
    'Malawi':'Sub-Saharan Africa','Sierra Leone':'Sub-Saharan Africa',
    'Afghanistan':'South Asia',
}

# ── Load & Prepare the Dataset ───────────────────────────────────────────────
# Read the Excel file (XLS format requires the xlrd engine). We strip any
# stray whitespace from column headers and rename them to shorter, more
# Pythonic labels for easier downstream use.
df = pd.read_excel('WHR_2025.xls', engine='xlrd')
df.columns = df.columns.str.strip()
df = df.rename(columns={
    'Country name':                               'country',
    'Ladder score':                               'happiness',
    'upperwhisker':                               'upper',
    'lowerwhisker':                               'lower',
    'Explained by: Log GDP per capita':           'gdp',
    'Explained by: Social support':               'social',
    'Explained by: Healthy life expectancy':      'life_exp',
    'Explained by: Freedom to make life choices': 'freedom',
    'Explained by: Generosity':                   'generosity',
    'Explained by: Perceptions of corruption':    'corruption',
    'Dystopia + residual':                        'dystopia',
})

# Assign a region to each country using our custom mapping.
# Countries not found in the map get labeled 'Other'.
df['region'] = df['country'].map(REGION_MAP).fillna('Other')

# The dataset arrives pre-sorted by Ladder score (descending), so a simple
# sequential index gives us an accurate global happiness rank.
df['rank']   = range(1, len(df) + 1)

print(f"Loaded {len(df)} countries")
print(df[['country','happiness','region']].head(10))

# ── Türkiye Quick Reference ─────────────────────────────────────────────────
# We extract Türkiye's rank and score once upfront so that we can annotate
# every chart with a consistent callout badge. This provides an anchor
# point of personal interest throughout the analysis.
tr = df[df['country'] == 'Türkiye'].iloc[0]
TR_RANK  = int(tr['rank'])
TR_SCORE = float(tr['happiness'])
TR_LABEL = f'🇹🇷 Türkiye  #{TR_RANK}/147 — {TR_SCORE:.3f}'
print(f"\n{TR_LABEL}\n")

# ═══════════════════════════════════════════════════════════════════════════════
# CHART 1 — Top 20 & Bottom 20 Happiness Rankings
# ═══════════════════════════════════════════════════════════════════════════════
# Side-by-side horizontal bar charts comparing the 20 happiest and 20
# unhappiest countries, with 95% confidence interval error bars drawn
# from the upper/lower whisker values published in the report.
top20 = df.head(20).copy()
bot20 = df.tail(20).copy()

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
fig.patch.set_facecolor('#FAFAF8')
for ax in [ax1, ax2]:
    ax.set_facecolor('#FAFAF8')

# --- Left panel: Top 20 Happiest ---
# Color each bar by the country's region for quick visual grouping.
top_colors = [REGION_COLORS.get(r, '#999') for r in top20['region']]
bars1 = ax1.barh(top20['country'][::-1], top20['happiness'][::-1],
                 color=top_colors[::-1], alpha=0.88,
                 edgecolor='white', linewidth=0.8)

# Overlay 95% confidence intervals from the WHR methodology.
ax1.errorbar(
    top20['happiness'][::-1], range(len(top20)),
    xerr=[top20['happiness'][::-1].values - top20['lower'][::-1].values,
          top20['upper'][::-1].values - top20['happiness'][::-1].values],
    fmt='none', color='#555', capsize=3, linewidth=1, zorder=4
)

# Add numeric labels at the end of each bar for precise reading.
for bar, val in zip(bars1, top20['happiness'][::-1]):
    ax1.text(bar.get_width() + 0.04, bar.get_y() + bar.get_height()/2,
             f'{val:.3f}', va='center', fontsize=8.5, fontweight='bold', color='#333')
ax1.set_xlim(5.5, 8.6)
ax1.set_xlabel('Happiness Score (Ladder Score)', fontsize=10)
ax1.set_title('🌟 Top 20 Happiest Countries\n2025 World Happiness Report',
              fontsize=12, fontweight='bold', pad=12)

# --- Right panel: Bottom 20 Unhappiest ---
bot_colors = [REGION_COLORS.get(r, '#999') for r in bot20['region']]
bars2 = ax2.barh(bot20['country'][::-1], bot20['happiness'][::-1],
                 color=bot_colors[::-1], alpha=0.88,
                 edgecolor='white', linewidth=0.8)
ax2.errorbar(
    bot20['happiness'][::-1], range(len(bot20)),
    xerr=[bot20['happiness'][::-1].values - bot20['lower'][::-1].values,
          bot20['upper'][::-1].values - bot20['happiness'][::-1].values],
    fmt='none', color='#555', capsize=3, linewidth=1, zorder=4
)
for bar, val in zip(bars2, bot20['happiness'][::-1]):
    ax2.text(bar.get_width() + 0.04, bar.get_y() + bar.get_height()/2,
             f'{val:.3f}', va='center', fontsize=8.5, fontweight='bold', color='#333')
ax2.set_xlim(1.2, 4.8)
ax2.set_xlabel('Happiness Score (Ladder Score)', fontsize=10)
ax2.set_title('💔 Bottom 20 Unhappiest Countries\n2025 World Happiness Report',
              fontsize=12, fontweight='bold', pad=12)

# Shared region legend placed at the bottom of the figure.
legend_patches = [mpatches.Patch(color=c, label=r)
                  for r, c in REGION_COLORS.items()
                  if r in df['region'].unique()]
fig.legend(handles=legend_patches, loc='lower center', ncol=5,
           fontsize=8, title='Region', title_fontsize=9,
           bbox_to_anchor=(0.5, -0.04), framealpha=0.9)

# Source citation for academic credibility.
ax1.text(0.02, -0.07,
         'Source: World Happiness Report 2025 | Error bars show 95% confidence interval',
         transform=ax1.transAxes, fontsize=7.5, color='#888', style='italic')

# Türkiye badge — a fixed callout that appears on every chart for context.
fig.text(0.5, -0.06, TR_LABEL,
         ha='center', fontsize=10, fontweight='bold',
         color='#C62828',
         bbox=dict(boxstyle='round,pad=0.4', facecolor='#FFF8E1',
                   edgecolor='#E53935', linewidth=1.2))

plt.tight_layout()
plt.savefig('results/happiness_rankings_top_bottom_20.png', dpi=180,
            bbox_inches='tight', facecolor='#FAFAF8')
plt.close()
print("Chart 1 saved → results/happiness_rankings_top_bottom_20.png")

# ═══════════════════════════════════════════════════════════════════════════════
# CHART 2 — Factor Breakdown for the Top 30 Countries
# ═══════════════════════════════════════════════════════════════════════════════
# A stacked horizontal bar chart decomposing each country's happiness score
# into its constituent factors. This is a core visualization because it
# shows *why* a country ranks where it does, not just its total score.
# The "Baseline" segment (Dystopia + residual) represents the theoretical
# minimum plus any unexplained variance.
top30 = df.head(30).copy().iloc[::-1].reset_index(drop=True)

# Ordered factor columns, their display labels, and distinct segment colors.
factors     = ['gdp','social','life_exp','freedom','generosity','corruption','dystopia']
factor_lbls = ['GDP','Social Support','Life Expectancy','Freedom','Generosity','Low Corruption','Baseline']
factor_cols = ['#1976D2','#388E3C','#F57C00','#7B1FA2','#E64A19','#00796B','#CFD8DC']

fig, ax = plt.subplots(figsize=(13, 11))
fig.patch.set_facecolor('#FAFAF8')
ax.set_facecolor('#FAFAF8')

# Build the stacked bars by accumulating a running left-offset for each factor.
lefts = np.zeros(len(top30))
for fac, lbl, col in zip(factors, factor_lbls, factor_cols):
    vals = top30[fac].fillna(0).values
    ax.barh(top30['country'], vals, left=lefts, color=col,
            label=lbl, alpha=0.88, edgecolor='white', linewidth=0.4)
    lefts += vals

# Place the total happiness score as a label at the right edge of each bar.
for i, (_, row) in enumerate(top30.iterrows()):
    ax.text(row['happiness'] + 0.05, i, f"{row['happiness']:.3f}",
            va='center', fontsize=8, fontweight='bold', color='#333')

ax.set_xlabel('Happiness Score Contribution', fontsize=11)
ax.set_title("What Drives Happiness in the World's Top 30 Countries?\nFactor Breakdown — WHR 2025",
             fontsize=14, fontweight='bold', pad=15)
ax.legend(loc='lower right', fontsize=9, framealpha=0.9, edgecolor='#ddd')
ax.set_xlim(0, 10.5)
ax.text(0.01, -0.04,
        'Source: World Happiness Report 2025 | Each segment shows factor contribution.',
        transform=ax.transAxes, fontsize=7.5, color='#888', style='italic')

# Türkiye callout badge — placed just below the chart title so it
# doesn't overlap with the factor legend in the lower-right corner.
fig.text(0.5, 0.925, TR_LABEL,
         ha='center', fontsize=9, fontweight='bold',
         color='#C62828',
         bbox=dict(boxstyle='round,pad=0.4', facecolor='#FFF8E1',
                   edgecolor='#E53935', linewidth=1.2))

plt.tight_layout()
plt.savefig('results/happiness_factor_breakdown_top30.png', dpi=180,
            bbox_inches='tight', facecolor='#FAFAF8')
plt.close()
print("Chart 2 saved → results/happiness_factor_breakdown_top30.png")

# ═══════════════════════════════════════════════════════════════════════════════
# CHART 3 — Regional Distribution (Box + Swarm Plot)
# ═══════════════════════════════════════════════════════════════════════════════
# Box plots overlaid with jittered scatter points to reveal both the
# summary statistics (median, IQR) and the individual country-level
# variation within each region. Regions are ordered by descending median
# so the visual hierarchy reads left-to-right from happiest to least happy.
region_order = (df.groupby('region')['happiness']
                  .median()
                  .sort_values(ascending=False)
                  .index.tolist())
region_order = [r for r in region_order if r != 'Other']

fig, ax = plt.subplots(figsize=(13, 7))
fig.patch.set_facecolor('#FAFAF8')
ax.set_facecolor('#FAFAF8')

# Build the data list in region order for matplotlib's boxplot function.
data_by_region = [df[df['region'] == r]['happiness'].values for r in region_order]
bp = ax.boxplot(data_by_region, vert=True, patch_artist=True,
                medianprops=dict(color='white', linewidth=2),
                whiskerprops=dict(linewidth=1.2),
                capprops=dict(linewidth=1.2),
                flierprops=dict(marker='o', markersize=4, alpha=0.5))

# Color each box to match our region palette.
for patch, region in zip(bp['boxes'], region_order):
    patch.set_facecolor(REGION_COLORS.get(region, '#999'))
    patch.set_alpha(0.82)

# Overlay individual country dots with slight horizontal jitter to avoid overlap.
for i, (region, box_data) in enumerate(zip(region_order, data_by_region), 1):
    x = np.random.normal(i, 0.06, size=len(box_data))
    ax.scatter(x, box_data, alpha=0.45,
               color=REGION_COLORS.get(region, '#999'), s=22, zorder=3)

    # Highlight Türkiye with a prominent star marker in its own region.
    if region == df[df['country'] == 'Türkiye']['region'].values[0]:
        tr_idx = i
        ax.scatter([i], [TR_SCORE], color='#E53935', s=90, zorder=6,
                   marker='*', edgecolors='white', linewidths=0.5)
        ax.annotate(f'#{TR_RANK} Türkiye\n{TR_SCORE:.3f}',
                    xy=(i, TR_SCORE),
                    xytext=(i + 0.35, TR_SCORE + 0.12),
                    fontsize=8, fontweight='bold', color='#C62828',
                    arrowprops=dict(arrowstyle='->', color='#E53935', lw=1))

# Show the sample size (n) below each box for quick reference.
for i, (region, d) in enumerate(zip(region_order, data_by_region), 1):
    ax.text(i, df['happiness'].min() - 0.15, f'n={len(d)}',
            ha='center', fontsize=8, color='#888')

ax.set_xticks(range(1, len(region_order)+1))
ax.set_xticklabels(region_order, rotation=22, ha='right', fontsize=9)
ax.set_ylabel('Happiness Score (Ladder Score)', fontsize=11)
ax.set_title('How Happy Is Each Region of the World?\nDistribution by Region — WHR 2025',
             fontsize=14, fontweight='bold', pad=15)

# Draw a horizontal reference line at the global average for easy comparison.
world_avg = df['happiness'].mean()
ax.axhline(world_avg, color='#E53935', linestyle='--', linewidth=1.2, alpha=0.7)
ax.text(len(region_order) + 0.3, world_avg,
        f'World avg\n{world_avg:.2f}', fontsize=8, color='#E53935', va='center')

ax.text(0.01, -0.12,
        'Source: World Happiness Report 2025 | Each dot is a country. Box shows median and IQR.',
        transform=ax.transAxes, fontsize=7.5, color='#888', style='italic')

plt.tight_layout()
plt.savefig('results/happiness_regional_distribution.png', dpi=180,
            bbox_inches='tight', facecolor='#FAFAF8')
plt.close()
print("Chart 3 saved → results/happiness_regional_distribution.png")

# ═══════════════════════════════════════════════════════════════════════════════
# CHART 4 — GDP vs Happiness Scatter Plot
# ═══════════════════════════════════════════════════════════════════════════════
# The classic "does money buy happiness?" question, visualized as a
# scatter plot of each country's GDP contribution against its overall
# happiness score. A linear trend line and Pearson's r quantify the
# strength of the relationship. Notable outliers are labeled individually.
fig, ax = plt.subplots(figsize=(12, 7))
fig.patch.set_facecolor('#FAFAF8')
ax.set_facecolor('#FAFAF8')

# Plot each region as a separate scatter series for a clean legend.
for region in df['region'].unique():
    if region == 'Other':
        continue
    sub = df[df['region'] == region]
    ax.scatter(sub['gdp'], sub['happiness'],
               c=REGION_COLORS.get(region, '#999'),
               s=65, alpha=0.82, edgecolors='white',
               linewidths=0.6, label=region, zorder=3)

# Compute the Pearson correlation and overlay a least-squares trend line.
r_val, p_val = stats.pearsonr(df['gdp'], df['happiness'])
m, b = np.polyfit(df['gdp'], df['happiness'], 1)
xline = np.linspace(df['gdp'].min(), df['gdp'].max(), 200)
ax.plot(xline, m*xline + b, color='#333', linewidth=1.8,
        linestyle='--', alpha=0.45, zorder=2)

# Annotate a hand-picked set of countries that represent interesting
# extremes or familiar reference points for most readers.
highlights = ['Finland','United States','Afghanistan','Lebanon','India',
              'China','Japan','Costa Rica','Zimbabwe','Singapore','Brazil','Türkiye']
for _, row in df[df['country'].isin(highlights)].iterrows():
    label = f"#{int(row['rank'])} {row['country']}" if row['country'] == 'Türkiye' else row['country']
    color = '#C62828' if row['country'] == 'Türkiye' else '#333'
    weight = 'bold' if row['country'] == 'Türkiye' else 'normal'
    ax.annotate(label, xy=(row['gdp'], row['happiness']),
                xytext=(4, 3), textcoords='offset points',
                fontsize=8, color=color, alpha=0.9, fontweight=weight)

# Make Türkiye stand out with a larger star marker.
tr_row = df[df['country'] == 'Türkiye'].iloc[0]
ax.scatter([tr_row['gdp']], [tr_row['happiness']], color='#E53935',
           s=100, zorder=6, marker='*', edgecolors='white', linewidths=0.5)

ax.set_xlabel('GDP per Capita Contribution (Log scale)', fontsize=11)
ax.set_ylabel('Happiness Score (Ladder Score)', fontsize=11)
ax.set_title(f'Wealth vs Happiness: How Strong Is the Link?\n147 Countries — WHR 2025  |  r = {r_val:.2f}',
             fontsize=14, fontweight='bold', pad=15)
ax.legend(title='Region', bbox_to_anchor=(1.02, 1), loc='upper left',
          fontsize=8.5, title_fontsize=9, framealpha=0.9, edgecolor='#ddd')
ax.text(0.02, 0.04,
        'Source: World Happiness Report 2025 | Dashed line = linear trend',
        transform=ax.transAxes, fontsize=7.5, color='#888', style='italic')

plt.tight_layout()
plt.savefig('results/happiness_vs_gdp_scatter.png', dpi=180,
            bbox_inches='tight', facecolor='#FAFAF8')
plt.close()
print("Chart 4 saved → results/happiness_vs_gdp_scatter.png")

# ═══════════════════════════════════════════════════════════════════════════════
# CHART 5 — Factor-Happiness Correlation Coefficients
# ═══════════════════════════════════════════════════════════════════════════════
# A compact horizontal bar chart of Pearson r-values showing which of the
# six WHR factors correlates most strongly with the overall happiness score.
# Significance stars follow the standard convention (*** p<0.001, etc.).
factor_names = {
    'gdp':        'GDP per Capita',
    'social':     'Social Support',
    'life_exp':   'Healthy Life Expectancy',
    'freedom':    'Freedom to Make Choices',
    'generosity': 'Generosity',
    'corruption': 'Low Corruption',
}

# Compute Pearson's r and the associated p-value for each factor.
corr_rows = []
for col, name in factor_names.items():
    r, p = stats.pearsonr(df[col].fillna(0), df['happiness'])
    corr_rows.append({'Factor': name, 'r': r, 'p': p})

corr_df = pd.DataFrame(corr_rows).sort_values('r', ascending=True)

fig, ax = plt.subplots(figsize=(10, 6))
fig.patch.set_facecolor('#FAFAF8')
ax.set_facecolor('#FAFAF8')

# Color bars green for positive correlation, red for negative.
bar_colors = ['#4CAF50' if r > 0 else '#F44336' for r in corr_df['r']]
bars = ax.barh(corr_df['Factor'], corr_df['r'],
               color=bar_colors, alpha=0.88,
               edgecolor='white', linewidth=0.8)

# Annotate each bar with the exact r-value and significance level.
for bar, (_, row) in zip(bars, corr_df.iterrows()):
    sig = '***' if row['p'] < 0.001 else ('**' if row['p'] < 0.01 else '*')
    offset = 0.01 if row['r'] > 0 else -0.01
    ha = 'left' if row['r'] > 0 else 'right'
    ax.text(row['r'] + offset, bar.get_y() + bar.get_height()/2,
            f"r = {row['r']:.2f} {sig}",
            va='center', fontsize=10, fontweight='bold', color='#333', ha=ha)

ax.axvline(0, color='#333', linewidth=1)
ax.set_xlabel('Pearson Correlation Coefficient (r)', fontsize=11)
ax.set_title("What Drives Happiness the Most?\nCorrelation of Each Factor with Happiness Score — WHR 2025",
             fontsize=14, fontweight='bold', pad=15)
ax.set_xlim(-0.2, 1.0)

# Significance legend in the bottom-right corner.
ax.text(0.98, 0.04, '*** p<0.001   ** p<0.01   * p<0.05',
        transform=ax.transAxes, fontsize=8, color='#888', style='italic', ha='right')
ax.text(0.01, -0.08,
        'Source: World Happiness Report 2025',
        transform=ax.transAxes, fontsize=7.5, color='#888', style='italic')

# Türkiye callout badge — placed to the right of the x-axis label
# so it doesn't overlap with the correlation bars near 0.8–1.0.
ax.text(0.99, -0.08, TR_LABEL,
        transform=ax.transAxes, ha='right', va='top', fontsize=9, fontweight='bold',
        color='#C62828',
        bbox=dict(boxstyle='round,pad=0.4', facecolor='#FFF8E1',
                  edgecolor='#E53935', linewidth=1.2))

plt.tight_layout()
plt.savefig('results/happiness_factor_correlations.png', dpi=180,
            bbox_inches='tight', facecolor='#FAFAF8')
plt.close()
print("Chart 5 saved → results/happiness_factor_correlations.png")

# ═══════════════════════════════════════════════════════════════════════════════
# CHART 6 — The Happiness Paradox (Over/Under-Performers vs GDP)
# ═══════════════════════════════════════════════════════════════════════════════
# Not every country's happiness follows the money. We standardize both
# the happiness score and the GDP contribution to z-scores, then compute
# the difference (paradox = happy_z − gdp_z). Countries with a large
# positive paradox are *happier than their wealth predicts*, while those
# with a large negative paradox are *less happy than expected given their
# economic standing*. This highlights the power of non-economic factors.

# Standardize both variables to make them directly comparable.
df['gdp_z']   = zscore(df['gdp'])
df['happy_z'] = zscore(df['happiness'])
df['paradox'] = df['happy_z'] - df['gdp_z']

# Select the 10 biggest overachievers and 10 biggest underachievers.
over  = df.nlargest(10, 'paradox')[['country','happiness','gdp','region','paradox']]
under = df.nsmallest(10, 'paradox')[['country','happiness','gdp','region','paradox']]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))
fig.patch.set_facecolor('#FAFAF8')
for ax in [ax1, ax2]:
    ax.set_facecolor('#FAFAF8')

def dual_bar(ax, data, gdp_color, hap_color, title):
    """
    Draw paired horizontal bars for GDP contribution and happiness score
    side by side. This makes it visually obvious when the two values diverge.
    """
    countries = data['country'].values[::-1]
    gdp_vals  = data['gdp'].values[::-1]
    hap_vals  = data['happiness'].values[::-1]
    y = np.arange(len(countries))
    h = 0.35
    ax.barh(y + h/2, gdp_vals, h, color=gdp_color,
            alpha=0.65, label='GDP Contribution', edgecolor='white')
    ax.barh(y - h/2, hap_vals, h, color=hap_color,
            alpha=0.65, label='Happiness Score', edgecolor='white')
    ax.set_yticks(y)
    ax.set_yticklabels(countries, fontsize=9)
    ax.set_title(title, fontsize=12, fontweight='bold', pad=12)
    ax.legend(fontsize=9, framealpha=0.9)

# Left panel: countries punching above their GDP weight (happy despite low GDP).
dual_bar(ax1, over,  '#90CAF9', '#A5D6A7',
         '🌿 Happier Than Their Wealth Predicts\n(Punching above their GDP weight)')

# Right panel: countries punching below their GDP weight (unhappy despite high GDP).
dual_bar(ax2, under, '#90CAF9', '#EF9A9A',
         '💰 Less Happy Than Their Wealth Predicts\n(Punching below their GDP weight)')

# Source citations for both panels.
for ax in [ax1, ax2]:
    ax.text(0.01, -0.06,
            'Source: World Happiness Report 2025 | Paradox score = happiness z-score minus GDP z-score',
            transform=ax.transAxes, fontsize=7.5, color='#888', style='italic')

# Türkiye callout badge centered below the figure.
fig.text(0.5, -0.04, TR_LABEL,
         ha='center', fontsize=10, fontweight='bold',
         color='#C62828',
         bbox=dict(boxstyle='round,pad=0.4', facecolor='#FFF8E1',
                   edgecolor='#E53935', linewidth=1.2))

plt.suptitle('The Happiness Paradox: Countries That Defy the Wealth Rule — WHR 2025',
             fontsize=15, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig('results/happiness_paradox_wealth_outliers.png', dpi=180,
            bbox_inches='tight', facecolor='#FAFAF8')
plt.close()
print("Chart 6 saved → results/happiness_paradox_wealth_outliers.png")

print("\nAll 6 charts saved to results/")