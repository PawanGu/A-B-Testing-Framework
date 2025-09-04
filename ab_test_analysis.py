#!/usr/bin/env python3
import math
import pandas as pd
from scipy.stats import norm
import matplotlib.pyplot as plt

def proportion_ztest(count1, nobs1, count2, nobs2, alternative="two-sided"):
    p_pool = (count1 + count2) / (nobs1 + nobs2)
    se = math.sqrt(p_pool * (1 - p_pool) * (1/nobs1 + 1/nobs2))
    z = (count2/nobs2 - count1/nobs1) / se
    if alternative == "two-sided":
        pval = 2 * (1 - norm.cdf(abs(z)))
    elif alternative == "larger":
        pval = 1 - norm.cdf(z)
    else:
        pval = norm.cdf(z)
    return z, pval

def wilson_ci(k, n, alpha=0.05):
    if n == 0: 
        return (float("nan"), float("nan"))
    z = norm.ppf(1 - alpha/2)
    p_hat = k / n
    denom = 1 + z**2/n
    center = (p_hat + z**2/(2*n)) / denom
    half = (z * math.sqrt(p_hat*(1-p_hat)/n + z**2/(4*n**2))) / denom
    return center - half, center + half

def required_sample_size(p_baseline, mde_abs, alpha=0.05, power=0.8):
    z_alpha = norm.ppf(1 - alpha/2)
    z_beta = norm.ppf(power)
    p1 = p_baseline
    p2 = p_baseline + mde_abs
    pbar = (p1 + p2)/2
    qbar = 1 - pbar
    se1 = p1*(1-p1)
    se2 = p2*(1-p2)
    n_per_group = ((z_alpha*math.sqrt(2*pbar*qbar) + z_beta*math.sqrt(se1 + se2))**2) / (mde_abs**2)
    return math.ceil(n_per_group)

def main():
    df = pd.read_csv("data/synthetic_ab_data.csv")
    summary = df.groupby("group")["converted"].agg(["sum","count"])
    c_conv = int(summary.loc["A_control","sum"])
    c_n = int(summary.loc["A_control","count"])
    t_conv = int(summary.loc["B_treatment","sum"])
    t_n = int(summary.loc["B_treatment","count"])

    cr_control = c_conv / c_n
    cr_treat = t_conv / t_n
    abs_lift = cr_treat - cr_control
    rel_lift = abs_lift / cr_control if cr_control>0 else float("nan")

    z, pval = proportion_ztest(c_conv, c_n, t_conv, t_n, alternative="two-sided")
    ci_c = wilson_ci(c_conv, c_n)
    ci_t = wilson_ci(t_conv, t_n)

    # Plot
    plt.figure()
    plt.bar(["Control (A)","Treatment (B)"], [cr_control, cr_treat])
    plt.title("Conversion Rate by Group")
    plt.ylabel("Conversion Rate")
    plt.savefig("figures/group_conversion.png", bbox_inches="tight")
    plt.close()

    # Report
    report = f"""
# A/B Test Report — Pricing + Promotion on Conversion

**Dataset**: synthetic_ab_data.csv (N={len(df)})

## Summary
- Control (A) Conversion: {cr_control:.4f}  (95% CI: [{ci_c[0]:.4f}, {ci_c[1]:.4f}])
- Treatment (B) Conversion: {cr_treat:.4f} (95% CI: [{ci_t[0]:.4f}, {ci_t[1]:.4f}])
- Absolute Lift: {abs_lift:.4f}
- Relative Lift: {rel_lift*100:.2f}%
- Two-sided z-test: z = {z:.3f}, p-value = {pval:.4g}

## Interpretation
{"Significant difference detected between groups." if pval < 0.05 else "No statistically significant difference detected at α=0.05."}

## Sample Size Guidance
- Baseline conversion (control): {cr_control:.4f}
- To detect an **absolute** lift of 1 percentage point (MDE = 0.01) with 80% power at α=0.05, you need:
  - **~{required_sample_size(cr_control, 0.01, alpha=0.05, power=0.8)} users per group**.
"""
    with open("report.md","w") as f:
        f.write(report.strip())

    print("Analysis complete. See report.md and figures/group_conversion.png")

if __name__ == "__main__":
    main()
