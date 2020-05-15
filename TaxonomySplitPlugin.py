import sys

class TaxonomySplitPlugin:
   def input(self, filename):
      filestuff = open(filename, 'r')
      firstline = filestuff.readline().strip() # Read first line
      self.taxa = firstline.split(',')
      self.taxa.remove(self.taxa[0])  # Remove placeholder

      for i in range(len(self.taxa)):
         self.taxa[i] = self.taxa[i].replace('\"', '')
         

      self.levels = ["kingdom", "phylum", "class", "order", "family", "genus", "species"]
      self.classificationlevel = 0     
      self.taxanames = [[],[],[],[],[],[],[]]
      for taxon in self.taxa:
         taxonomy = taxon.split("..__")
         if (self.classificationlevel != 0 and len(taxonomy) != self.classificationlevel):
            print("WARNING MULTIPLE CLASSIFICATION LEVELS PRESENT")
         self.classificationlevel = max(self.classificationlevel, len(taxonomy))
         #for j in range(0, len(taxonomy)):
         for j in range(len(taxonomy)-1, -1, -1):
            # TMC check if unclassifiable at this level, if so use the one higher
            if (taxonomy[j] == str(self.levels[j][0])): # Not classifiable
               k = j-1
               while (taxonomy[k] == str(self.levels[k][0])):
                  k -= 1
               taxonomy[j] = taxonomy[k]+"("+self.levels[k]+")"
            if (taxonomy[j] not in self.taxanames[j]):
               self.taxanames[j].append(taxonomy[j])
         
      self.lines = []
      for line in filestuff:
         self.lines.append(line)

      self.sums = dict()
      for taxon in self.taxa:
         self.sums[taxon] = 0


   def run(self):
      self.samplecounts = []
      self.samplenames = []
      for line in self.lines:
         elements = line.split(',')
         self.samplenames.append(elements[0])
         elements.remove(elements[0]) # remove sample name
         counts = [dict(), dict(), dict(), dict(), dict(), dict(), dict()]  # 7 at most
         for i in range(0, len(elements)):
            taxonomy = self.taxa[i].split("..__")  # characters on which to split
            for j in range(len(taxonomy)-1, -1, -1):
            #for j in range(0, len(taxonomy)):
               if (taxonomy[j] == str(self.levels[j][0])): # Not classifiable
                  k = j-1
                  while (taxonomy[k] == str(self.levels[k][0])):
                     k -= 1
                  taxonomy[j] = taxonomy[k]+"("+self.levels[k]+")"
               if (taxonomy[j] in counts[j]):
                  counts[j][taxonomy[j]] += float(elements[i])
               else:
                  counts[j][taxonomy[j]] = float(elements[i])
         self.samplecounts.append(counts)

   def output(self,filename):
      for i in range(self.classificationlevel):
         outstuff = open(filename+"."+self.levels[i]+".csv", 'w')
         outstuff.write('\"\",')
         names = []
         for taxon in self.taxanames[i]:
            names.append(taxon)
         for j in range(len(names)):
            outstuff.write('\"'+names[j]+'\"')
            if (j != len(names)-1):
               outstuff.write(',')
            else:
               outstuff.write('\n')
         for k in range(len(self.samplenames)):
            outstuff.write(self.samplenames[k]+',')
            for j in range(len(names)):
               outstuff.write(str(self.samplecounts[k][i][names[j]]))
               if (j != len(names)-1):
                  outstuff.write(',')
               else:
                  outstuff.write('\n')
