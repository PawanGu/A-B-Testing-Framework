# A/B Test Report — Pricing + Promotion on Conversion

**Dataset**: synthetic_ab_data.csv (N=50000)

## Summary
- Control (A) Conversion: 0.0715  (95% CI: [0.0684, 0.0748])
- Treatment (B) Conversion: 0.0887 (95% CI: [0.0852, 0.0922])
- Absolute Lift: 0.0172
- Relative Lift: 24.01%
- Two-sided z-test: z = 7.070, p-value = 1.555e-12

## Interpretation
Significant difference detected between groups.

## Sample Size Guidance
- Baseline conversion (control): 0.0715
- To detect an **absolute** lift of 1 percentage point (MDE = 0.01) with 80% power at α=0.05, you need:
  - **~11088 users per group**.

## Notes
- The simulation applies a slight negative price effect and a positive promo effect; net impact is observable in treatment vs control.
- Additional columns (`country`, `device`) can be used for stratified analysis or CUPED-style variance reduction.