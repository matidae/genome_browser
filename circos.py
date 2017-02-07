import sys
from operator import itemgetter


def select_contigs(blast, main_contig):
    dcov = {}
    dlen = {}
    lcontigs = []
    for i in blast:
        name = i.split()[1]
        cov = int(i.split()[3])
        slen = int(i.split()[13])
        if name != main_contig:
            if name not in dcov.keys():
                dcov[name] = cov
                dlen[name] = slen
            else:
                dcov[name] += cov
    dcov_sort = sorted(dcov, key=dcov.get, reverse=True)[:11]
    for i in sorted(dlen, key=dlen.get, reverse=True):
        if i in dcov_sort:
            lcontigs.append((i, dlen[i]))
    return lcontigs


def order_contigs(lcontigs):
    olcontigs = []
    m = 0
    n = len(lcontigs)-1
    for i in xrange(len(lcontigs)):
        if i%2 == 0:
            olcontigs.append(lcontigs[m])
            m += 1
        else:
            olcontigs.append(lcontigs[n])
            n -= 1
    return olcontigs


def create_karyo(olcontigs, main_contig, color):
        outk = open("out.karyo", "w")
        c = 0
        outk.write(" ".join(["chr", "-", main_contig[0], main_contig[0], "1",
                   str(main_contig[1]), "red", "\n"]))
        for elem in olcontigs:
            name = elem[0]
            length = elem[1]
            outk.write(" ".join(["chr", "-", name, name, "1", str(length),
                       color[c], "\n"]))
            c += 1
        outk.close()


def create_links(olcontigs, main_contig, blast, color):
    outl = open("out.links", "w")
    qname = main_contig[0]
    count = 0
    for i in xrange(len(olcontigs)):
        olname = olcontigs[i][0]
        olcolor = color[i]
        for j in blast:
            if j.split()[1] == olname:
                qstart = j.split()[6]
                qend = j.split()[7]
                sstart = j.split()[8]
                send = j.split()[9]
                qlength = j.split()[12]
                slength = j.split()[13]
                outl.write(" ".join(["a" + str(count), qname, qstart, qend,
                                     "color=" + olcolor, "\n"]))
                outl.write(" ".join(["a" + str(count), olname, sstart, send,
                                     "color=" + olcolor, "\n"]))
                count += 1
    outl.close()


if __name__ == "__main__":
    color = ["blue_a2", "yellow_a2", "green_a2", "purple_a2", "orange_a2",
             "grey_a2", "vdblue_a2", "vdyellow_a2", "vdgreen_a2", "vdpurple_a2",
             "vdorange_a2", "vdgrey_a2", "red_a2", "blue_a2", "yellow_a2",
             "green_a2", "purple_a2", "orange_a2", "red_a2", "grey_a2"]
    blast = open(sys.argv[1]).readlines()
    main_contig = sys.argv[2]
    main_contig_len = int(blast[0].split()[12])
    lcontigs = select_contigs (blast, main_contig)
    main_contig = (main_contig, main_contig_len)
    olcontigs = order_contigs(lcontigs)
    create_karyo(olcontigs, main_contig, color)
    create_links(olcontigs, main_contig, blast, color)
