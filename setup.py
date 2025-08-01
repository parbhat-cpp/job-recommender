from setuptools import find_packages,setup
from typing import List

HYPEN_E_DOT = '-e .'

def get_requirements() -> List[str]:
    """
    This function will return list of requirements
    """
    requirement_list: List[str] = []
    try:
        with open('requirements.txt','r') as file:
            # read lines from file
            lines = file.readlines()
            # process each line
            for line in lines:
                requirement = line.strip()
                # ignore empty lines and -e .
                if requirement and requirement != HYPEN_E_DOT:
                    requirement_list.append(requirement)
    except Exception as e:
        print("requirements.txt not found")
    
    return requirement_list

setup(
    name='Job Recommender',
    version='0.0.1',
    author='Parbhat Sharma',
    author_email='parbhats660@gmail.com',
    packages=find_packages(),
    install_requires=get_requirements(),
)