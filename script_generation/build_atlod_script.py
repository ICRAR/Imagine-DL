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
Build the screen
"""
import argparse
import glob
import logging
import os

LOG = logging.getLogger(__name__)


class BuildScript(object):
    def __init__(self, input_directories, output_directory):
        self._input_directories = input_directories
        self._output_directory = output_directory

    def check_exists(self):
        for input_directory in self._input_directories:
            if not os.path.isdir(input_directory):
                LOG.error('{0} is not a valid input directory'.format(input_directory))
                return False

        if not os.path.isdir(self._output_directory):
            LOG.error('{0} is not a valid output directory'.format(self._output_directory))
            return False

        return True

    def execute(self):
        count = 0
        for input_directory in self._input_directories:
            for file_name in glob.glob(os.path.join(input_directory, '*')):
                LOG.info('{0} - {1}'.format(file_name, count))
                self._print_file(file_name, count)
                count += 1

    def _print_file(self, input_file_name, directory_counter):
        directory_name = os.path.join(self._output_directory, '{0:06d}'.format(directory_counter))
        if not os.path.exists(directory_name):
            os.makedirs(directory_name)

        file_name = os.path.join(directory_name, 'process_data.sh')
        out_file_name = os.path.join(directory_name, 'output')

        LOG.info('Creating {0}'.format(file_name))
        output_file = open(file_name, 'w')
        output_file.write('''#!/bin/bash
source /usr/local/miriad/MIRRC.sh
export PATH=$PATH:$HOME/bin:$MIRBIN

export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/gupc/lib64

atlod in={0} out={1} ifsel=1 restfreq=1.420405752 options=bary,birdie,rfiflag,noauto edge=0  
uvsplit vis={1} options=mosaic      
'''.format(input_file_name, out_file_name))


def parse_args():
    parser = argparse.ArgumentParser('Build the script to extract scans from Miriad')
    parser.add_argument('output_directory', help='the output directory')
    parser.add_argument('input_directory', nargs='+', help='the input directory')

    return parser.parse_args()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    args = parse_args()
    build_script = BuildScript(args.input_directory, args.output_directory)
    if build_script.check_exists():
        build_script.execute()
