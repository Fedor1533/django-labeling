from django.db import models
from django.utils.text import Truncator
from django.contrib.auth.models import User
from itertools import zip_longest
from django.db.models import Max

import numpy as np


# Class for files from where the xray sources were loaded
class MetaSource(models.Model):
    file_name = models.CharField(max_length=200)
    version = models.PositiveIntegerField(default=1, blank=True, null=True)
    description = models.TextField(max_length=500, blank=True, null=True)  # Maybe dont need it

    def __str__(self):
        return 'MetaSource: {}'.format(self.file_name)


# Class for sources that are considered one space object
class MetaObject(models.Model):
    master_name = models.CharField(max_length=200)
    unchange_flag = models.BooleanField(default=False, blank=True, null=True)
    description = models.TextField(max_length=500, blank=True, null=True)  # Maybe dont need it

    # for master optical sources from different surveys
    ls_source = models.ForeignKey('LS', on_delete=models.CASCADE, related_name='meta_objects', blank=True, null=True)
    gaia_source = models.ForeignKey('GAIA', on_delete=models.CASCADE, related_name='meta_objects', blank=True, null=True)
    ps_source = models.ForeignKey('PS1', on_delete=models.CASCADE, related_name='meta_objects', blank=True, null=True)

    def __str__(self):
        return 'MetaObject: {}'.format(self.master_name)


# Class for surveys where transients were detected
class Survey(models.Model):
    name = models.PositiveIntegerField(unique=True)
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(blank=True, null=True)
    description = models.TextField(max_length=500, blank=True, null=True)

    def __str__(self):
        return 'Survey {}'.format(self.name)

    @staticmethod
    def get_fields_to_show():
        fields = ['name', 'RA', 'DEC', 'ztf_name', 'comment', 'source_class', 'L', 'B', 'R98', 'FLAG', 'qual',
                  'g_d2d', 'g_s', 'g_id', 's_d2d', 's_id', 's_z', 's_otype', 's_nsrc', 'checked', 'flag_xray',
                  'flag_radio', 'flag_agn_wise', 'w1', 'w2', 'w3', 'w1snr', 'w2snr', 'w3snr', 'g_nsrc', 'sdss_nsrc',
                  'sdss_p', 'sdss_id', 'sdss_sp', 'sdss_d2d', 'added', '_15R98', 'g_gmag', 'g_maxLx', 'w_nsrc', 'R98c',
                  'z', 'CTS_e1', 'CTS_e2', 'CTS_e3', 'CTS_e4', 'CTS_e123', 'D2D_e1', 'D2D_e3e2', 'D2D_e4', 'D2D_e123',
                  'EXP_e1', 'EXP_e12', 'EXP_e2', 'EXP_e3', 'EXP_e4', 'EXP_e123',
                  'FLUX_e1', 'FLUX_e2', 'FLUX_e3', 'FLUX_e4', 'FLUX_e123',
                  'G_L_e1', 'G_L_e2', 'G_L_e3', 'G_U_e1', 'G_U_e2', 'G_U_e3', 'G_e1','G_e2', 'G_e3',
                  'ID_e1', 'ID_e2', 'ID_e3', 'ID_e4', 'ID_e123',
                  'LIKE_e1','LIKE_e12', 'LIKE_e2', 'LIKE_e3', 'LIKE_e4', 'LIKE_e123',
                  'NH_L_e1', 'NH_L_e2', 'NH_L_e3', 'NH_U_e1', 'NH_U_e2', 'NH_U_e3', 'NH_e1', 'NH_e2', 'NH_e3',
                  'RADEC_ERR_e1', 'RADEC_ERR_e12', 'RADEC_ERR_e2', 'RADEC_ERR_e3', 'RADEC_ERR_e4', 'RADEC_ERR_e123',
                  'Tin_L_e1', 'Tin_L_e2', 'Tin_L_e3', 'Tin_U_e1', 'Tin_U_e2', 'Tin_U_e3', 'Tin_e1','Tin_e2', 'Tin_e3',
                  'UPLIM_e1', 'UPLIM_e2', 'UPLIM_e3', 'UPLIM_e4', 'UPLIM_e12', 'UPLIM_e123',
                  'RATIO_e3e2', 'TSTART_e1', 'TSTART_e2', 'TSTART_e3', 'TSTART_e4',
                  'TSTOP_e1', 'TSTOP_e2', 'TSTOP_e3', 'TSTOP_e4', 'g_b', 'ps_p']
        return fields

    def get_sources_count(self):
        return Source.objects.filter(survey=self).count()


# Class for xray sources from all surveys
class Source(models.Model):
    name = models.CharField(max_length=150)

    RA = models.FloatField()
    DEC = models.FloatField()

    ztf_name = models.CharField(max_length=100, blank=True, null=True)
    comment = models.TextField(max_length=2000, blank=True, null=True)

    CLASS_CHOICES = [
        ('TDE', 'TDE Source'),
        ('NOT TDE', 'Not TDE Source'),
        ('NaN', 'Unknown Source'),
    ]
    source_class = models.CharField(
        max_length=100,
        choices=CLASS_CHOICES,
        default='NaN',
        blank=True, null=True,
    )

    master_source = models.BooleanField(default=True, blank=True, null=True)
    # dup_id = models.PositiveIntegerField(blank=True, null=True)

    # TODO: Think about formats and view of fields
    L = models.FloatField(blank=True, null=True)
    B = models.FloatField(blank=True, null=True)
    R98 = models.FloatField(blank=True, null=True)
    FLAG = models.IntegerField(blank=True, null=True)
    qual = models.IntegerField(blank=True, null=True)

    g_d2d = models.FloatField(blank=True, null=True)
    g_s = models.IntegerField(blank=True, null=True)
    g_id = models.BigIntegerField(blank=True, null=True)

    s_d2d = models.FloatField(blank=True, null=True)
    s_id = models.CharField(max_length=100, blank=True, null=True)
    s_z = models.FloatField(blank=True, null=True)
    s_otype = models.CharField(max_length=100, blank=True, null=True)
    s_nsrc = models.IntegerField(blank=True, null=True)
    checked = models.IntegerField(blank=True, null=True)

    flag_xray = models.IntegerField(blank=True, null=True)
    flag_radio = models.IntegerField(blank=True, null=True)
    flag_agn_wise = models.IntegerField(blank=True, null=True)

    # w1,2,3
    w1 = models.FloatField(blank=True, null=True)
    w2 = models.FloatField(blank=True, null=True)
    w3 = models.FloatField(blank=True, null=True)
    # w1snr,2,3
    w1snr = models.FloatField(blank=True, null=True)
    w2snr = models.FloatField(blank=True, null=True)
    w3snr = models.FloatField(blank=True, null=True)

    g_nsrc = models.IntegerField(blank=True, null=True)
    sdss_nsrc = models.IntegerField(blank=True, null=True)
    sdss_p = models.IntegerField(blank=True, null=True)
    sdss_id = models.BigIntegerField(blank=True, null=True)
    sdss_sp = models.BigIntegerField(blank=True, null=True)
    sdss_d2d = models.FloatField(blank=True, null=True)
    added = models.CharField(max_length=100, blank=True, null=True)

    _15R98 = models.FloatField(blank=True, null=True)
    g_gmag = models.FloatField(blank=True, null=True)
    g_maxLx = models.FloatField(blank=True, null=True)
    w_nsrc = models.IntegerField(blank=True, null=True)
    R98c = models.FloatField(blank=True, null=True)
    z = models.FloatField(blank=True, null=True)

    # CTS_e1,2,3,4
    CTS_e1 = models.FloatField(blank=True, null=True)
    CTS_e2 = models.FloatField(blank=True, null=True)
    CTS_e3 = models.FloatField(blank=True, null=True)
    CTS_e4 = models.FloatField(blank=True, null=True)
    CTS_e123 = models.FloatField(blank=True, null=True)

    D2D_e1 = models.FloatField(blank=True, null=True)
    D2D_e3e2 = models.FloatField(blank=True, null=True)
    D2D_e4 = models.FloatField(blank=True, null=True)
    D2D_e123 = models.FloatField(blank=True, null=True)

    # EXP_e1,2,3,4
    EXP_e1 = models.FloatField(blank=True, null=True)
    EXP_e2 = models.FloatField(blank=True, null=True)
    EXP_e3 = models.FloatField(blank=True, null=True)
    EXP_e4 = models.FloatField(blank=True, null=True)
    EXP_e12 = models.FloatField(blank=True, null=True)
    EXP_e123 = models.FloatField(blank=True, null=True)

    # FLUX_e1,2,3,4
    FLUX_e1 = models.FloatField(blank=True, null=True)
    FLUX_e2 = models.FloatField(blank=True, null=True)
    FLUX_e3 = models.FloatField(blank=True, null=True)
    FLUX_e4 = models.FloatField(blank=True, null=True)
    FLUX_e123 = models.FloatField(blank=True, null=True)

    # LIKE_e1,2,3,4
    LIKE_e1 = models.FloatField(blank=True, null=True)
    LIKE_e2 = models.FloatField(blank=True, null=True)
    LIKE_e3 = models.FloatField(blank=True, null=True)
    LIKE_e4 = models.FloatField(blank=True, null=True)
    LIKE_e12 = models.FloatField(blank=True, null=True)
    LIKE_e123 = models.FloatField(blank=True, null=True)

    # G_L_e1,2,3
    G_L_e1 = models.FloatField(blank=True, null=True)
    G_L_e2 = models.FloatField(blank=True, null=True)
    G_L_e3 = models.FloatField(blank=True, null=True)
    # G_U_e1,2,3
    G_U_e1 = models.FloatField(blank=True, null=True)
    G_U_e2 = models.FloatField(blank=True, null=True)
    G_U_e3 = models.FloatField(blank=True, null=True)
    # G_e1,2,3
    G_e1 = models.FloatField(blank=True, null=True)
    G_e2 = models.FloatField(blank=True, null=True)
    G_e3 = models.FloatField(blank=True, null=True)

    # ID_e1,2,3,4
    ID_e1 = models.BigIntegerField(blank=True, null=True)
    ID_e2 = models.BigIntegerField(blank=True, null=True)
    ID_e3 = models.BigIntegerField(blank=True, null=True)
    ID_e4 = models.BigIntegerField(blank=True, null=True)
    ID_e123 = models.BigIntegerField(blank=True, null=True)

    # NH_L_e1,2,3
    NH_L_e1 = models.FloatField(blank=True, null=True)
    NH_L_e2 = models.FloatField(blank=True, null=True)
    NH_L_e3 = models.FloatField(blank=True, null=True)
    # NH_U_e1,2,3
    NH_U_e1 = models.FloatField(blank=True, null=True)
    NH_U_e2 = models.FloatField(blank=True, null=True)
    NH_U_e3 = models.FloatField(blank=True, null=True)
    # N_e1,2,3
    NH_e1 = models.FloatField(blank=True, null=True)
    NH_e2 = models.FloatField(blank=True, null=True)
    NH_e3 = models.FloatField(blank=True, null=True)

    #RADEC_ERR_e1,2,3,4
    RADEC_ERR_e1 = models.FloatField(blank=True, null=True)
    RADEC_ERR_e2 = models.FloatField(blank=True, null=True)
    RADEC_ERR_e3 = models.FloatField(blank=True, null=True)
    RADEC_ERR_e4 = models.FloatField(blank=True, null=True)
    RADEC_ERR_e12 = models.FloatField(blank=True, null=True)
    RADEC_ERR_e123 = models.FloatField(blank=True, null=True)

    RATIO_e3e2 = models.FloatField(blank=True, null=True)

    # Tin_L_e1,2,3
    Tin_L_e1 = models.FloatField(blank=True, null=True)
    Tin_L_e2 = models.FloatField(blank=True, null=True)
    Tin_L_e3 = models.FloatField(blank=True, null=True)
    # Tin_U_e1,2,3
    Tin_U_e1 = models.FloatField(blank=True, null=True)
    Tin_U_e2 = models.FloatField(blank=True, null=True)
    Tin_U_e3 = models.FloatField(blank=True, null=True)
    # Tin_e1,2,3
    Tin_e1 = models.FloatField(blank=True, null=True)
    Tin_e2 = models.FloatField(blank=True, null=True)
    Tin_e3 = models.FloatField(blank=True, null=True)

    # UPLIM_e1,2,3,4
    UPLIM_e1 = models.FloatField(blank=True, null=True)
    UPLIM_e2 = models.FloatField(blank=True, null=True)
    UPLIM_e3 = models.FloatField(blank=True, null=True)
    UPLIM_e4 = models.FloatField(blank=True, null=True)
    UPLIM_e12 = models.FloatField(blank=True, null=True)
    UPLIM_e123 = models.FloatField(blank=True, null=True)

    # TSTART_e1,2,3,4
    TSTART_e1 = models.CharField(max_length=100, blank=True, null=True)
    TSTART_e2 = models.CharField(max_length=100, blank=True, null=True)
    TSTART_e3 = models.CharField(max_length=100, blank=True, null=True)
    TSTART_e4 = models.CharField(max_length=100, blank=True, null=True)
    # TSTOP_e1,2,3,4
    TSTOP_e1 = models.CharField(max_length=100, blank=True, null=True)
    TSTOP_e2 = models.CharField(max_length=100, blank=True, null=True)
    TSTOP_e3 = models.CharField(max_length=100, blank=True, null=True)
    TSTOP_e4 = models.CharField(max_length=100, blank=True, null=True)

    g_b = models.IntegerField(blank=True, null=True)
    ps_p = models.IntegerField(blank=True, null=True)
    # END

    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name='sources')

    # For ability to rebuild lost Data: expert's comments on sources
    meta_data = models.ForeignKey(MetaSource, on_delete=models.CASCADE, related_name='file_sources', blank=True, null=True)
    row_num = models.PositiveIntegerField()  # row number in load file
    # to find sources that are considered one space object
    meta_object = models.ForeignKey(MetaObject, on_delete=models.CASCADE, related_name='object_sources', blank=True, null=True)

    def __str__(self):
        return 'Source: {}'.format(self.name)

    def get_comment_count(self):
        return Comment.objects.filter(source=self).count()

    def get_last_comment(self):
        return Comment.objects.filter(source=self).order_by('-created_at').first()

    def get_opt_survey_sources(self, survey_name):
        if survey_name == 'LS':
            opt_sources = self.ls_sources.all()
            return opt_sources if opt_sources.exists() else None

        elif survey_name == 'GAIA':
            opt_sources = self.gaia_sources.all()
            return opt_sources if opt_sources.exists() else None

        if survey_name == 'PS1':
            opt_sources = self.ps1_sources.all()
            return opt_sources if opt_sources.exists() else None

    def __iter__(self):
        for field in Survey.get_fields_to_show():
            value = getattr(self, field, None)
            yield field, value


# Class for comments on xray sources
class Comment(models.Model):
    comment = models.TextField(max_length=2000)
    follow_up = models.TextField(max_length=1000, blank=True, null=True)

    source_class = models.CharField(
        max_length=100,
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


# TODO: full models for Optical Surveys
# Models for DESI Legacy Imaging Surveys sources
class LS(models.Model):
    opt_id = models.PositiveIntegerField()
    name = models.CharField(max_length=150)

    RA = models.FloatField()
    DEC = models.FloatField()

    source_class = models.CharField(
        max_length=100,
        choices=Source.CLASS_CHOICES,
        default='NaN',
        blank=True, null=True,
    )

    xray_source = models.ForeignKey(Source, on_delete=models.CASCADE, related_name='ls_sources')
    # Status
    master_source = models.BooleanField(default=False, blank=True, null=True)
    probable_source = models.BooleanField(default=True, blank=True, null=True)

    # for master optical sources, xray_source must be linked with meta_object
    # meta_object = models.ForeignKey(MetaObject, on_delete=models.CASCADE, related_name='ls_sources', blank=True, null=True)

    def __str__(self):
        return 'LS: {}'.format(self.name)

    def __iter__(self):
        for field in LS._meta.get_fields():
            value = getattr(self, field.name, None)
            yield field.name, value

    class Meta:
        verbose_name_plural = "Legacy Surveys"


# Models for GAIA sources
class GAIA(models.Model):
    opt_id = models.PositiveIntegerField()
    name = models.CharField(max_length=150)

    RA = models.FloatField()
    DEC = models.FloatField()

    source_class = models.CharField(
        max_length=100,
        choices=Source.CLASS_CHOICES,
        default='NaN',
        blank=True, null=True,
    )

    xray_source = models.ForeignKey(Source, on_delete=models.CASCADE, related_name='gaia_sources')
    # Status
    master_source = models.BooleanField(default=False, blank=True, null=True)
    probable_source = models.BooleanField(default=True, blank=True, null=True)

    # for master optical sources, xray_source must be linked with meta_object
    # meta_object = models.ForeignKey(MetaObject, on_delete=models.CASCADE, related_name='gaia_sources', blank=True, null=True)

    def __str__(self):
        return 'GAIA: {}'.format(self.name)

    def __iter__(self):
        for field in GAIA._meta.get_fields():
            value = getattr(self, field.name, None)
            yield field.name, value

    class Meta:
        verbose_name_plural = "GAIA"


# Models for Pan-STARRS1 DR2 sources
class PS1(models.Model):
    opt_id = models.PositiveIntegerField()
    name = models.CharField(max_length=150)

    RA = models.FloatField()
    DEC = models.FloatField()

    source_class = models.CharField(
        max_length=100,
        choices=Source.CLASS_CHOICES,
        default='NaN',
        blank=True, null=True,
    )

    xray_source = models.ForeignKey(Source, on_delete=models.CASCADE, related_name='ps1_sources')
    # Status
    master_source = models.BooleanField(default=False, blank=True, null=True)
    probable_source = models.BooleanField(default=True, blank=True, null=True)

    # for master optical sources, xray_source must be linked with meta_object
    # meta_object = models.ForeignKey(MetaObject, on_delete=models.CASCADE, related_name='ps1_sources', blank=True, null=True)

    def __str__(self):
        return 'PS1: {}'.format(self.name)

    def __iter__(self):
        for field in PS1._meta.get_fields():
            value = getattr(self, field.name, None)
            yield field.name, value

    class Meta:
        verbose_name_plural = "Pan-STARRS1"


# Class for comments on optical sources
class OptComment(models.Model):
    comment = models.TextField(max_length=1500)

    # TODO: master opt sources
    master_ls = models.CharField(max_length=150, blank=True, null=True)
    master_gaia = models.CharField(max_length=150, blank=True, null=True)
    master_ps = models.CharField(max_length=150, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='opt_comments')
    updated_at = models.DateTimeField(blank=True, null=True)

    source = models.ForeignKey(Source, on_delete=models.CASCADE, related_name='opt_comments')

    def __str__(self):
        truncated_comment = Truncator(self.comment)
        return 'OptComment: {}'.format(truncated_comment.chars(10))
