from django.db import models
from django.template.defaultfilters import slugify

class Species(models.Model):
    species_code = models.IntegerField(unique=True)
    common_name = models.CharField(max_length=40, null=True, blank=True)
    scientific_name = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        ordering = ['common_name']
        verbose_name_plural = "Species"

    def __str__(self):
        if self.scientific_name:
            spc_unicode = "{} ({})".format(self.common_name,
                                          self.scientific_name)
        else:
            spc_unicode =  "{}".format(self.common_name)
        return spc_unicode


class FN011(models.Model):
    ''' Project meta data.
    '''

    year = models.CharField(max_length=4, db_index=True)
    prj_date0 = models.DateTimeField()
    prj_date1 = models.DateTimeField()
    prj_cd = models.CharField(max_length=13, db_index=True, unique=True)
    prj_nm = models.CharField(max_length=255)
    prj_ldr = models.CharField(max_length=255)
    aru = models.CharField(max_length=3, blank=True, null=True)
    comment0 = models.TextField(blank=True, null=True)
    entry = models.CharField(max_length=7, blank=True, null=True)
    f1 = models.CharField(max_length=2, blank=True, null=True)
    fof_loc = models.CharField(max_length=31, blank=True, null=True)
    fof_nm = models.CharField(max_length=36, blank=True, null=True)
    gaz_nm = models.CharField(max_length=21, blank=True, null=True)
    local_nm = models.CharField(max_length=21, blank=True, null=True)
    mode_cnt = models.CharField(max_length=3, blank=True, null=True)
    prj_his = models.TextField(blank=True, null=True)
    prj_rdo = models.FloatField(default=0, blank=True, null=True)
    prj_size = models.FloatField(default=0, blank=True, null=True)
    prj_ver = models.CharField(max_length=16, blank=True, null=True)
    space_cnt = models.CharField(max_length=3, blank=True, null=True)
    ssn_cnt = models.CharField(max_length=3, blank=True, null=True)
    unit_lc = models.CharField(max_length=31, blank=True, null=True)
    unit_nm = models.CharField(max_length=31, blank=True, null=True)
    v0 = models.CharField(max_length=5, blank=True, null=True)
    v11 = models.CharField(max_length=5, blank=True, null=True)
    wb_cd = models.CharField(max_length=7, blank=True, null=True)
    wby = models.CharField(max_length=8, blank=True, null=True)
    wby_nm = models.CharField(max_length=26, blank=True, null=True)
    min_dd_lat = models.FloatField(default=0, blank=True, null=True)
    max_dd_lat = models.FloatField(default=0, blank=True, null=True)
    min_dd_lon = models.FloatField(default=0, blank=True, null=True)
    max_dd_lon = models.FloatField(default=0, blank=True, null=True)

    class Meta:
        #ordering = ['last_name', 'first_name']
        #unique_together = ('last_name', 'first_name')
        pass

    def __str__(self):
        return '{} - {}'.format(self.prj_cd, self.prj_nm)


class FN121(models.Model):
    '''A table to hold information on fishing events/efforts
    '''
    project = models.ForeignKey(FN011, related_name="Project")

    sam = models.CharField(max_length=5, db_index=True)
    grid = models.CharField(max_length=4, db_index=True)
    effdt0 = models.DateTimeField(blank=True, null=True)
    effdt1 = models.DateTimeField(blank=True, null=True)
    effdur = models.FloatField(blank=True, null=True)
    efftm0 = models.DateTimeField(blank=True, null=True)
    efftm1 = models.DateTimeField(blank=True, null=True)
    effst = models.CharField(max_length=2, blank=True, null=True)
    gr = models.CharField(max_length=5, blank=True, null=True)
    orient = models.CharField(max_length=2, blank=True, null=True)
    sidep = models.FloatField(default=0, blank=True, null=True)
    latlong = models.CharField(max_length=14, blank=True, null=True)
    siloc = models.CharField(max_length=12, blank=True, null=True)
    lat = models.CharField(max_length=50, blank=True, null=True)
    lon = models.CharField(max_length=50, blank=True, null=True)
    xy_type = models.CharField(max_length=3,blank=True, null=True)
    dd_lat = models.FloatField(blank=True, null=True)
    dd_lon = models.FloatField(blank=True, null=True)
    dd_lat2 = models.FloatField(blank=True, null=True)
    dd_lon2 = models.FloatField(blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)
    grtp = models.CharField(max_length=3, blank=True, null=True)
    area = models.CharField(max_length=3, blank=True, null=True)
    site = models.CharField(max_length=4, blank=True, null=True)
    sitem = models.CharField(max_length=5, blank=True, null=True)
    xfishnam = models.CharField(max_length=9, blank=True, null=True)
    xgryarn = models.CharField(max_length=2, blank=True, null=True)
    xorient = models.CharField(max_length=2, blank=True, null=True)
    xset = models.CharField(max_length=2, blank=True, null=True)
    xstat = models.CharField(max_length=3, blank=True, null=True)
    spctrg = models.CharField(max_length=50,blank=True, null=True)
    comment1 = models.CharField(max_length=50, blank=True, null=True)
    secchi = models.FloatField(blank=True, null=True)
    xslime = models.CharField(max_length=2, blank=True, null=True)


#CREATE UNIQUE INDEX [PrimaryKey] ON [Offshore_FN121] (Key_FN121 ASC) WITH PRIMARY DISALLOW NULL;
#CREATE INDEX [GRID] ON [Offshore_FN121] (GRID ASC);
#CREATE INDEX [Key] ON [Offshore_FN121] (Key_FN121 ASC);
#CREATE INDEX [Key_FN011] ON [Offshore_FN121] (Key_FN011 ASC);
#CREATE INDEX [Offshore_FN121YEAR] ON [Offshore_FN121] (YEAR ASC);


    class Meta:
        #ordering = ['last_name', 'first_name']
        unique_together = ('project', 'sam')


    def __str__(self):
        return '{}-{}'.format(self.project.prj_cd, self.sam)


class FN122(models.Model):
    '''A table to hold inforamtion about indivual fishing
    efforts(mesh/panel attributes)

    '''

    sample = models.ForeignKey(FN121, related_name="sample")
    #sam = models.CharField(max_length=5, blank=True, null=True)
    eff = models.CharField(max_length=4, blank=True, null=True)
    effdst = models.FloatField(blank=True, null=True)
    grdep = models.FloatField(blank=True, null=True)
    grtem0 = models.FloatField(blank=True, null=True)
    grtem1 = models.FloatField(blank=True, null=True)
    stratum = models.CharField(max_length=8, blank=True, null=True)
    xeffday = models.CharField(max_length=3, blank=True, null=True)
    xeffdsta = models.CharField(max_length=6, blank=True, null=True)
    xeffdstb = models.CharField(max_length=6, blank=True, null=True)
    xgrdep = models.CharField(max_length=4, blank=True, null=True)
    xgrdepa = models.CharField(max_length=4, blank=True, null=True)
    xgrdepb = models.CharField(max_length=4, blank=True, null=True)
    xgrtem = models.CharField(max_length=4, blank=True, null=True)
    xgrtema = models.CharField(max_length=5, blank=True, null=True)
    xgrtemb = models.CharField(max_length=5, blank=True, null=True)
    xsidep = models.CharField(max_length=4, blank=True, null=True)
    xsidepa = models.CharField(max_length=4, blank=True, null=True)
    xsidepb = models.CharField(max_length=4, blank=True, null=True)


    class Meta:
        #ordering = ['last_name', 'first_name']
        unique_together = ('sample', 'eff')

    def __str__(self):
        return '{}-{}'.format(self.sample,
                                 self.eff)



class FN123(models.Model):
    ''' a table for catch counts.
    '''

    effort = models.ForeignKey(FN121, related_name="effort")
    species = models.ForeignKey(Species, related_name="species")

    grp = models.CharField(max_length=3, default='00', blank=True, null=True)
    catcnt = models.IntegerField(blank=True, null=True)
    biocnt = models.IntegerField(default=0, blank=True, null=True)
    kilcnt = models.IntegerField(default=0, blank=True, null=True)
    mrkcnt = models.IntegerField(default=0, blank=True, null=True)
    rcpcnt = models.IntegerField(default=0, blank=True, null=True)
    rlscnt = models.IntegerField(default=0, blank=True, null=True)
    #these are text and probably shouldn't be:
    catwt = models.CharField(max_length=8, blank=True, null=True)
    stratum = models.CharField(max_length=9, blank=True, null=True)
    xcatcnta = models.CharField(max_length=6, blank=True, null=True)
    xcatcntb = models.CharField(max_length=6, blank=True, null=True)
    xlntally = models.CharField(max_length=6, blank=True, null=True)
    xtally = models.CharField(max_length=5, blank=True, null=True)
    comment0 = models.TextField(blank=True, null=True)
    comment3 = models.TextField(blank=True, null=True)

    class Meta:
        #ordering = ['last_name', 'first_name']
        unique_together = ('effort', 'species', 'grp')

    def __str__(self):
        pass


class FN125(models.Model):
    '''A table for biological data collected from fish
    '''
    class Meta:
        #ordering = ['last_name', 'first_name']
        #unique_together = ('last_name', 'first_name')
        pass

    def __str__(self):
        pass
