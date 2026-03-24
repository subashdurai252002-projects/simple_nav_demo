from setuptools import find_packages, setup

package_name = 'simple_nav_demo'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='subash',
    maintainer_email='subashdurai252002@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'navigator_node = simple_nav_demo.navigator_node:main',
            'mission_node = simple_nav_demo.mission_node:main',
        ],
    },
)
