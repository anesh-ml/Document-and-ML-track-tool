from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.12'
DESCRIPTION = 'Ml tracking tool using jupyter extensions'
LONG_DESCRIPTION = 'A package that allows users to document their ML experiments.'

# Setting up
setup(
    name="MlTrackTool",
    version=VERSION,
    author="Anesh",
    url="https://github.com/anesh-ml/ML_tracking_tool",
    author_email="analytics955@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    package_dir={'':'.'},
    include_package_data=True,
    include_dirs=True,
    package_data={'ml_track_tool':["templates/*.html"]},
    py_modules=["plotly_","summary_plots","OpenSheet","utils","flask_app"],
    install_requires=['ipysheet', 'scikit-plot', 'lime','Shapely','plotly','flask','jinja2','psutil','xlwt','imagesize'],
    keywords=['python', 'Machine learning', 'MLops', 'ML tracking system'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)