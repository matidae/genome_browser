import sys
from subprocess import Popen, PIPE
from operator import attrgetter

orfs_data = {i.split()[0]: i.split()[1:] for i in open(sys.argv[2])}
nlines = int(Popen(["wc", "-l", sys.argv[1]], stdout=PIPE).communicate()[0].split(" ")[0])
mapeos = []
n = 0
open("out.masp", "w").close()
open("out.rhs", "w").close()
open("out.dgf", "w").close()
open("out.gp63", "w").close()
open("out.tasv", "w").close()
open("out.mucin", "w").close()
open("out.ts", "w").close()
open("out.solobrener", "w").close()
open("out.nobrener", "w").close()
open("out.hypocons", "w").close()
open("out.nohypo", "w").close()
open("out.hypo", "w").close()


class Mapeo:
    def __init__(self, qname, sname, idn, cov, evalue, desc):
        self.qname = qname
        self.sname = sname
        self.idn = idn
        self.cov = cov
        self.evalue = evalue
        self.desc = desc


def entry(*args):
    m = args[0]
    line = ""
    contig = "_".join(m.qname.split("_")[:2])
    start = orfs_data[m.qname][0]
    end = orfs_data[m.qname][1]
    strand = orfs_data[m.qname][2]
    org = m.desc.split("|")[1].strip().replace(" ", "_")
    prod = m.desc.split("|")[2].strip().replace(" ", "_")
    slen = m.desc.split("|")[4].strip().replace(" ", "_").replace("length=", "")
    desc = "id=" + m.qname + ";len=" + str(int(end)-int(start)) + ";name=" + \
            m.sname + ";idn=" + str(m.idn)[:4] + ";cov=" + str(m.cov)[:4]
    desc += ";evalue=" + str(m.evalue) + ";peplen=" + slen + ";prod=" + prod + ";org=" + org
    line = "\t".join([contig, "getorf", "orf", start, end, ".", strand, ".", desc])
    if len(args) ==1:
        return line + "\n"
    else:
        n = args[1]
        org = n.desc.split("|")[1].strip().replace(" ", "_")
        prod = n.desc.split("|")[2].strip().replace(" ", "_")
        slen = n.desc.split("|")[4].strip().replace(" ", "_").replace("length=","")
        desc = ";name2=" + n.sname + ";idn2=" + str(n.idn)[:4] + ";cov2=" + str(n.cov)[:4]
        desc += ";evalue2=" + str(n.evalue) + ";peplen2=" + slen + ";prod2=" + prod + ";org2=" + org
        line += desc
        return line + "\n"


def anota_familias(mapeos):
    for i in mapeos:
        if "MASP" in i.desc and float(i.evalue) < 1e-30:
            with open("out.masp", "a") as out_masp:
                out_masp.write(entry(i))
            return True
        elif "DGF" in i.desc and float(i.evalue) < 1e-30:
            with open("out.dgf", "a") as out_dgf:
                out_dgf.write(entry(i))
            return True
        elif "RHS" in i.desc and float(i.evalue) < 1e-30:
            with open("out.rhs", "a") as out_rhs:
                out_rhs.write(entry(i))
                return True
        elif "trans-sialidase" in i.desc and float(i.evalue) < 1e-30:
            with open("out.ts", "a") as out_ts:
                out_ts.write(entry(i))
                return True
        elif "GP63" in i.desc and float(i.evalue) < 1e-30:
            with open("out.gp63", "a") as out_gp63:
                out_gp63.write(entry(i))
                return True
        elif "TASV" in i.desc and float(i.evalue) < 1e-30:
            with open("out.tasv", "a") as out_tasv:
                out_tasv.write(entry(i))
                return True
        elif "mucin" in i.desc and "MASP" not in i.desc and float(i.evalue) < 1e-30:
            with open("out.mucin", "a") as out_mucin:
                out_mucin.write(entry(i))
                return True
        else:
            return False


def anota_solo_brener(mapeos):
    noh = [i for i in mapeos if "hypothetical" not in i.desc.lower() and
           "unnamed" not in i.desc.lower() and "unknown" not in i.desc.lower()]
    m = ""
    for i in noh:
        if i.evalue < 1e-20:
            m = i
            break
    if not len(m):
        m = mapeos[0]
    with open("out.solobrener", "a") as out_solobrener:
        out_solobrener.write(entry(m))


def anota_no_brener(mapeos):
    noh = [i for i in mapeos if "hypothetical" not in i.desc.lower() and
           "unnamed" not in i.desc.lower() and "unknown" not in i.desc.lower()]
    m = ""
    for i in noh:
        if i.evalue < 1e-20:
            m = i
            break
    if not len(m):
        m = mapeos[0]
    with open("out.nobrener", "a") as out_nobrener:
        out_nobrener.write("\t".join(entry(m)))

def anota_no_hypo(mapeos):
    siB = [i for i in mapeos if "TcCLB" in i.sname]
    siBnh = [i for i in mapeos if "TcCLB" in i.sname and "hypothetical" not in
             i.desc.lower() and "unnamed" not in i.desc.lower() and "unknown" not in i.desc.lower()]
    noBRG = [i for i in mapeos if "TcCLB" not in i.sname and "TRSC" not in
             i.sname and "DQ04" not in i.sname]
    noBRGnh = [i for i in mapeos if "TcCLB" not in i.sname and "TRSC" not in
               i.sname and "DQ04" not in i.sname and "hypothetical" not in
               i.desc.lower() and "unnamed" not in i.desc.lower() and "unknown" not in i.desc.lower()]
    m = ""
    n = ""
    for i in siBnh:
        if i.evalue < 1e-30:
            m = i
            break
    if not len(m):
        m = siB[0]
    for i in noBRGnh:
        if i.evalue < 1e-20:
            n = i
            break
    if not len(n):
        n = noBRG[0]
    if ("hypothetical" not in m.desc.lower() and "unnamed" not in m.desc.lower() and
        "unknown" not in m.desc.lower()) or ("hypothetical" not in n.desc.lower() and
        "unnamed" not in n.desc.lower() and "unknown" not in n.desc.lower()):
        with open("out.nohypo", "a") as out_nohypo:
            out_nohypo.write(entry(m, n))
    elif "conserved" in m.desc.lower() and "conserved" in n.desc.lower():
        with open("out.hypocons", "a") as out_hypocons:
            out_hypocons.write(entry(m, n))
    else:
        with open("out.hypo", "a") as out_hypo:
            out_hypo.write(entry(m, n))


def eligiendo(mapeos):
        esflia = False
        checkflia = sum(["MASP" in i.desc or "trans-sialidase" in i.desc or
                         "TASV" in i.desc or "GP63" in i.desc or "RHS" in i.desc
                         or "DGF-1" in i.desc or "mucin" in i.desc for i in mapeos])
        if checkflia:
            esflia = anota_familias(mapeos)
        if not esflia:
            noBRG = [i for i in mapeos if "TcCLB" not in i.sname and "TRSC" not in
                     i.sname and "DQ04" not in i.sname]
            noBRGnh = [i for i in mapeos if "TcCLB" not in i.sname and "TRSC" not in
                       i.sname and "DQ04" not in i.sname and "hypothetical" not in
                       i.desc.lower() and "unnamed" not in i.desc.lower() and
                       "unknown" not in i.desc.lower()]
            siB = [i for i in mapeos if "TcCLB" in i.sname]
            siBRG = [i for i in mapeos if "TcCLB" in i.sname or "TRSC" in
                     i.sname or "DQ04" in i.sname]
            if len(siBRG) == len(mapeos):
                anota_solo_brener(mapeos)
            elif len(mapeos) == len(noBRG) or len(siB) == 0:
                anota_no_brener(mapeos)
            else:
                anota_no_hypo(mapeos)

with open(sys.argv[1]) as blast:
    qname_pre = ""
    for line in blast:
        n += 1
        sname = line.split("\t")[1]
        idn = float(line.split("\t")[2])
        cov = float(line.split("\t")[3]) / float(line.split("\t")[13])
        desc = line.split("\t")[12]
        evalue = line.split("\t")[10]
        if qname_pre != "" and n < nlines:
            qname = line.split()[0]
            if qname_pre != qname:
                eligiendo(mapeos)
                mapeos = []
                qname_pre = qname
                mapeos.append(Mapeo(qname, sname, idn, cov, evalue, desc))
            else:
                mapeos.append(Mapeo(qname, sname, idn, cov, evalue, desc))
        elif n == nlines:
            eligiendo(mapeos)

        else:
            qname_pre = line.split()[0]
            mapeos.append(Mapeo(qname_pre, sname, idn, cov, evalue, desc))
