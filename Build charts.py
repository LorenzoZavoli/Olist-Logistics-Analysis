import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns # Seaborn makes life much easier compared to pure matplotlib!

# Input/Output folder
IN = "data"
OUT = "images"

# ================================================================
# Chart 1: Satisfaction vs Delivery Time (Bars + Line)
# ================================================================

df1 = pd.read_csv(f"{IN}/tab_delivery_bracket.csv")

df1["delivery_braket"] = df1["delivery_braket"].replace({
    "1. within 1 week delivery": "1-7 ",
    "2. within 2 weeks delivery": "8-14",
    "3. within 3 weeks delivery": "15-21",
    "4. within 4 weeks delivery": "22-28",
    "5. 4+ weeks delivery": "29+", 
})
fig, ax1 = plt.subplots(figsize=(10, 6))
ax1.bar(df1["delivery_braket"], df1["deliveries_number"], color="#cfe0e8")
ax1.set_ylabel("Number of orders", fontsize=14, labelpad = 10)
ax1.set_xlabel("Delivery time bracket (days)", fontsize=14, labelpad = 10)
ax1.tick_params(axis="both", labelsize=13)
ax2 = ax1.twinx()
ax2.plot(df1["delivery_braket"], df1["avg_review_score"], color="#1f3b57", marker="o", label="Avg Score", linewidth=2)
ax2.set_ylabel("Average review score (1-5)", fontsize=14, labelpad = 10)
ax2.set_ylim(1, 5)
ax2.tick_params(axis="both", labelsize=13)
for i in range(len(df1)):
    x = df1["delivery_braket"][i]
    y = df1["avg_review_score"][i]
    ax2.text(x, y + 0.1, f"{y:.1f}", ha="center", va="bottom", fontweight="bold", color="#1f3b57")


plt.title("Customer satisfaction vs Delivery time", fontweight = "bold", fontsize=16, pad=10)
plt.xticks(rotation=45) # Rotate bottom labels if they are too long
plt.tight_layout() 
plt.savefig(f"{OUT}/01_score_delivery.png")
plt.close()


# ================================================================
# Chart 2: Satisfaction vs Delay
# ================================================================
df2 = pd.read_csv(f"{IN}/tab_delay_bracket.csv")
df2["delay_braket"] = df2["delay_braket"].replace({
    "1. no delay": "0",
    "2. within 1 week delay": "1-7",
    "3. within 2 weeks delay": "8-14",
    "4. within 3 weeks delay": "15-21",
    "5. 3+ weeks delay": "22+",
})

fig, ax1 = plt.subplots(figsize=(10, 6))
ax1.bar(df2["delay_braket"], df2["deliveries_number"], color="#cfe0e8")
ax1.set_ylabel("Number of orders", fontsize=14, labelpad = 10)
ax1.set_xlabel("Delay bracket (days)", fontsize=14, labelpad = 10)
ax1.tick_params(axis="both", labelsize=13)
ax2 = ax1.twinx()
ax2.plot(df2["delay_braket"], df2["avg_review_score"], color="teal", marker="o", linewidth=2)
ax2.set_ylabel("Average review score (1-5)", fontsize=14, labelpad = 10)
ax2.set_ylim(1, 5)
ax2.tick_params(axis="both", labelsize=13)
for i in range(len(df2)):
    x = df2["delay_braket"][i]
    y = df2["avg_review_score"][i]
    ax2.text(x, y + 0.1, f"{y:.1f}", ha="center", va="bottom", fontweight="bold", color="teal")

plt.title("Customer satisfaction vs Delay", fontweight = "bold", fontsize=16, pad=10)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(f"{OUT}/02_score_delay.png")
plt.close()


# ================================================================
# Chart 3: Revenue at Risk by State 
# ================================================================
states = pd.read_csv(f"{IN}/tab_impact_revenue.csv").fillna(0)

# Sort states from best to worst by % of revenue at risk
states_sorted = states.sort_values(by="pct_revenue_at_risk", ascending=False)
bench = pd.read_csv(f"{IN}/tab_Brazil_benchmark.csv").iloc[0]
states_sorted["Performance"] = ["Above national average" if x > bench["pct_revenue_at_risk"] else "Below national average" for x in states_sorted["pct_revenue_at_risk"]]

plt.figure(figsize=(8, 10))
ax = sns.barplot(data=states_sorted, x="pct_revenue_at_risk", y="customer_state", hue="Performance", dodge=False, palette={"Above national average": "#e76f51", "Below national average": "#2a9d8f"})
ax.tick_params(axis="both", labelsize=13)

plt.title("Percentage of revenue at risk by state", fontsize=16, fontweight="bold", pad=10)
plt.xlabel("% State revenue at risk (review scores <= 2)", fontsize=14, labelpad=10)
plt.ylabel("", fontsize=14)
plt.axvline(bench["pct_revenue_at_risk"], color="black", linestyle="--", linewidth=1.5, label=f"Brazil average: {bench['pct_revenue_at_risk']:.1f}%")
plt.legend(loc="lower right", fontsize=11)
plt.tight_layout()
plt.savefig(f"{OUT}/03_revenue_risk_state.png")
plt.close()


# ================================================================
# Chart 4: Relationship between Delay and Low Score (Basic Scatterplot)
# ================================================================
plt.figure(figsize=(10, 7))
 
# separate States between high and low revenue for transparency (avobe/below 0.5% of total revenue)
total_br_revenue = states["total_state_revenue"].sum()
states["revenue_weight_pct"] = (states["total_state_revenue"] / total_br_revenue) * 100
high_rev = states[states["revenue_weight_pct"] >= 0.5]
low_rev = states[states["revenue_weight_pct"] < 0.5]
 
vmin = states["pct_revenue_at_risk"].min()
vmax = states["pct_revenue_at_risk"].max()
 
sc1 = plt.scatter(high_rev["pct_delay"], high_rev["avg_review_score"], 
                  c=high_rev["pct_revenue_at_risk"], cmap="OrRd", 
                  s=100, edgecolors="#444444", vmin=vmin, vmax=vmax)
 
sc2 = plt.scatter(low_rev["pct_delay"], low_rev["avg_review_score"], 
                  c=low_rev["pct_revenue_at_risk"], cmap="OrRd", 
                  s=100, alpha=0.25, edgecolors="#444444", vmin=vmin, vmax=vmax)
 
# Aggiungiamo la barra dei colori laterale legandola a sc1
cbar = plt.colorbar(sc1, pad=0.02)
cbar.set_label("% Revenue at risk", fontsize=13)
 
# Add the dashed lines for the Brazil benchmarks
plt.axvline(bench["pct_delay"], color="#b0b0b0", linestyle="--", linewidth=1.5, label=f"Brazil avg delay: {bench['pct_delay']:.0f}%")
plt.axhline(bench["avg_review_score"], color="gray", linestyle="--", linewidth=1.5, label=f"Brazil avg score: {bench['avg_review_score']:.2f}")
 
custom_offsets = {
    "AC": (-0.5, 0.0),  
}
for i in range(len(states)):
    state_name = states["customer_state"][i]
    x_pos = states["pct_delay"][i]
    y_pos = states["avg_review_score"][i]
    if state_name in custom_offsets:
        offset_x = custom_offsets[state_name][0]
        offset_y = custom_offsets[state_name][1]
        plt.text(x_pos + offset_x, y_pos + offset_y +0.011, state_name, fontsize=9)
    else:
        plt.text(x_pos - 0.2, y_pos + 0.011, state_name, fontsize=9)
 
plt.xticks(fontsize=13)
plt.yticks(fontsize=13)

plt.title("Percentage of delays vs Average review score\n(transparecy for states with revenue < 0.5% of Brazil's total)", fontweight="bold",fontsize=16,pad=10)
plt.xlabel("% Delayed orders", fontsize=14, labelpad=10)
plt.ylabel("Average review score (1-5)", fontsize=14, labelpad=10)
plt.legend(loc="upper right", fontsize=10)
 
plt.tight_layout()
plt.savefig(f"{OUT}/04_scatter.png", bbox_inches="tight")
plt.close()