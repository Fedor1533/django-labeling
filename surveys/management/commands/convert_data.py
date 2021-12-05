from django.core.management import BaseCommand
from django.utils import timezone
import pandas as pd
import pickle

# from surveys.models import *


class Command(BaseCommand):
    help = "Convert data from PKL to Parquet file."

    def add_arguments(self, parser):
        parser.add_argument("file_path", type=str, help='path for pkl file')

    @staticmethod
    def get_fields():
        fields = ['name', 'RA', 'DEC', 'ztf_name', 'comment', 'source_class', 'master_source', 'dup_id', 'L', 'B',
                  'R98', 'g_d2d', 'g_s', 'g_nsrc', 'g_gmag', 's_d2d', 's_id', 's_z', 's_otype', 'flag_agn_wise',
                  'flag_xray', 'flag_radio', 'sdss_p', 'sdss_nsrc', 'RATIO_e2e1', 'FLUX_e1', 'FLUX_e2', 'FLUX_e3',
                  'CTS_e1', 'CTS_e2', 'CTS_e3', 'EXP_e1', 'EXP_e2', 'EXP_e3', 'LIKE_e1', 'LIKE_e2', 'LIKE_e3', 'G_L_e2',
                  'G_e2', 'G_U_e2', 'Tin_L_e2', 'Tin_e2', 'Tin_U_e2', 'NH_L_e2', 'NH_e2', 'NH_U_e2', 'UPLIM_e1',
                  'UPLIM_e2', 'UPLIM_e3', 'TSTART_e1', 'TSTART_e2', 'TSTART_e3', 'TSTOP_e1', 'TSTOP_e2', 'TSTOP_e3',
                  'survey', 'file', 'row_num']
        return fields

    def handle(self, *args, **options):
        # self.stdout.write(f'Pandas version: {pd.__version__}')
        start_time = timezone.now()
        file_path = options["file_path"]
        with open(file_path, 'rb') as f:
            data = pickle.load(f)

        xray_sources = data.rename(columns={'SRCNAME': 'name', 'ZTF': 'ztf_name', 'ID': 'source_class',
                                            'notes': 'comment'
                                            })
        # TODO: change this later
        xray_sources['dup_id'] = xray_sources.index
        xray_sources['row_num'] = range(len(xray_sources.index))
        xray_sources.drop(columns=['w1', 'w2', 'w3', 'w1snr', 'w2snr', 'w3snr', 'w_nsrc',
                                   'FLUX_e4', 'CTS_e4', 'EXP_e4', 'LIKE_e4', 'UPLIM_e4',
                                   'ID_e2', 'ID_e3', 'ID_e4', 'TSTART_e4', 'TSTOP_e4', 'added'], inplace=True)
        xray_sources['survey'] = 1
        xray_sources[4:8]['survey'] = 2
        xray_sources[8:]['survey'] = 3
        xray_sources['file'] = file_path[-15:]

        # Check if all field names in dataframe - add them
        fields = Command.get_fields()
        for field in fields:
            if field not in xray_sources.columns:
                xray_sources[field] = None

        xray_sources = xray_sources[fields]
        self.stdout.write(f'New table attributes:\n{dict(xray_sources.dtypes)}')

        xray_sources.to_parquet('surveys/test_xray_data/xray_sources.parquet', engine='fastparquet')

        self.stdout.write(f'End converting pkl')
        end_time = timezone.now()
        self.stdout.write(self.style.SUCCESS(f'Converting PKL took: {(end_time - start_time).total_seconds()} seconds.'))