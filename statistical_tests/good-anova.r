df <- read.csv('data-transform.csv')

anova <- aov(ART ~ young*difficult, data = df)
summary(anova)
