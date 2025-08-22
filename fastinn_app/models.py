
from django.db import models


class FastinnData(models.Model):
    id = models.CharField(db_column='id', primary_key=True)
    faerslunumer = models.IntegerField(db_column='FAERSLUNUMER', blank=True, null=True)
    emnr = models.IntegerField(db_column='EMNR', blank=True, null=True)
    skjalanumer = models.TextField(db_column='SKJALANUMER', blank=True, null=True)  
    fastnum = models.IntegerField(db_column='FASTNUM', blank=True, null=True)
    heimilisfang = models.TextField(db_column='HEIMILISFANG', blank=True, null=True)  
    postnr = models.FloatField(db_column='POSTNR', blank=True, null=True)
    heinum = models.FloatField(db_column='HEINUM', blank=True, null=True)
    svfn = models.IntegerField(db_column='SVFN', blank=True, null=True)
    sveitarfelag = models.TextField(db_column='SVEITARFELAG', blank=True, null=True)  
    utgdag = models.TextField(db_column='UTGDAG', blank=True, null=True)  
    thinglystdags = models.TextField(db_column='THINGLYSTDAGS', blank=True, null=True)  
    kaupverd = models.IntegerField(db_column='KAUPVERD', blank=True, null=True)
    fasteignamat = models.TextField(db_column='FASTEIGNAMAT', blank=True, null=True)  
    fasteignamat_gildandi = models.FloatField(db_column='FASTEIGNAMAT_GILDANDI', blank=True, null=True)
    fyrirhugad_fasteignamat = models.FloatField(db_column='FYRIRHUGAD_FASTEIGNAMAT', blank=True, null=True)
    brunabotamat_gildandi = models.FloatField(db_column='BRUNABOTAMAT_GILDANDI', blank=True, null=True)
    byggar = models.FloatField(db_column='BYGGAR', blank=True, null=True)
    fepilog = models.TextField(db_column='FEPILOG', blank=True, null=True)  
    einflm = models.FloatField(db_column='EINFLM', blank=True, null=True)
    lod_flm = models.FloatField(db_column='LOD_FLM', blank=True, null=True)
    lod_flmein = models.TextField(db_column='LOD_FLMEIN', blank=True, null=True)  
    fjherb = models.FloatField(db_column='FJHERB', blank=True, null=True)
    tegund = models.TextField(db_column='TEGUND', blank=True, null=True)  
    fullbuid = models.IntegerField(db_column='FULLBUID', blank=True, null=True)
    onothaefur_samningur = models.IntegerField(db_column='ONOTHAEFUR_SAMNINGUR', blank=True, null=True)
    date = models.TextField(db_column='DATE', blank=True, null=True)
    source = models.TextField(db_column='SOURCE', blank=True, null=True)
    fermetravera = models.FloatField(db_column='fermetravera', blank=True, null=True)


    class Meta:
        managed = False
        db_table = 'fastinn_data'
        # ordering = ['-id']
