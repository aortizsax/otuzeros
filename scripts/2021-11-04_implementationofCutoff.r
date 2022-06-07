#zero filtering practice 
#NICK data
OTUtable <- read.csv('../data/nickdata/table.from_biom.tsv',
                     sep = '\t',header = T,row.names = 1,
                     check.names = F)
head(OTUtable)

tftab<-OTUtable==0
tftab[tftab] <- 1

#from python code
CUTOFF <- 117.15
sum(rowSums(tftab)>CUTOFF)
sum(rowSums(tftab)<CUTOFF)

# head(OTUtable)
dim(OTUtable)
zerofiltOTU <- OTUtable[rowSums(tftab)<CUTOFF,]
# head(zerofiltOTU)
dim(zerofiltOTU)



#alex data
OTUtableA <- read.csv('../data/alexdata/table.from_biom.tsv',
                      sep = '\t',header = T,row.names = 1,
                      check.names = F)
head(OTUtableA)

tftabA<-OTUtableA==0
# tftabA[,1]
tftabA[tftabA] <- 1
# tftabA[tftabA==F] <- 0

#from python code
CUTOFF <- 246.65
sum(rowSums(tftabA)>CUTOFF)
sum(rowSums(tftabA)<CUTOFF)

head(OTUtableA)
dim(OTUtableA)
zerofiltOTUa <- OTUtableA[rowSums(tftabA)<CUTOFF,]
head(zerofiltOTUa)
dim(zerofiltOTUa)

