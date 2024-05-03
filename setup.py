from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'can_transceiver_2'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob(os.path.join('launch', '*launch.[pxy][yma]*'))),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Andrei Smirnov',
    maintainer_email='andrey040902@gmail.com',
    description='ROS-CAN transceiver for EUREKA rover',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
                'can_transceiver = can_transceiver_2.can_transceiver:main',
        ],
    },
)
