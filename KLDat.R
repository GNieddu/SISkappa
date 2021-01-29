rm(list=ls())

library(tidyr)
library(dplyr)
library(ggplot2)

require("reticulate")
source_python("pickle_reader.py")

mod.indx <- 1
Mod.list <- c("SI","SIS","SIR","SEIR")
Mod.name.list <- c("1D-SIS","SIS","SIR","SEIR")
for (mod.name in Mod.list) {
  dat.path <- paste0("data/in/",mod.name,"KLdat.pkl")
  Mod.dat.util <- read_pickle_file(dat.path)

  kval <- Mod.dat.util[['kval Vector']]
  Nval <- Mod.dat.util[['Nval Vector']]
  KLDiv <- Mod.dat.util[['KLDiv Matrix']]

  i.indx <- 1
  for (i in kval) {
    j.indx <- 1
    for (j in Nval) {
      if (j.indx==1 & i.indx==1 & mod.indx==1) {
        KL.df <- data.frame("KLDiv" = KLDiv[i.indx,j.indx],
        "kval" = i,
        "Nval" = j,
        "Model" = Mod.name.list[mod.indx])
      } else {
        KL.util <- data.frame("KLDiv" = KLDiv[i.indx,j.indx],
        "kval" = i,
        "Nval" = j,
        "Model" = Mod.name.list[mod.indx])
        KL.df <- rbind(KL.df,KL.util)
      }
      j.indx <- j.indx + 1
    }
    i.indx <- i.indx + 1
  }
  mod.indx <- mod.indx + 1


}

KL.df <- KL.df %>% mutate(kN = kval*Nval)


KL.plt <- ggplot() + geom_point(data=KL.df,
                                aes(x=log10(kN),
                                    y=KLDiv,
                                    color=Model,
                                    shape=Model)) +
                      xlab("External infection rate [log10(infections/day)]") +
                      ylab("KL-Divergence") +
                      theme(text = element_text(size = 20)) +
                      theme(legend.text = element_text(size = 20)) +
                      guides(size=FALSE)



pdf("KLDiv_Combined.pdf",width=8,height=5)
KL.plt
dev.off()
