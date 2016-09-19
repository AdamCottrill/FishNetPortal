#=============================================================
# c:/1work/Python/djcode/fn_portal/utils/calc_smallfish_flentlen.r
# Created: 16 Sep 2016 09:51:18
#
# DESCRIPTION:
#
#
# A little helper script to calculate flen-Tlen coefficients for
# species found in the small fish database.  Allows us to estimate
# flen when we didn't bother to collect it.
#
# A. Cottrill
#=============================================================

# LIBRARIES:
library(RODBC)
library(reshape2)
library(plyr)


#=============================================================

DBASE <- 'C:/1work/Python/djcode/fn_portal/utils/mdbs/Smallfish.mdb'

DBConnection <- odbcConnectAccess(DBASE, uid = "")
data <- sqlFetch(DBConnection, 'get_both_flen_tlen', colnames=FALSE,
               rownames=FALSE, stringsAsFactors=FALSE)
names(data) <- toupper(names(data))
head(data)
str(data)
nrow(data)
odbcClose(DBConnection)


#subset our data to include only those species with some minumumn
#number of observations:
minNobs <- 5
nobsSpc <- count(data, 'SPC')
nobsSpc <- nobsSpc[nobsSpc[,2]>minNobs,]
data <-  data[data$SPC %in% nobsSpc$SPC,]


flen_tlen<- function(x){
  # a helper function used by plyr to fit a linear regession of the data
  # data in x (x is a dataframe that must contain the variables flen
  # and tlen.

  fit <- try( lm(TLEN ~ FLEN, data=x), silent=TRUE)
  if(inherits(fit, 'try-error')){
    return(data.frame(slope=NA, intercept=NA, N=NA))
  } else {
    coefs = coef(fit)
    return(data.frame(slope=coefs[2], intercept=coefs[1], N=nrow(x)))
  }

  }


flen_tlen_coefs <-  ddply(data, 'SPC', flen_tlen)

#convert the species codes back to text and add the leading 0's
flen_tlen_coefs$SPC <- sprintf('%03d', flen_tlen_coefs$SPC)

DBConnection <- odbcConnectAccess(DBASE, uid = "", pwd = "")
sqlSave(DBConnection, flen_tlen_coefs, safer = FALSE, fast = TRUE,
        rownames=FALSE)
odbcClose(DBConnection)
