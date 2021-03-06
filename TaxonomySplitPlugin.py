import sys
import os
class TaxonomySplitPlugin:
   def input(self, filename):
      filestuff = open(filename, 'r')
      firstline = filestuff.readline().strip() # Read first line
      self.taxa = firstline.split(',')
      self.taxa.remove(self.taxa[0])  # Remove placeholder
      self.taxmap = dict()
      for i in range(len(self.taxa)):
         self.taxa[i] = self.taxa[i].replace('\"', '')
         
      self.levels = ["kingdom", "phylum", "class", "order", "family", "genus", "species"]
      self.classificationlevel = 0     
      self.taxanames = [[],[],[],[],[],[],[]]
      for taxon in self.taxa:
         taxonomy = taxon.split("; __")
         if (self.classificationlevel != 0 and len(taxonomy) != self.classificationlevel):
            print("WARNING MULTIPLE CLASSIFICATION LEVELS PRESENT")
            print(taxonomy)
         self.classificationlevel = max(self.classificationlevel, len(taxonomy))
         #for j in range(0, len(taxonomy)):
         for j in range(len(taxonomy)-1, -1, -1):
            # TMC check if unclassifiable at this level, if so use the one higher
            if (taxonomy[j] == str(self.levels[j][0])): # Not classifiable
               k = j-1
               while (taxonomy[k] == str(self.levels[k][0])):
                  k -= 1
               taxonomy[j] = taxonomy[k]+"("+self.levels[k]+")"
            elif (j == 6):
               taxonomy[j] = taxonomy[j-1]+" "+taxonomy[j]
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
         #print("******************************* NEW SAMPLE **************************************")
         elements = line.split(',')
         self.samplenames.append(elements[0])
         elements.remove(elements[0]) # remove sample name
         counts = [dict(), dict(), dict(), dict(), dict(), dict(), dict()]  # 7 at most
         for i in range(0, len(elements)):
            #print("CLASSIFYING TAXON: "+self.taxa[i])
            taxonomy = self.taxa[i].split("; __")  # characters on which to split
            for j in range(len(taxonomy)-1, -1, -1):
            #for j in range(0, len(taxonomy)):
               if (taxonomy[j] == str(self.levels[j][0])): # Not classifiable
                  k = j-1
                  while (taxonomy[k] == str(self.levels[k][0])):
                     k -= 1
                  taxonomy[j] = taxonomy[k]+"("+self.levels[k]+")"
               elif (j == 6):
                  taxonomy[j] = taxonomy[j-1]+" "+taxonomy[j]
               if (taxonomy[j] in counts[j]):
                  counts[j][taxonomy[j]] += float(elements[i])
                  #if (float(elements[i]) != 0):
                  #  print("ADDING "+elements[i]+" TO "+taxonomy[j]+": "+str(counts[j][taxonomy[j]]))
               else:
                  #if (float(elements[i]) != 0):
                  #  print("CREATING NEW "+taxonomy[j])
                  counts[j][taxonomy[j]] = float(elements[i])
            self.taxmap[self.taxa[i]] = taxonomy
         self.samplecounts.append(counts)
         #print("******************************* DONE SAMPLE **************************************")

   def output(self,filename):
      directories = False
      
      taxfile = open(filename+".tax.csv", 'w')
      taxfile.write('\"\"')
      for i in range(self.classificationlevel):
         taxfile.write(',')
         taxfile.write(self.levels[i])
      taxfile.write('\n')

      for taxon in self.taxa:
         taxfile.write(taxon+",")
         for i in range(self.classificationlevel):
            taxfile.write(self.taxmap[taxon][i])
            if (i != self.classificationlevel-1):
               taxfile.write(',')
            else:
               taxfile.write('\n')

      #print(filename[0:filename.rfind('/')]+"/kingdom")
      if os.path.exists(filename[0:filename.rfind('/')]+"/kingdom"):
         directories = True
      for i in range(self.classificationlevel):
         if (directories):
            prefix = filename[0:filename.rfind('/')]+"/"+self.levels[i]+"/"+filename[filename.rfind('/')+1:len(filename)]
         else:
            prefix = filename+"."+self.levels[i]+".csv"
         
         outstuff = open(prefix, 'w')
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
