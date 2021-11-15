import setuptools

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

with open('/home/cmts/Documents/misc/timerdo/requirements.txt', 'r',
          encoding='utf-8') as fo:
    requires = fo.read()

setuptools.setup(
    name='timerdo',
    version='0.0.1',
    author='Caio Mescouto',
    author_email='caiomescouto@gmail.com',
    description='A minimalist to-do list with a built-in timer',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/caiomts/timerdo',
    project_urls={
        'Bug Tracker': 'https://github.com/caiomts/timerdo/issues',
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=requires,
    python_requires='>=3.9',
    entry_points={
        'console_scripts': [
            'timerdo = timerdo.main:app'
        ]
    },
)

