#uploading and previewing the csv

> df <- read.csv(file.choose())

> head(df)

  X county_fips fips state         county pcp_rate prev_hos_stays uninsured_rate blk_child_pov_rate whi_child_pov_rate od_rate od_deaths
1 2           1 1001    AL Autauga County    44.00           4365           8.19              26.10               8.27   10.86         6
2 3           3 1003    AL Baldwin County    62.68           2888          10.21              53.68               6.87   31.61        75
3 4           5 1005    AL Barbour County    40.06           3560          12.12              49.30               3.85   16.16         4
4 5           7 1007    AL    Bibb County    66.73           5029          10.84              69.43              23.95   27.02         6
5 6           9 1009    AL  Blount County    20.32           2099          12.52              18.48              12.32   23.81        14
6 7          11 1011    AL Bullock County    19.38           4377          11.41              47.06               6.72      NA        NA
  od_pop med_income blk_med_income whi_med_income rural_pct
1  58333      68857          53861          76976     40.68
2 238339      74248          39015          81134     37.59
3  24753      45298          28125          65577     65.92
4  22206      56025          25833          60817    100.00
5  58811      64962             NA          62636     90.49
6     NA      36204          30149          65063    100.00

nrow(df)
[1] 3152

#question 1a: paired t-test on black and white child poverty rates

> t.test(df$blk_child_pov_rate, df$whi_child_pov_rate, paired = TRUE)

        Paired t-test

data:  df$blk_child_pov_rate and df$whi_child_pov_rate
t = 46.885, df = 1629, p-value < 2.2e-16
alternative hypothesis: true mean difference is not equal to 0
95 percent confidence interval:
 20.75085 22.56286
sample estimates:
mean difference 
        21.65685 
        
#question 1b: paired t-test on black and white median income

> t.test(df$blk_med_income, df$whi_med_income, paired = TRUE)

        Paired t-test

data:  df$blk_med_income and df$whi_med_income
t = -39.531, df = 1766, p-value < 2.2e-16
alternative hypothesis: true mean difference is not equal to 0
95 percent confidence interval:
 -22959.00 -20788.51
sample estimates:
  mean difference 
        -21873.76 

#splitting rural percentage into a more rural or more urban category (area type)

> df$area_type <- ifelse(df$rural_pct >= 50, "Rural", "Urban")

#question 2a: welch t-test on uninsured rate and area tyoe

> t.test(uninsured_rate ~ area_type, data = df)

        Welch Two Sample t-test

data:  uninsured_rate by area_type
t = 8.3699, df = 2429.5, p-value < 2.2e-16
alternative hypothesis: true difference in means between group Rural and group Urban is not equal to 0
95 percent confidence interval:
 1.083095 1.745886
sample estimates:
mean in group Rural mean in group Urban 
          10.983803            9.569312 

#question 2b: welch t-test on primary care physician rate and area type
          
> t.test(pcp_rate ~ area_type, data = df)

        Welch Two Sample t-test

data:  pcp_rate by area_type
t = -19.951, df = 2377, p-value < 2.2e-16
alternative hypothesis: true difference in means between group Rural and group Urban is not equal to 0
95 percent confidence interval:
 -28.59955 -23.48053
sample estimates:
mean in group Rural mean in group Urban 
           43.68287            69.72291 

#question 2c: welch t-test on previous hospital stays and area type
        
> t.test(prev_hos_stays ~ area_type, data = df)

        Welch Two Sample t-test

data:  prev_hos_stays by area_type
t = 5.7275, df = 2936.3, p-value = 1.123e-08
alternative hypothesis: true difference in means between group Rural and group Urban is not equal to 0
95 percent confidence interval:
 139.2789 284.2832
sample estimates:
mean in group Rural mean in group Urban 
           2904.976            2693.195 

#linear regression for question 2a           
           
> summary(lm(uninsured_rate ~ rural_pct + med_income, data = df))

Call:
  lm(formula = uninsured_rate ~ rural_pct + med_income, data = df)

Residuals:
    Min      1Q  Median      3Q     Max 
-8.1509 -3.3786 -0.8198  2.3113 25.0426 

Coefficients:
              Estimate Std. Error t value Pr(>|t|)    
(Intercept)  1.533e+01  4.439e-01  34.533  < 2e-16 ***
rural_pct    8.560e-03  2.568e-03   3.334 0.000866 ***
med_income  -8.241e-05  5.218e-06 -15.793  < 2e-16 ***
---
Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1

Residual standard error: 4.401 on 3140 degrees of freedom
  (9 observations deleted due to missingness)
Multiple R-squared:  0.1049,	Adjusted R-squared:  0.1043 
F-statistic:   184 on 2 and 3140 DF,  p-value: < 2.2e-16

#linear regression for question 2b

> summary(lm(pcp_rate ~ rural_pct + med_income, data = df))

Call:
  lm(formula = pcp_rate ~ rural_pct + med_income, data = df)

Residuals:
   Min     1Q Median     3Q    Max 
-84.71 -20.85  -5.78  13.06 521.78 

Coefficients:
              Estimate Std. Error t value Pr(>|t|)    
(Intercept)  5.528e+01  3.471e+00  15.923  < 2e-16 ***
rural_pct   -3.619e-01  2.029e-02 -17.836  < 2e-16 ***
med_income   3.163e-04  4.081e-05   7.752 1.24e-14 ***
---
Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1

Residual standard error: 33.64 on 2974 degrees of freedom
  (175 observations deleted due to missingness)
Multiple R-squared:  0.1667,	Adjusted R-squared:  0.1661 
F-statistic: 297.4 on 2 and 2974 DF,  p-value: < 2.2e-16

#linear regression for question 2c

> summary(lm(prev_hos_stays ~ rural_pct + med_income, data = df))

Call:
  lm(formula = prev_hos_stays ~ rural_pct + med_income, data = df)

Residuals:
    Min      1Q  Median      3Q     Max 
-2759.9  -662.0   -75.0   546.4  6981.0 

Coefficients:
              Estimate Std. Error t value Pr(>|t|)    
(Intercept)  4.297e+03  1.058e+02  40.604   <2e-16 ***
rural_pct   -1.507e+00  6.131e-01  -2.457    0.014 *  
med_income  -2.100e-02  1.247e-03 -16.846   <2e-16 ***
---
Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1

Residual standard error: 1030 on 3058 degrees of freedom
  (91 observations deleted due to missingness)
Multiple R-squared:  0.09217,	Adjusted R-squared:  0.09158 
F-statistic: 155.2 on 2 and 3058 DF,  p-value: < 2.2e-16

#splitting west virginia from the other states

> df$is_wv <- ifelse(df$state == "WV", "WV", "Other")

#question 3a: t-test on overdose rate in west virginia and states other than west virginia and dc

> t.test(od_rate ~ is_wv, data = df)

        Welch Two Sample t-test

data:  od_rate by is_wv
t = -8.2819, df = 44.476, p-value = 1.469e-10
alternative hypothesis: true difference in means between group Other and group WV is not equal to 0
95 percent confidence interval:
 -55.06756 -33.51727
sample estimates:
mean in group Other    mean in group WV 
           31.81536            76.10778 

#question 3b: wilcox test on overdose rate and west virginia           
           
> wilcox.test(od_rate ~ is_wv, data = df)

        Wilcoxon rank sum test with continuity correction

data:  od_rate by is_wv
W = 7934, p-value < 2.2e-16
alternative hypothesis: true location shift is not equal to 0