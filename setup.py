from setuptools import setup, find_packages

setup(
    name='factor_sum',
    version='1.1',
    description='Sums positive integers that are both less than a user \
                 defined maximum and divisable by at least one number in a \
                 user defined set of numbers.',
    author='Aubrey Stark-Toller',
    author_email='aubrey@deepearth.uk',
    license='GPL3',
    include_package_data=True,
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 2.7',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',

    ],
    keywords='project django',
    packages=find_packages(exclude=['tests*']),
    entry_points = {
        'console_scripts': [
            'factor_sum = factor_sum:main', ], }, )
