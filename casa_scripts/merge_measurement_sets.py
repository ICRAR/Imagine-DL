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
Merge files
"""
import glob

import logging

casalog.filter('DEBUGGING')
logging.info('Starting logger for...')
LOG = logging.getLogger('merge_measurement_sets')

list_measurement_sets = []
for file_name in glob.glob('/scratch/kevin/imagine/*/*.ms'):
    list_measurement_sets.append(file_name)
    LOG.info('Adding {0}'.format(file_name))

LOG.info('List = {0}'.format(list_measurement_sets))
concat(list_measurement_sets, '/scratch/kevin/imagine/final.ms', timesort=True, copypointing=True)
