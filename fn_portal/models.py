from django.db import models
from django.template.defaultfilters import slugify
from django.core.urlresolvers import reverse
from django.db.models import F, Sum, Count


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
    prj_cd = models.CharField(max_length=13, db_index=True, unique=True)
    slug = models.CharField(max_length=13, db_index=True, unique=True)
    prj_nm = models.CharField(max_length=255)
    prj_ldr = models.CharField(max_length=255)
    prj_date0 = models.DateTimeField()
    prj_date1 = models.DateTimeField()
    source =  models.CharField(max_length=255)
    lake =  models.CharField(max_length=20)
    comment0 = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['year', 'prj_cd']
        pass

    def save(self, *args, **kwargs):
        self.slug = slugify(self.prj_cd)
        super(FN011, self).save( *args, **kwargs)

    def __str__(self):
        return '{} - {}'.format(self.prj_cd, self.prj_nm)

    def get_absolute_url(self):
        return reverse('fn_portal.views.project_detail', args=[str(self.slug)])


    def total_catch(self):
        """

        Arguments:
        - `self`:
        """

        total_catch = FN121.objects.filter(project=self).\
              aggregate(total=Sum('effort__catch__catcnt'))

        return total_catch



    def catch_counts(self):
        """

        Arguments:
        - `self`:
        """

        catcnts = FN121.objects.filter(project=self).\
              annotate(species=F('effort__catch__species__common_name')).\
              values('species').\
              annotate(total=Sum('effort__catch__catcnt')).order_by('species')

        return catcnts


class FN121(models.Model):
    '''A table to hold information on fishing events/efforts
    '''
    project = models.ForeignKey(FN011, related_name="samples")

    sam = models.CharField(max_length=5, db_index=True)
    effdt0 = models.DateTimeField(blank=True, null=True)
    effdt1 = models.DateTimeField(blank=True, null=True)
    effdur = models.FloatField(blank=True, null=True)
    efftm0 = models.DateTimeField(blank=True, null=True)
    efftm1 = models.DateTimeField(blank=True, null=True)
    effst = models.CharField(max_length=2, blank=True, null=True)
    grtp = models.CharField(max_length=3, blank=True, null=True)
    gr = models.CharField(max_length=5, blank=True, null=True)
    orient = models.CharField(max_length=2, blank=True, null=True)
    sidep = models.FloatField(default=0, blank=True, null=True)
    grid = models.CharField(max_length=4, db_index=True)
    dd_lat = models.FloatField(blank=True, null=True)
    dd_lon = models.FloatField(blank=True, null=True)
    sitem = models.CharField(max_length=5, blank=True, null=True)
    comment1 = models.CharField(max_length=50, blank=True, null=True)
    secchi = models.FloatField(blank=True, null=True)

    #TODO:
    #geom = models.PointField(srid=4326,
    #                         help_text='Represented as (longitude, latitude)')


    class Meta:
        ordering = ['project', 'sam']
        unique_together = ('project', 'sam')

    def __str__(self):
        return '{}-{}'.format(self.project.prj_cd, self.sam)

    def get_absolute_url(self):
        return reverse('fn_portal.views.sample_detail',
                       args=[str(self.project.slug), str(self.sam)])

    def total_catch(self):
        """

        Arguments:
        - `self`:
        """

        total_catch = FN122.objects.filter(sample=self).\
              aggregate(total=Sum('catch__catcnt'))

        return total_catch


    def catch_counts(self):
        """

        Arguments:
        - `self`:
        """

        catcnts = FN122.objects.filter(sample=self).\
              annotate(species=F('catch__species__common_name')).\
              values('species').\
              annotate(total=Sum('catch__catcnt')).order_by('species')

        return catcnts



class FN122(models.Model):
    '''A table to hold inforamtion about indivual fishing
    efforts(mesh/panel attributes)

    '''
    sample = models.ForeignKey(FN121, related_name="effort")
    #sam = models.CharField(max_length=5, blank=True, null=True)
    eff = models.CharField(max_length=4, blank=True, null=True)
    effdst = models.FloatField(blank=True, null=True)
    grdep = models.FloatField(blank=True, null=True)
    grtem0 = models.FloatField(blank=True, null=True)
    grtem1 = models.FloatField(blank=True, null=True)

    class Meta:
        #ordering = ['last_name', 'first_name']
        unique_together = ('sample', 'eff')

    def __str__(self):
        return '{}-{}'.format(self.sample,
                                 self.eff)


class FN123(models.Model):
    ''' a table for catch counts.
    '''

    effort = models.ForeignKey(FN122, related_name="catch")
    species = models.ForeignKey(Species, related_name="species")

    grp = models.CharField(max_length=3, default='00')
    catcnt = models.IntegerField(blank=True, null=True)
    biocnt = models.IntegerField(default=0, blank=True, null=True)
    #these are text and probably shouldn't be:
    comment = models.TextField(blank=True, null=True)


    class Meta:
        #ordering = ['last_name', 'first_name']
        unique_together = ('effort', 'species', 'grp')

    def __str__(self):
        return '{}-{}-{}'.format(self.effort,
                              self.species.species_code,
                              self.grp)


class FN125(models.Model):
    '''A table for biological data collected from fish
    '''

    catch = models.ForeignKey(FN123, related_name="fish")

    fish = models.CharField(max_length=6)
    flen = models.IntegerField(blank=True, null=True)
    tlen = models.IntegerField(blank=True, null=True)
    rwt = models.IntegerField(blank=True, null=True)
    clipc = models.CharField(max_length=6, blank=True, null=True)
    sex = models.CharField(max_length=2, blank=True, null=True)
    mat = models.CharField(max_length=2, blank=True, null=True)
    gon = models.CharField(max_length=4, blank=True, null=True)
    noda = models.CharField(max_length=6, blank=True, null=True)
    nodc = models.CharField(max_length=6, blank=True, null=True)
    comment5 = models.CharField(max_length=50, blank=True, null=True)


    class Meta:
        #ordering = ['last_name', 'first_name']
        unique_together = ('catch', 'fish')
        pass

    def __str__(self):
        pass


class FN127(models.Model):
    '''A table for age interpretations collected from fish
    '''

    fish = models.ForeignKey(FN125, related_name="age_estimates")

    ageid = models.IntegerField()
    agea = models.IntegerField(blank=True, null=True)
    accepted = models.BooleanField(default=False)
    agest = models.CharField(max_length=5, blank=True, null=True)
    xagem = models.CharField(max_length=2, blank=True, null=True)
    agemt = models.CharField(max_length=5)
    edge = models.CharField(max_length=2, blank=True, null=True)
    conf = models.IntegerField(blank=True, null=True)
    nca = models.IntegerField(blank=True, null=True)

    class Meta:
        #ordering = ['last_name', 'first_name']
        #unique_together = ('fish', 'tagnum', 'grp')
        pass

    def __str__(self):
        return '{}-{}({})'.format(self.fish,
                              self.agea,
                              self.ageid)


#class FN_Lamprey(models.Model):
#    ''' a table for lamprey data.
#    '''
#
#    fish = models.ForeignKey(FN125, related_name="tags")
#    #lamprey flags - these belong in child table
#    lam_flag = models.CharField(max_length=1)
#    xlam = models.CharField(max_length=6, blank=True, null=True)
#    lamijc = models.CharField(max_length=50, blank=True, null=True)
#
#    class Meta:
#        #ordering = ['last_name', 'first_name']
#        #unique_together = ('fish', 'tagnum', 'grp')
#
#    def __str__(self):
#
#        if self.xlam:
#            return '{}-{}'.format(self.fish,
#                                  self.xlam)
#        else:
#            return '{}-{}'.format(self.fish,
#                                  self.lamijc)
#


class FN_Tags(models.Model):
    ''' a table for the tag(s) assoicated with a fish.
    '''

    fish = models.ForeignKey(FN125, related_name="tags")
    #tag fields
    tagstat = models.CharField(max_length=5, blank=True, null=True)
    tagid = models.CharField(max_length=9, blank=True, null=True)
    tagdoc = models.CharField(max_length=6, blank=True, null=True)
    xcwtseq = models.CharField(max_length=5, blank=True, null=True)
    xtaginckd = models.CharField(max_length=6, blank=True, null=True)
    xtag_chk = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        #ordering = ['last_name', 'first_name']
        #unique_together = ('fish', 'tagnum', 'grp')
        pass

    def __str__(self):
        return '{}-{}({})'.format(self.fish,
                              self.tagnum,
                              self.tagid)
