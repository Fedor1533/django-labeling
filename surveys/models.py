from django.db import models
from django.utils.text import Truncator
from django.contrib.auth.models import User


class Survey(models.Model):
    name = models.PositiveIntegerField(unique=True)
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(blank=True, null=True)
    description = models.TextField(max_length=1000)

    def __str__(self):
        return 'Survey {}'.format(self.name)

    def get_sources_count(self):
        return Source.objects.filter(survey=self).count()


class Source(models.Model):
    name = models.CharField(max_length=150, unique=True)

    RA = models.DecimalField(max_digits=9, decimal_places=5)
    DEC = models.DecimalField(max_digits=9, decimal_places=5)

    ztf_name = models.CharField(max_length=100, blank=True, null=True)
    comment = models.TextField(max_length=2000, blank=True, null=True)

    CLASS_CHOICES = [
        ('TDE', 'TDE Source'),
        ('NOT TDE', 'Not TDE Source'),
        ('NaN', 'Unknown Source'),
    ]
    source_class = models.CharField(
        max_length=20,
        choices=CLASS_CHOICES,
        default='NaN',
        blank=True, null=True,
    )

    master_source = models.BooleanField(default=True, blank=True, null=True)
    dup_id = models.PositiveIntegerField(blank=True, null=True)

    # TODO: Think about formats and view of NEW fields
    L = models.FloatField(blank=True, null=True),
    B = models.FloatField(blank=True, null=True),
    R98 = models.FloatField(blank=True, null=True),
    g_d2d = models.FloatField(blank=True, null=True),
    g_s = models.FloatField(blank=True, null=True),
    g_nsrc = models.FloatField(blank=True, null=True),
    g_gmag = models.FloatField(blank=True, null=True),
    s_d2d = models.FloatField(blank=True, null=True),
    s_id = models.FloatField(blank=True, null=True),
    s_z = models.FloatField(blank=True, null=True),
    s_otype = models.FloatField(blank=True, null=True),
    # w1,2,3
    w_e1 = models.DecimalField(max_digits=9, decimal_places=5, blank=True, null=True)
    w_e2 = models.DecimalField(max_digits=9, decimal_places=5, blank=True, null=True)
    w_e3 = models.DecimalField(max_digits=9, decimal_places=5, blank=True, null=True)

    # w1_snr,2,3
    w_snr_e1 = models.DecimalField(max_digits=9, decimal_places=5, blank=True, null=True)
    w_snr_e2 = models.DecimalField(max_digits=9, decimal_places=5, blank=True, null=True)
    w_snr_e3 = models.DecimalField(max_digits=9, decimal_places=5, blank=True, null=True)

    w_nsrc = models.DecimalField(max_digits=9, decimal_places=5, blank=True, null=True)
    flag_agn_wise = models.DecimalField(max_digits=9, decimal_places=5, blank=True, null=True)
    flag_xray = models.DecimalField(max_digits=9, decimal_places=5, blank=True, null=True)
    flag_radio = models.DecimalField(max_digits=9, decimal_places=5, blank=True, null=True)
    sdss_p = models.DecimalField(max_digits=9, decimal_places=5, blank=True, null=True)
    sdss_nsrc = models.DecimalField(max_digits=9, decimal_places=5, blank=True, null=True)
    RATIO_e2e1 = models.DecimalField(max_digits=9, decimal_places=5, blank=True, null=True)
    # FLUX_e2,3,4
    FLUX_e1 = models.DecimalField(max_digits=9, decimal_places=5, blank=True, null=True)
    FLUX_e2 = models.DecimalField(max_digits=9, decimal_places=5, blank=True, null=True)
    FLUX_e3 = models.DecimalField(max_digits=9, decimal_places=5, blank=True, null=True)

    # CTS_e2,3,4
    CTS_e1 = models.DecimalField(max_digits=9, decimal_places=5, blank=True, null=True)
    CTS_e2 = models.DecimalField(max_digits=9, decimal_places=5, blank=True, null=True)
    CTS_e3 = models.DecimalField(max_digits=9, decimal_places=5, blank=True, null=True)

    # EXP_e2,3,4
    EXP_e1 = models.DecimalField(max_digits=9, decimal_places=5, blank=True, null=True)
    EXP_e2 = models.DecimalField(max_digits=9, decimal_places=5, blank=True, null=True)
    EXP_e3 = models.DecimalField(max_digits=9, decimal_places=5, blank=True, null=True)
    # LIKE_e2,3,4
    LIKE_e1 = models.DecimalField(max_digits=9, decimal_places=5, blank=True, null=True)
    LIKE_e2 = models.DecimalField(max_digits=9, decimal_places=5, blank=True, null=True)
    LIKE_e3 = models.DecimalField(max_digits=9, decimal_places=5, blank=True, null=True)

    G_L_e2 = models.DecimalField(max_digits=9, decimal_places=5, blank=True, null=True)
    G_e2 = models.DecimalField(max_digits=9, decimal_places=5, blank=True, null=True)
    G_U_e2 = models.DecimalField(max_digits=9, decimal_places=5, blank=True, null=True)
    Tin_L_e2 = models.DecimalField(max_digits=9, decimal_places=5, blank=True, null=True)
    Tin_e2 = models.DecimalField(max_digits=9, decimal_places=5, blank=True, null=True)
    Tin_U_e2 = models.DecimalField(max_digits=9, decimal_places=5, blank=True, null=True)
    NH_L_e2 = models.DecimalField(max_digits=9, decimal_places=5, blank=True, null=True)
    NH_e2 = models.DecimalField(max_digits=9, decimal_places=5, blank=True, null=True)
    NH_U_e2 = models.DecimalField(max_digits=9, decimal_places=5, blank=True, null=True)
    # UPLIM_e1,2,3,4
    UPLIM_e1 = models.DecimalField(max_digits=9, decimal_places=5, blank=True, null=True)
    UPLIM_e2 = models.DecimalField(max_digits=9, decimal_places=5, blank=True, null=True)
    UPLIM_e3 = models.DecimalField(max_digits=9, decimal_places=5, blank=True, null=True)

    # TSTART_e1,2,3,4
    TSTART_e1 = models.CharField(max_length=100, blank=True, null=True)
    TSTART_e2 = models.CharField(max_length=100, blank=True, null=True)
    TSTART_e3 = models.CharField(max_length=100, blank=True, null=True)

    # TSTOP_e1,2,3,4
    TSTOP_e1 = models.CharField(max_length=100, blank=True, null=True)
    TSTOP_e2 = models.CharField(max_length=100, blank=True, null=True)
    TSTOP_e3 = models.CharField(max_length=100, blank=True, null=True)
    # END of new fields

    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name='sources')

    def __str__(self):
        return 'Source: {}'.format(self.name)

    def get_comment_count(self):
        return Comment.objects.filter(source=self).count()

    def get_last_comment(self):
        return Comment.objects.filter(source=self).order_by('-created_at').first()

    def __iter__(self):
        f_list = ['comments', 'master_source', 'survey']  # TODO: how to not show fields smarter
        for field in self._meta.get_fields():
            if field.name not in f_list:
                value = getattr(self, field.name, None)
                yield (field.name, value)


class Comment(models.Model):
    comment = models.TextField(max_length=2000)
    follow_up = models.TextField(max_length=1000, blank=True, null=True)

    source_class = models.CharField(
        max_length=20,
        choices=Source.CLASS_CHOICES,
        default='NaN',
        blank=True, null=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    updated_at = models.DateTimeField(blank=True, null=True)

    source = models.ForeignKey(Source, on_delete=models.CASCADE, related_name='comments')

    def __str__(self):
        truncated_comment = Truncator(self.comment)
        return 'Comment: {}'.format(truncated_comment.chars(10))


class OptSource(models.Model):
    name = models.CharField(max_length=150)

    RA = models.DecimalField(max_digits=9, decimal_places=5)
    DEC = models.DecimalField(max_digits=9, decimal_places=5)

    ztf_name = models.CharField(max_length=100, blank=True, null=True)

    source_class = models.CharField(
        max_length=20,
        choices=Source.CLASS_CHOICES,
        default='NaN',
        blank=True, null=True,
    )
    # Status
    master_source = models.BooleanField(default=False, blank=True, null=True)
    probable_source = models.BooleanField(default=False, blank=True, null=True)

    # Legacy Surveys attributes
    ls_type = models.CharField(max_length=100, blank=True, null=True),
    ls_ra = models.FloatField(blank=True, null=True),
    ls_dec = models.FloatField(blank=True, null=True),
    ls_bx = models.FloatField(blank=True, null=True),
    ls_by = models.FloatField(blank=True, null=True),
    ls_ebv = models.FloatField(blank=True, null=True),
    ls_mjd_min = models.FloatField(blank=True, null=True),
    ls_mjd_max = models.FloatField(blank=True, null=True),
    ls_ref_cat = models.CharField(max_length=100, blank=True, null=True),
    ls_ref_id = models.FloatField(blank=True, null=True),
    ls_pmra = models.FloatField(blank=True, null=True),
    ls_pmdec = models.FloatField(blank=True, null=True),
    ls_parallax = models.FloatField(blank=True, null=True),
    ls_ref_epoch = models.FloatField(blank=True, null=True),

    # SDSS attributes
    sdss_MODE = models.FloatField(blank=True, null=True),
    sdss_CLEAN = models.FloatField(blank=True, null=True),
    sdss_ra = models.FloatField(blank=True, null=True),
    sdss_dec = models.FloatField(blank=True, null=True),
    sdss_RAERR = models.FloatField(blank=True, null=True),
    sdss_DECERR = models.FloatField(blank=True, null=True),
    sdss_cModelFlux_u = models.FloatField(blank=True, null=True),
    sdss_cModelFluxIvar_u = models.FloatField(blank=True, null=True),
    sdss_cModelFlux_g = models.FloatField(blank=True, null=True),
    sdss_cModelFluxIvar_g = models.FloatField(blank=True, null=True),

    # Pan-STARRS1 DR2 attributes
    ps_raBest = models.FloatField(blank=True, null=True),
    ps_decBest = models.FloatField(blank=True, null=True),
    ps_raStack = models.FloatField(blank=True, null=True),
    ps_decStack = models.FloatField(blank=True, null=True),
    ps_raStackErr = models.FloatField(blank=True, null=True),
    ps_decStackErr = models.FloatField(blank=True, null=True),
    ps_raMean = models.FloatField(blank=True, null=True),
    ps_decMean = models.FloatField(blank=True, null=True),
    ps_raMeanErr = models.FloatField(blank=True, null=True),
    ps_decMeanErr = models.FloatField(blank=True, null=True),
    ps_objInfoFlag = models.FloatField(blank=True, null=True),
    ps_qualityFlag = models.FloatField(blank=True, null=True),
    ps_primaryDetection = models.FloatField(blank=True, null=True),
    ps_bestDetection = models.FloatField(blank=True, null=True),
    ps_duplicat = models.CharField(max_length=100, blank=True, null=True),
    ps_d_to = models.FloatField(blank=True, null=True),
    ps_fitext = models.CharField(max_length=100, blank=True, null=True),
    ps_devaucou = models.CharField(max_length=100, blank=True, null=True),
    ps_star = models.CharField(max_length=100, blank=True, null=True),

    # GAIA attributes
    gaiaedr3_ra = models.FloatField(blank=True, null=True),
    gaiaedr3_ra_error = models.FloatField(blank=True, null=True),
    gaiaedr3_dec = models.FloatField(blank=True, null=True),
    gaiaedr3_dec_error = models.FloatField(blank=True, null=True),
    gaiaedr3_parallax = models.FloatField(blank=True, null=True),
    gaiaedr3_parallax_error = models.FloatField(blank=True, null=True),
    gaiaedr3_pm = models.FloatField(blank=True, null=True),
    gaiaedr3_pmra = models.FloatField(blank=True, null=True),
    gaiaedr3_pmra_error = models.FloatField(blank=True, null=True),
    gaiaedr3_pmdec = models.FloatField(blank=True, null=True),
    gaiaedr3_pmdec_error = models.FloatField(blank=True, null=True),

    # WISE attributes
    ls_flux_w1 = models.FloatField(blank=True, null=True),
    ls_flux_w2 = models.FloatField(blank=True, null=True),
    ls_flux_w3 = models.FloatField(blank=True, null=True),
    ls_flux_w4 = models.FloatField(blank=True, null=True),

    def __str__(self):
        return 'OptSource: {}'.format(self.name)

    def get_comment_count(self):
        return Comment.objects.filter(source=self).count()

    def get_last_comment(self):
        return Comment.objects.filter(source=self).order_by('-created_at').first()

    def __iter__(self):
        f_list = []  # TODO: how to not show fields smarter
        for field in self._meta.get_fields():
            if field.name not in f_list:
                value = getattr(self, field.name, None)
                yield (field.name, value)


class OptComment(models.Model):
    comment = models.TextField(max_length=1500)
    follow_up = models.TextField(max_length=500, blank=True, null=True)

    # TODO: Status field

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='opt_comments')
    updated_at = models.DateTimeField(blank=True, null=True)

    opt_source = models.ForeignKey(OptSource, on_delete=models.CASCADE, related_name='comments')

    def __str__(self):
        truncated_comment = Truncator(self.comment)
        return 'OptComment: {}'.format(truncated_comment.chars(10))