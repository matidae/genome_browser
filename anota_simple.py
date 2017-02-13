import sys
from subprocess import Popen, PIPE
from operator import attrgetter

orfs_data = {i.split()[0]: i.split()[1:] for i in open(sys.argv[2])}
nlines = int(Popen(["wc", "-l", sys.argv[1]], stdout=PIPE).communicate()[0].split(" ")[0])
mapeos = []
n = 0
open("out.anota", "w").close()


class Mapeo:
    def __init__(self, qname, sname, idn, cov, evalue, desc, slen):
        self.qname = qname
        self.sname = sname
        self.idn = idn
        self.cov = cov
        self.evalue = evalue
        self.desc = desc
        self.slen = slen

def entry(*args):
    m = args[0]
    line = ""
    contig = "_".join(m.qname.split("_")[:2])
    start = orfs_data[m.qname][0]
    end = orfs_data[m.qname][1]
    strand = orfs_data[m.qname][2]
    org = m.desc.split("[")[1][:-1]
    prod = m.desc.split("[")[0][:-1]
    desc = "id=" + m.qname + ";len=" + str(int(end)-int(start)) + ";name=" + \
           m.sname + ";idn=" + str(m.idn)[:4] + ";cov=" + str(m.cov)[:4]
    desc += ";evalue=" + str(m.evalue) + ";peplen=" + m.slen + ";prod=" + prod + ";org=" + org
    line = "\t".join([contig, "getorf", "orf", start, end, ".", strand, ".", desc]) 
    if len(args) ==1:
        return line + "\n"
    else:       
        n = args[1]
        org = n.desc.split("[")[1][:-1]
        prod = n.desc.split("[")[0][:-1]
        desc = ";name2=" + n.sname + ";idn2=" + str(n.idn)[:4] + ";cov2=" + str(n.cov)[:4]
        desc += ";evalue2=" + str(n.evalue) + ";peplen2=" + n.slen + ";prod2=" + prod + ";org2=" + org
        line += desc
        return line + "\n"


def anota(mapeos):
        with open("out.anota", "a") as out_hypo:
            if len(mapeos) == 1:
                out_hypo.write(entry(mapeos[0]))
            else:
                out_hypo.write(entry(mapeos[0], mapeos[1]))


with open(sys.argv[1]) as blast:
    qname_pre = ""
    for line in blast:
        n += 1
        sname = line.split("\t")[1]
        idn = float(line.split("\t")[2])
        cov = float(line.split("\t")[3]) / float(line.split("\t")[13])
        desc = line.split("\t")[12]
        evalue = line.split("\t")[10]
        slen = line.split("\t")[14].strip()
        if qname_pre != "" and n < nlines:
            qname = line.split()[0]
            if qname_pre != qname:
                anota(mapeos)
                mapeos = []
                qname_pre = qname
                mapeos.append(Mapeo(qname, sname, idn, cov, evalue, desc, slen))
            else:
                mapeos.append(Mapeo(qname, sname, idn, cov, evalue, desc, slen))
        elif n == nlines:
            anota(mapeos)
                
        else:
            qname_pre = line.split()[0]
            mapeos.append(Mapeo(qname_pre, sname, idn, cov, evalue, desc, slen))
