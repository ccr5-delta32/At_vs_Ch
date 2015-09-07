# At_vs_Ch

If you are reading this and you are not me then hear this:

These scripts should be useless to you other than to get some ideas of how to do or not to do some things.

How to use this:

'Accession_selection' contains the method for selecting arabidopsis accessions from the final set of the 1001 genomes project. 
1.) create the MySQL table using 'create_At_Variants.py'. 
2.) populate the table with variants from the .sdi or .sdi.gz using 'populate_MAGIC_At_Variants.py' or 'populate_close2Ch_At_Variants.py'.
3.) use stuff in 'At_SNP_tables' to create reorganized tables.
4.) use 'At_fasta.py' to produce FASTA alignment of SNPs and list of positions of those SNPs.
5.) use the files from (4) to run SweeD and OmegaPlus like in 'sweep_analysis'.

