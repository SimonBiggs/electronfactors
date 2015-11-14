from setuptools import setup

setup(
    name = "electronfactors",
    version = "0.1.3",
    author = "Simon Biggs",
    author_email = "mail@simonbiggs.net",
    description = "Predict electron insert factors",
    long_description = """Predict electron insert factors to an uncertainty approaching measurement using the measurements you have already taken.

You can start on a given energy/applicator/SSD combination if you have at least eight data points.

For more information visit the gihub repository, https://github.com/SimonBiggs/electronfactors
    
This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more details.""",
    keywords = [],
    packages = ["electronfactors"],
    license='AGPL3+',
    classifiers = [],
    url = "https://github.com/SimonBiggs/electronfactors"
)
