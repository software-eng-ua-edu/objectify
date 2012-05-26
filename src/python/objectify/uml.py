def uml(self):
  base = ("digraph G {\nfontname = \"Bitstream Vera Sans\"\nfontsize = 8\n"
           "node [\nfontname = \"Bitstream Vera Sans\"\nfontsize = 8\nshape = \"record\"\n]\n"
           "edge [\nfontname = \"Bitstream Vera Sans\"\nfontsize = 8\n]\n")
   for i in self.structs:
     self.className = i
     uml = "%s [\n label = \"{%s|" % (self.className, self.className)
     for f in self.structs[i]:
       uml += "+ %s : %s \l" % (f[1], f[0])
     uml += "}\"\n]"
     print '%s%s\n' % (base, uml)
     open(self.className + ".dot","w").write(base + uml + "\n}")
