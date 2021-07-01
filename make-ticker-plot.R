library(tidyverse)
library(knitr)

# read data
x <- read_csv("wsb.csv", col_types = cols(
  ticker = col_character(),
  date = col_double(),
  title = col_character(),
  url = col_character()
))

# 10 most mentioned stock tickers
data <- x %>%
  select(ticker) %>%
  group_by(ticker) %>%
  summarize(count = n()) %>%
  arrange(desc(count)) %>%
  slice(1:10) %>%
  mutate(ticker = as.factor(ticker))

#get current date as a string
date <- toString(Sys.Date())

#get most mentioned stock as a string
most_mentioned <- data %>%
  slice(1)
ticker <- toString(most_mentioned$ticker)

# create plot
ticker_plot <- data %>%
  ggplot(mapping = aes(fct_reorder(ticker, count), count)) +
  geom_col(fill = "lightblue") +
  geom_text(aes(label = count), position = position_dodge(width = 0.9), vjust = -0.25) +
  theme_classic() +
  labs(title = "Frequently Mentioned Tickers on WallStreetBets",
       subtitle = paste(ticker, "was the most commonly mentioned stock ticker on", date),
       x = "Ticker",
       y = "Post Title Mentions",
       caption = "Source: r/WallStreetBets")

write_rds(ticker_plot, "ticker-plot.rds")