###############################################
##            FOMC Word Watching            ##
###############################################

# INFO: Due to sleep function of 3 to 7 seconds between each parsing, it's can take around 20 minutes to run it all.

#R packages
library(rstudioapi)
library(tidyverse)
library(reticulate)

#install.packages("rstudioapi")
setwd(dirname(getActiveDocumentContext()$path))

###############################################
##            Run Python scripts             ##
###############################################

reticulate::source_python("getFedFundsRate.py")
reticulate::source_python("iterateMinutes.py")

#Get Minutes


###############################################
##            Run R scripts                  ##
###############################################

# Get last Minutes date

df <- read.table(
  "data\\fomcMinutesSummary.csv",
  sep=",", header=TRUE
)

# Covert dates
df <- df %>%
  mutate(date = as.Date(gsub("\\D", "", date), format= "%Y%m%d"))

date_last_minutes = as.Date(max(df$date))

# Run markdown report
res <- rmarkdown::render("index.rmd", output_file = "index.html")
# save copy of report
file.copy(res,  sprintf("OldReports\\index_%s.html", date_last_minutes))