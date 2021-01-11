# -*- coding: utf-8 -*-
#/bin/python
#Pipeline for single cell analysis,


import sys
import re
import os


##THE REF FILES ARE FOR GPMP6
##GRcH38: /diazlab/refs/Homo_sapiens/refdata-cellranger-GRCh38-1.2.0
##vartrix: /home/fcatalan/bin/vartrix-v1.1.0-x86_64-linux/vartrix
##annovar: /diazlab/shared/annovar/
##CONICS: /diazlab/software/CONICS/run_CONICS.sh
##reference directory
refDir="/diazlab/fcatalan/ref"

BamList=open(sys.argv[1],'r')#Col1: xxx.bam, Col2: Path to xxx_barcode_file, Clo3: Path to directory_tumor_bam_files



for line in BamList:
    line=line.strip()
    line=line.split()
    print(line)
    ##aa=line[0].split('/')
    bamName=line[0].split('.bam')

    #variants calling
    c='java -Xmx60g -jar /home/shared/cbc/software_cbc/picard-tools-1.67/AddOrReplaceReadGroups.jar  I='+'%s'%line[0]+' O='+'%s'%bamName[0]+'_added_sorted.bam SO=coordinate RGID=singl_cell RGLB=single_cell RGPL=ILLUMINA RGPU=1 RGSM=1'
    os.system(c)
    d='java -Xmx60g -jar /home/shared/cbc/software_cbc/picard-tools-1.67/MarkDuplicates.jar I='+'%s'%bamName[0]+'_added_sorted.bam O='+'%s'%bamName[0]+'_added_sorted_MarkD.bam CREATE_INDEX=true VALIDATION_STRINGENCY=SILENT M=output.metrics'
    os.system(d)
    e='java -Xmx50g -jar /home/dhu/gatk/GenomeAnalysisTK.jar -T SplitNCigarReads -R /diazlab/fcatalan/ref/genome.fa -I '+'%s'%bamName[0]+'_added_sorted_MarkD.bam -o '+'%s'%bamName[0]+'_added_sorted_MarkD_split.bam -rf ReassignOneMappingQuality -RMQF 255 -RMQT 60 -U ALLOW_N_CIGAR_READS'
    os.system(e)
    f='java -Xmx50g -jar /home/dhu/gatk/GenomeAnalysisTK.jar -T HaplotypeCaller -R /diazlab/fcatalan/ref/genome.fa -I '+'%s'%bamName[0]+'_added_sorted_MarkD_split.bam'+' -dontUseSoftClippedBases -stand_call_conf 20.0 -stand_emit_conf 20.0 -o '+'%s'%bamName[0]+'_added_sorted_MarkD_split.vcf'
    os.system(f)
    g='java -jar /diazlab/shared/bin/picard-tools-1.124/picard.jar SortVcf I='+'%s'%bamName[0]+'_added_sorted_MarkD_split.vcf'+' O='+'%s'%bamName[0]+'_added_sorted.MarkD.split.order.vcf SD=/diazlab/fcatalan/ref/genome.dict'
    os.system(g)
    h='java -jar /home/dhu/gatk/GenomeAnalysisTK.jar -T VariantFiltration -R /diazlab/fcatalan/ref/genome.fa -V '+'%s'%bamName[0]+'_added_sorted.MarkD.split.order.vcf -U ALLOW_SEQ_DICT_INCOMPATIBILITY -window 35 -cluster 3 -filterName FS -filter "FS >30.0" -filterName QD -filter "QD<2.0" -o '+'%s'%bamName[0]+'_added_sorted.MarkD.split.order.filter.vcf'
    os.system(h)
    i='/opt/local/bin/python2.7 /diazlab/fcatalan/diazlab_code/mutation_calling/vcfPass.py '+'%s'%bamName[0]+'_added_sorted.MarkD.split.order.filter.vcf '+'%s'%bamName[0]+'_added_sorted.MarkD.split.order.filter.PASS.vcf'
    os.system(i)

    #annotate variants through annovar
    j='/diazlab/shared/annovar/table_annovar.pl '+'%s'%bamName[0]+'_added_sorted.MarkD.split.order.filter.PASS.vcf /diazlab/fcatalan/ref/humandb -buildver hg38 -out '+'%s'%bamName[0]+' -remove -protocol refGene,avsnp147,cosmic70,ljb26_all,esp6500siv2_all -operation g,f,f,f,f -nastring . -vcfinput'
    os.system(j)
    ll='grep -v "\<rs" '+'%s'%bamName[0]+'.hg38_multianno.txt | grep "nonsynonymous" > '+'%s'%bamName[0]+'.hg38_multianno.txt_nonsy'
    os.system(ll)
    #convert from to vartrix compartible input files
    mm='/opt/local/bin/python2.7 /diazlab/fcatalan/diazlab_code/mutation_calling/vcf2vartrix.py '+'%s'%bamName[0]+'.hg38_multianno.txt_nonsy '+'%s'%bamName[0]+'.hg38_multianno.vcf '+'%s'%bamName[0]+'.hg38_multianno.txt_nonsy.vcf'
    os.system(mm)
    mmm='/opt/local/bin/python2.7 /diazlab/fcatalan/diazlab_code/mutation_calling/vcfFilter4vartrix.py '+'%s'%bamName[0]+'.hg38_multianno.txt_nonsy.vcf '+'%s'%bamName[0]+'.hg38_multianno.txt_nonsy_filter.vcf'
    os.system(mmm)
    #Extracting single cell variant information from 10x Genomics single cell data using VarTrix
    m='/home/fcatalan/vartrix-v1.1.0-x86_64-linux/vartrix --bam '+'%s'%line[0]+' --cell-barcodes '+'%s'%line[1]+' --fasta /diazlab/fcatalan/ref/genome.fa --mapq 10 --out-matrix '+'%s'%bamName[0]+'_filter.vartrix'+' --out-variants '+'%s'%bamName[0]+'_filter.vartrix.variants --threads 8 --vcf '+'%s'%bamName[0]+'.hg38_multianno.txt_nonsy_filter.vcf'
    os.system(m)
    m2='/home/fcatalan/vartrix-v1.1.0-x86_64-linux/vartrix --bam '+'%s'%line[0]+' --cell-barcodes '+'%s'%line[1]+' --fasta /diazlab/fcatalan/ref/genome.fa --mapq 10 --out-matrix '+'%s'%bamName[0]+'.vartrix'+' --out-variants '+'%s'%bamName[0]+'.vartrix.variants --threads 8 --vcf '+'%s'%bamName[0]+'.hg38_multianno.txt_nonsy.vcf'
    os.system(m2)
BamList.close()
