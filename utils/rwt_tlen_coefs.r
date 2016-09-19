#=============================================================
# c:/1work/Python/djcode/fn_portal/utils/rwt_tlen_coefs.r
# Created: 16 Sep 2016 14:13:34
#
# DESCRIPTION:
#
# A. Cottrill
#=============================================================

# LIBRARIES:
library(RODBC)
library(reshape2)
library(ggplot2)
library(plyr)

#=============================================================

DBASE <- 'C:/1work/ScrapBook/Biomass_per_net.mdb'
DBConnection <- odbcConnectAccess(DBASE, uid = "", pwd = "")
DF <- sqlFetch(DBConnection, 'get_tlen_rwt_data', colnames=FALSE,
               rownames=FALSE, stringsAsFactors=FALSE)
names(DF) <- toupper(names(DF))
head(DF)
str(DF)
nrow(DF)
odbcClose(DBConnection)


wt_length<- function(x){
  # a helper function used by plyr to fit a von-bert curve to the
  # data in x (x is a dataframe that must contain the variables AGE
  # and FLEN.
  x <- subset(x, !is.na(x$TLEN) & !is.na(x$RWT))

  x$logrwt = log(x$RWT)
  x$logtlen = log(x$TLEN)

  fit <- try( lm(logrwt ~ logtlen, data=x), silent=TRUE)
  if(inherits(fit, 'try-error')){
    return(data.frame(alpha=NA, beta=NA))
  } else {
    coefs = coef(fit)
    return(data.frame(alpha=coefs[2], beta=coefs[1]))
  }

  }


wtlength_coefs <-  ddply(DF, 'SPC', wt_length)

(nrow(wtlength_coefs))

wtlength_coefs <- subset(wtlength_coefs, !is.na(wtlength_coefs$alpha)
                         & wtlength_coefs$alpha>0)
wtlength_coefs$SPC <- sprintf('%03d', wtlength_coefs$SPC)


DBConnection <- odbcConnectAccess(DBASE, uid = "", pwd = "")
sqlSave(DBConnection, wtlength_coefs, safer = FALSE, fast = TRUE,
        rownames=FALSE)
odbcClose(DBConnection)
