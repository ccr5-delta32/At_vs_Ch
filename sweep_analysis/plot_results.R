###########################################################################################
###                                     Arabidopsis                                     ###
###########################################################################################

# Genome wide significance cutoff
for (x in 1:5) {
  if (x == 1) {
    GWcutoff <- read.table(paste("./OmegaPlus_Report.At_grid600k-Chr", x, sep=''), skip=2, header=FALSE)
  } else {
    GWcutoff <- rbind(GWcutoff, read.table(paste("./OmegaPlus_Report.At_grid600k-Chr", x, sep=''), skip=2, header=FALSE))
  }
}

pcutoff = 0.01
sig99 <- quantile(GWcutoff[,2], probs=c(0,1,(1-pcutoff)))[3]
pcutoff = 0.05
sig95 <- quantile(GWcutoff[,2], probs=c(0,1,(1-pcutoff)))[3]

# Plot all chromosomes
close.screen(all.screens=TRUE)
split.screen(c(5,1))

for (x in 1:5) {
  cdata <- read.table(paste("./OmegaPlus_Report.At_grid600k-Chr", x, sep=''), skip=2, header=FALSE)
  screen(x) 
  par(mar=c(2,2,0,2))
  plot(cdata[,1], cdata[,2], type='l')
  abline(h=quantile(cdata[,2], probs=c(0,1,(1-pcutoff)))[3], lty=2, col="red", lwd=1.1)
  abline(h=quantile(cdata[,2], probs=c(0,1,0.95))[3], lty=1, col="red", lwd=1.3)
}

# Plot specific loci
genes <- read.table('../At_gene_positions', header=TRUE, stringsAsFactors=FALSE)
do <-2 
updown <- 15000
cdata <- read.table(paste("./OmegaPlus_Report.At_grid600k-Chr", genes$chromosome[do], sep=''), skip=2, header=FALSE)

gene <- cdata[which(cdata[,1] >= (genes$prime5[do]-updown) & cdata[,1] <= (genes$prime3[do]+updown)),]
par(lwd=1.25, xpd=FALSE)
plot(gene$V1, gene$V2, type='l', ylim=c(-1, 1.05*(max(sig95, gene[,2]))), las=1, main=paste('Chromosome ', genes$chromosome[do]), ylab='OmegaPlus', xlab='Position (bp)')
abline(h=c(0,sig95), lty=1, col=c("black", "red"), lwd=1.2)
abline(v=c(genes$prime5[do], genes$prime3[do], ifelse(genes$prime5[do]<genes$prime3[do], genes$prime5[do]-3000, genes$prime5[do]+3000)), lty=c(3,3,1), col="blue")
arrows(genes$prime5[do],-0.5,genes$prime3[do],-0.5, length=0.15, lwd=5, col="grey52")
text(min(genes$prime5[do], genes$prime3[do]) + ((max(genes$prime5[do], genes$prime3[do]) - min(genes$prime5[do], genes$prime3[do])) / 2), -1.35, labels=substitute(paste(italic(N)), list(N=genes$locus[do])))
legend(xpd=TRUE, x=min(genes$prime5[do], genes$prime3[do]) + ((max(genes$prime5[do], genes$prime3[do])-min(genes$prime5[do], genes$prime3[do]))/2), y=1.07*(max(sig95, gene[,2])), horiz=TRUE, bty='n', xjust=0.5, yjust=0, lty=c(3,1,1), col=c("blue", "blue", "red"), legend=c("ORF", "ATG-3k", "GW 5% threshold"))

###
c3  <- read.table("OmegaPlus_Report.At_grid600k-Chr3", skip=2, header=FALSE)
max(c3)
c3[which(c3$V2==max(c3)),]
c3[65300:65400,]
close.screen(all.screens=TRUE)
split.screen(c(2,1))
screen(1)
  par(mar=c(0.2,2,2,2))
  subs <- c3
  subs[which(subs[,2] < 2500), 2] = NA 
  plot(subs[,1], subs[,2], ylim=c(2500,1.5e+8), axes=FALSE, type='o', cex=0.5)
  axis(side=2, at=seq(1e+7,1.5e+8, by=0.2e+8))
  box()
screen(2)
  par(mar=c(2,2,0.2,2))
  subs <- c3
  subs[which(subs[,2] > 2500), 2] = NA
  plot(subs[,1], subs[,2], type='l')
  abline(h=quantile(cdata[,2], probs=c(0,1,(1-pcutoff)))[3], lty=2, col="red", lwd=1.1)
  abline(h=quantile(cdata[,2], probs=c(0,1,0.95))[3], lty=1, col="red", lwd=1.3)

sub1 <- c3
sub1[which(sub1[,2] > 50000), 2] = 0
max(sub1[,2])


###########################################################################################
###                                      Cardamine                                      ###
###########################################################################################


