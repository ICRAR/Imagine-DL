#
#    ICRAR - International Centre for Radio Astronomy Research
#    (c) UWA - The University of Western Australia
#    Copyright by UWA (in the framework of the ICRAR)
#    All rights reserved
#
#    This library is free software; you can redistribute it and/or
#    modify it under the terms of the GNU Lesser General Public
#    License as published by the Free Software Foundation; either
#    version 2.1 of the License, or (at your option) any later version.
#
#    This library is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#    Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public
#    License along with this library; if not, write to the Free Software
#    Foundation, Inc., 59 Temple Place, Suite 330, Boston,
#    MA 02111-1307  USA
#
"""
Create the CSV file
"""

import argparse
import csv
import logging
import os

casalog.filter('DEBUGGING')
logging.info('Starting logger for...')
LOG = logging.getLogger("create_csv_file")


class CreateCsv(object):
    def __init__(self, directory_to_scan, csv_filename):
        self.directory_to_scan = directory_to_scan
        self._csv_filename = csv_filename
        self._csv_writer = None
        self._spectral_window_info = None
        self._observer = None

    def _extract_data(self, measurement_set):
        # Open the measurement set
        ms.open(measurement_set)
        self._spectral_window_info = ms.getspectralwindowinfo()

        scan_summary = ms.getscansummary()

        data = ms.getdata(["axis_info","ha"], ifraxis=True)
        ms.close()

        (head, observation_name) = os.path.split(measurement_set)
        elements = observation_name.split('.')
        target = elements[0]

        for scan_number in scan_summary.keys():
            begin_time = scan_summary[scan_number]['0']['BeginTime']
            end_time = scan_summary[scan_number]['0']['EndTime']

            hour_angle_begin_time = self._get_hour_angle(begin_time, data)
            hour_angle_end_time = self._get_hour_angle(end_time, data)

            for spectral_window_number in self._spectral_window_info.keys():
                number_channels = self._spectral_window_info[spectral_window_number]['NumChan']
                for channel_number in range(0, number_channels):
                    vis_stats = visstat(
                        vis=measurement_set,
                        datacolumn='data',
                        scan=scan_number,
                        spw='{0}:{1}'.format(spectral_window_number, channel_number),
                        useflags=False,
                    )
                    if vis_stats is not None:
                        frequency = self._get_frequency(spectral_window_number, channel_number)
                        self._write_line(
                            target,
                            scan_number,
                            begin_time,
                            end_time,
                            hour_angle_begin_time,
                            hour_angle_end_time,
                            spectral_window_number,
                            channel_number,
                            frequency,
                            vis_stats
                        )

    def _write_line(self, observation_id, scan_number, begin_time, end_time, hour_angle_begin_time, hour_angle_end_time, spectral_window_number, channel_number, frequency, vis_stats):
        result = vis_stats[vis_stats.keys()[0]]
        self._csv_writer.writerow([
            observation_id,
            scan_number,
            begin_time,
            end_time,
            hour_angle_begin_time,
            hour_angle_end_time,
            spectral_window_number,
            channel_number,
            frequency,
            '{0:.5f}'.format(result['max']),
            '{0:.5f}'.format(result['mean']),
            '{0:.5f}'.format(result['medabsdevmed']),
            '{0:.5f}'.format(result['median']),
            '{0:.5f}'.format(result['min']),
            '{0:.5f}'.format(result['npts']),
            '{0:.5f}'.format(result['quartile']),
            '{0:.5f}'.format(result['rms']),
            '{0:.5f}'.format(result['stddev']),
            '{0:.5f}'.format(result['sum']),
            '{0:.5f}'.format(result['sumsq']),
            '{0:.5f}'.format(result['var']),
        ])

    def _get_frequency(self, spectral_window_number, channel_number):
        spectral_window = self._spectral_window_info[spectral_window_number]
        frequency = spectral_window['Chan1Freq']
        width = spectral_window['ChanWidth']

        return frequency + channel_number * width

    def extract_statistics(self):
        list_measurement_sets = self._find_measurement_sets(self.directory_to_scan)
        LOG.info('Measurement Sets: {0}'.format(list_measurement_sets))

        # Open the CSV file
        with open(self._csv_filename, 'wb') as csv_file:
            self._csv_writer = csv.writer(csv_file, quoting=csv.QUOTE_MINIMAL)
            self._csv_writer.writerow([
                'target',
                'scan',
                'begin_time',
                'end_time',
                'begin_hour_angle',
                'end_hour_angle',
                'spectral_window',
                'channel',
                'frequency',
                'max',
                'mean',
                'medabsdevmed',
                'median',
                'min',
                'npts',
                'quartile',
                'rms',
                'stddev',
                'sum',
                'sumsq',
                'var',
            ])

            for measurement_set in list_measurement_sets:
                self._extract_data(measurement_set)

    def _find_measurement_sets(self, directory_to_scan):
        list_measurement_sets = []
        for entry in os.listdir(directory_to_scan):
            full_pathname = os.path.join(directory_to_scan, entry)
            if entry.endswith('.ms'):
                list_measurement_sets.append(full_pathname)
            elif os.path.isdir(full_pathname):
                list_measurement_sets.extend(self._find_measurement_sets(full_pathname))

        return list_measurement_sets

    @staticmethod
    def _get_hour_angle(time, data):
        hour_angles = data['axis_info']['time_axis']['HA']
        mj_dates = data['axis_info']['time_axis']['MJDseconds']
        time_in_seconds = time * 3600 * 24
        count = 0
        for mjd in mj_dates:
            if time_in_seconds <= mjd:
                return hour_angles[count]
            count += 1

        return hour_angles[-1]


def parse_args():
    """
    This is called via Casa so we have to be a bit careful
    :return:
    """
    parser = argparse.ArgumentParser('Get the arguments')
    parser.add_argument('arguments', nargs='+', help='the arguments')

    parser.add_argument('--nologger', action="store_true")
    parser.add_argument('--log2term', action="store_true")
    parser.add_argument('--logfile')
    parser.add_argument('-c', '--call')

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    create_csv = CreateCsv(args.arguments[0], args.arguments[1])
    create_csv.extract_statistics()
