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
Extract a CSV file for the measurement set data
"""
import csv
import glob
import os

casalog.filter('DEBUGGING')

for file_name in glob.glob('*.ms'):
    ms.open(file_name)
    data = ms.getdata(["amplitude", "axis_info", "ha", "flag"], ifraxis=True)
    ms.close()

    flags = data['flag']
    hour_angles = data['axis_info']['time_axis']['HA']
    mjd = data['axis_info']['time_axis']['MJDseconds']
    amplitudes = data['amplitude']
    baselines = data['axis_info']['ifr_axis']['ifr_shortname']
    polarisations = data['axis_info']['corr_axis']
    frequencies = data['axis_info']['freq_axis']['chan_freq']

    (head, observation_name) = os.path.split(file_name)
    elements = observation_name.split('.')
    target = elements[0]

    shape = amplitudes.shape

    with open(file_name + '.csv', 'wb') as csv_file:
        csv_writer = csv.writer(csv_file, quoting=csv.QUOTE_NONNUMERIC)
        csv_writer.writerow([
            'target',
            'polarisation',
            'MJDseconds',
            'hour angle',
            'channel',
            'frequency',
            'baseline',
            'amplitude',
            'flagged',
        ])
        for polarisation in range(0, shape[0]):
            for channel in range(0, shape[1]):
                for baseline in range(0, shape[2]):
                    for timestamp in range(0, shape[3]):
                        csv_writer.writerow([
                            target,
                            polarisations[polarisation],
                            mjd[timestamp],
                            hour_angles[timestamp],
                            channel,
                            frequencies[channel][0],
                            baselines[baseline],
                            amplitudes[polarisation][channel][baseline][timestamp],
                            flags[polarisation][channel][baseline][timestamp],
                        ])
