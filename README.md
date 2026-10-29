# Assingment-7_Llerena

Behind every sports dataset lies a story waiting to be told. Rather than treating NBA.csv as a dry spreadsheet of box scores, this script takes a data-driven journey through modern basketball history.

We begin by identifying the league's ultimate iron man—the player with the most regular-season appearances on record. By building a dedicated profile, we track how their three-point shooting evolved across decades, fit an ordinary least-squares regression line to model their career trajectory, and use calculus-based numerical integration to see if continuous mathematics agrees with real-world shooting averages.

From there, the analysis expands to the entire league. We examine whether core scoring metrics follow well-behaved distributions through higher-order statistical moments, reconstruct missing seasonal data using interpolation, and apply hypothesis testing to rigorously evaluate scoring volume and shooting inefficiency.

Libraries used:
  Pandas: Utilized for data ingestion, cleaning, and heterogeneous tabular manipulation. Specific tasks include filtering conditional subsets (Stage == 'Regular_Season'), identifying modal player frequencies, and parsing season timeline strings into discrete numerical temporal features.

NumPy: Serves as the numerical foundation, transforming Pandas Series into homogeneous 1D floating-point arrays. This ensures memory-contiguous execution, resolves Pandas index-alignment overhead, and streamlines vector math for linear evaluation and array difference operations (np.setdiff1d).

SciPy: Leveraged for advanced numerical and inferential computing across three dedicated sub-packages:

scipy.stats: Executed ordinary least-squares regression (linregress), high-order distribution profiling (skew, kurtosis), one-sample hypothesis testing (ttest_1samp), and paired-sample relational testing (ttest_rel).

scipy.integrate: Performed numerical integration (quad) to compute the continuous average accuracy across career intervals via the Mean Value Theorem for integrals.

scipy.interpolate: Implemented piecewise linear interpolation (interp1d) to estimate shooting percentages for absent/unrecorded seasons within the career timeline.

Key Steps:
Dedicated Player Profile (player_df): Instead of filtering the master dataset on every calculation, the modal player (.mode()[0]) was extracted into an isolated DataFrame (player_df). This keeps downstream calculations lightweight, prevents inadvertent data mutation, and provides a clean sandbox for feature engineering.

Linear Fit was regressed 3-point accuracy (dependent variable y) against career years (independent variable x) to generate a line of best fit: y_hat(x) = slope * x + intercept. Then, integrated this fit line across the player's career span using scipy.integrate.quad, setting the lower bound to the earliest season (a = 2000) and the upper bound to the final season (b = 2019). Dividing the resulting area by the span (b - a = 19 years) yielded a continuous average (36.88%) that closely matches the player's true empirical average (36.99%), confirming the fit's validity with only a 0.11% residual delta.

An interpolator was defined to estimate realistic shooting percentages for any seasons missing (2002, 2015) from the active career window. Results were stored in preds (38.46, 33.78)

League Distribution Moments and Hypothesis Testing

Mean: The average for FGA (679.86) is more than double the average for FGM (311.48). The direct ratio of these means (311.48 / 679.86) indicates an overall conversion proportion of approximately 0.458 (45.8%).

Variance: FGA displays a variance of 118,066.75, which is more than 4.5 times greater than the variance of FGM (25,944.08). Converting these to standard deviations (approx. 343.61 for FGA vs. 161.07 for FGM) shows that attempt volume fluctuates over twice as widely as scoring volume across the dataset.

Skewness: Both distributions show nearly identical positive skewness values (0.77 for FGM and 0.73 for FGA). Being between 0.5 and 1.0, both datasets are moderately skewed to the right, meaning the bulk of the observations cluster below the mean while a smaller number of large values extend the right tail.

Kurtosis: Excess kurtosis values are 0.15 for FGM and 0.12 for FGA. Because both values are close to 0, both distributions are essentially mesokurtic, meaning their peak sharpness and tail thicknesses closely resemble a standard normal distribution without extreme outliers.

Hypothesis Tests Comparison:

Individual Tests: Both one-sample tests yielded large positive statistics of similar magnitude: t = 131.98 for FGM and t = 135.04 for FGA. With degrees of freedom in the thousands, these values sit over 130 standard errors away from the null value (mu = 0). The computed p = 0.0 is the result of floating-point underflow (p < 0.001), indicating conclusive statistical significance.

Relational (Paired) Test: The paired test produced t = -133.01 with p = 0.0. While the magnitude of t is nearly identical to the individual tests (~133), the sign inverts to negative. Evaluating the pairwise difference (FGM - FGA) subtracts a larger quantity from a smaller one across every observation, producing a consistent negative difference vector whose mean is significantly less than zero.
