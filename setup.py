from setuptools import setup, find_packages

setup(
    name='factor_sum',
    version='0.1',
    description='Sums positive integers that divisable by at least \
                 one number in a passed set of numbers.',
    author='Aubrey Stark-Toller',
    author_email='aubrey@deepearth.uk',
    license='MIT',
    include_package_data=True,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: GPL3 License',
        'Programming Language :: Python :: 3.4',
    ],
    keywords='project django',
    packages=find_packages(exclude=['tests*']),
    entry_points = {
        'console_scripts': [
            'factor_sum = factor_sum:main', ], }, )
