
setwd("/Users/MegGarr/Documents/SISkappa/")
rm(list=ls())

library(dplyr)
library(tidyr)
library(ggplot2)

SI.df <- read.csv("./data/out/SI/SIk_keq_1p172Em05_Neq_1p172E04",
                  header = FALSE)

ggplot(SI.df) + geom_point(aes(x=V1,y=V2))

ggplot(SI.df) + geom_histogram(aes(x=V2,y=..density..))

kappa <- SI.df[[1,3]]
N <- SI.df[[1,4]]
