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
import logging
import os

LOG = logging.getLogger(__name__)


class BuildScript(object):
    def __init__(self, directory):
        self._directory = directory

    def check_exists(self):
        if not os.path.isdir(self._directory):
            LOG.error('{0} is not a valid output directory'.format(self._directory))
            return False

        return True

    def execute(self):
        for directory_name in os.listdir(self._directory):
            if directory_name.isdigit():
                full_path = os.path.join(self._directory, directory_name)
                LOG.info('{0}'.format(full_path))

                casa_file = os.path.join(full_path, 'casa_script.py')
                output_file = open(os.path.join(full_path, 'casa_script.bash'), 'w')
                output_file.write('''
/usr/local/bin/casa --nologger --log2term -c {0}                
'''.format(casa_file))
                output_file.close()

                output_file = open(casa_file, 'w')

                for element in os.listdir(full_path):
                    if self._matches_calibrator(element):
                        output_file.write('''
importmiriad('{0}', '{0}.ms')
'''.format(os.path.join(full_path, element)))

                output_file.close()

    @staticmethod
    def _matches_calibrator(element):
        head, ext = os.path.splitext(element)
        elements = head.split('-')
        if len(elements) == 2:
            return elements[0].isdigit() and elements[1].isdigit()

        return False


def parse_args():
    parser = argparse.ArgumentParser('Build the script to extract scans from Miriad')
    parser.add_argument('directory', help='the root directory')

    return parser.parse_args()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    args = parse_args()
    build_script = BuildScript(args.directory)
    if build_script.check_exists():
        build_script.execute()
