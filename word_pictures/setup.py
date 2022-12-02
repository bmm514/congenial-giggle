import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(name='word_pictures',
    version='0.0.1',
    author='Ben Murcott',
    author_email='benmurcott96@gmail.com',
    description='Make pictures from strings',
    long_description = long_description,
    long_description_content_type = "text/markdown",
    #url='https://github.com/bmm514/stepRNA.git',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: Unix"
    ],
    #license='MIT',
    #keywords=['Dicer', 'RNA', 'genomics', 'processing', 'sRNA', 'miRNA'],
    packages=["word_pictures"],
    python_requires=">=3.8.10",
    install_requires=[
        "matplotlib>=3.6.2",
        "numpy>=1.23.4",
        "Pillow>=9.3.0"
        ]
#    scripts=["bin/stepRNA",
#    "stepRNA/stepRNA_run_bowtie.py",
#    "stepRNA/stepRNA_cigar_process.py"
#    ]
)

