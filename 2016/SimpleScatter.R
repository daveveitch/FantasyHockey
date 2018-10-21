# IMPORT LIBRARIES
library(dplyr)
library(chron)
library(plotly)
library(ggplot2)

#Import Season Stats
setwd("WORKING DIRECTORY")
fhstatscsv <- read.csv("20180102.csv", header=TRUE)

#Use Player Code column as Row Name
row.names(fhstatscsv) <- fhstatscsv$Player.Code

#gives format of ATOI in numeric form with minutes as units
correct_ATOI <- sub(pattern=":", replacement=".", x= fhstatscsv$ATOI)
correct_ATOI <- as.numeric(correct_ATOI)
correct_ATOI <- correct_ATOI + (correct_ATOI - round(correct_ATOI)) / 0.6
fhstatscsv$ATOI <- correct_ATOI

#Filters Players According to a Number of Metrics
relevant_player_df <- filter(fhstatscsv, ATOI > 10, GP > 20, PTS/GP > .5, (PP+PP.1)/GP > 0.1) 

# Creates Plot_Ly plot
p <- plot_ly(data = relevant_player_df, x= ~PTS/GP, y = ~(PP+PP.1)/GP, color = ~(HIT)/GP, text = ~Player, type = 'scatter')
p

