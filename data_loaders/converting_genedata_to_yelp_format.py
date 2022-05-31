import os
import csv
import json

DATA_DIR = "../datasets/GeneCards"


def load_gen_func_description(concat=True):
    fun_des_file = csv.reader(open("%s/GeneFuncDescriptionsV5.7.csv" % DATA_DIR))
    next(fun_des_file, None)

    p_gene = ""
    p_des = []
    MIN_LEN_DES = 14
    gene_2_des = {}
    for row in fun_des_file:
        c_gene = row[0]
        c_des = row[2]
        if c_des.startswith("Reaction"):
            continue
        elif len(c_des) < MIN_LEN_DES:
            continue
        if c_gene == p_gene:
            p_des.append(c_des)
        else:
            if p_gene != "":
                if concat:
                    p_des = "".join(p_des)
                gene_2_des[p_gene] = p_des
            p_gene = c_gene
            p_des = [c_des]
    if concat:
        p_des = "".join(p_des)
    gene_2_des[p_gene] = p_des
    return gene_2_des


def load_gen_sum(concat=True):
    sum_des_file = csv.reader(open("%s/GeneSummariesV5.7.csv" % DATA_DIR))
    next(sum_des_file, None)

    MIN_LEN_DES = 2
    p_gene = ""
    p_des = []
    gene_2_sum = {}

    for row in sum_des_file:
        c_gene = row[0]
        c_des = row[2]
        if c_des.startswith("Reaction"):
            continue
        elif len(c_des) < MIN_LEN_DES:
            continue
        if c_gene == p_gene:
            p_des.append(c_des)
        else:
            if p_gene != "":
                if concat:
                    p_des = "".join(p_des)
                gene_2_sum[p_gene] = p_des
            p_gene = c_gene
            p_des = [c_des]

    if concat:
        p_des = "".join(p_des)
    gene_2_sum[p_gene] = p_des
    return gene_2_sum


def get_update_dict(d, k, v):
    try:
        v = d[k]
    except:
        d[k] = v
    return v


def get_dict(d, k, v=-1):
    try:
        v = d[k]
    except:
        pass
    return v


def load_pathway2gene():
    gp_file = csv.reader(open("%s/GenePathwaysV5.7.csv" % DATA_DIR))
    next(gp_file, None)
    pwid_2_name = {}
    pw_id_2_gene = {}
    for row in gp_file:
        gen_id = row[0]
        pw_id = row[3]
        pw_name = row[1]
        pw_g = get_update_dict(pw_id_2_gene, pw_id, [])
        pw_g.append(gen_id)
        pwid_2_name[pw_id] = pw_name
    return pw_id_2_gene, pwid_2_name


def export_gene_data(mode=0):
    pw_2_gene, pw_2_name = load_pathway2gene()
    gene_2_des = load_gen_func_description()
    gen_2_sum = load_gen_sum()
    # Business file
    f_business = open("%s/business.json" % DATA_DIR, "w")
    for pw, name in pw_2_name.items():
        f_business.write(json.dumps({"business_id": pw, "name": name}) + "\n")
    f_business.close()
    # Review file
    f_review = open("%s/review_%s.json" % (DATA_DIR, mode), "w")
    for pw, genes in pw_2_gene.items():
        for gene in genes:
            gen_des = get_dict(gene_2_des, gene, "")
            if mode == 2:
                gen_des = gen_des +"." + get_dict(gen_2_sum, gene, "")
            elif mode == 1:
                gen_des = get_dict(gen_2_sum, gene, "")
            js = {"review_id": pw+"_"+gene, "user_id": gene, "business_id": pw, "text": gen_des,
                  "stars":1.0,"useful":1,"funny":1,"cool":1}
            f_review.write(json.dumps(js)+"\n")
    f_review.close()

def tt():
    ar = {"a": 1}
    s = json.dumps(ar)
    print(s)


if __name__ == "__main__":
    # d = load_gen_func_description()
    # d = load_gen_sum()
    # tt()
    export_gene_data(mode=0)
    export_gene_data(mode=1)
    export_gene_data(mode=2)

    # print(d)
