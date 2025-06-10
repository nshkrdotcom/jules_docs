from setuptools import setup, find_packages
import os

# Function to read the long description from README.md
def read_readme():
    with open(os.path.join(os.path.dirname(__file__), 'README.md'), encoding='utf-8') as f:
        return f.read()

# Function to read requirements from requirements.txt
def read_requirements():
    # Path assumes setup.py is in project root, and requirements.txt is in jules_scripter directory
    # Adjust if your requirements.txt is elsewhere (e.g., project root)
    requirements_path = os.path.join(os.path.dirname(__file__), 'jules_scripter', 'requirements.txt')
    if not os.path.exists(requirements_path):
        # Fallback if requirements.txt is in the root, common for many projects
        requirements_path = os.path.join(os.path.dirname(__file__), 'requirements.txt')
        if not os.path.exists(requirements_path):
            # If no requirements.txt is found, return an empty list or default deps
            print("Warning: requirements.txt not found. Using default dependencies.")
            return ['selenium>=4.10.0', 'webdriver-manager>=4.0.0']


    with open(requirements_path, 'r') as req_file:
        return [line.strip() for line in req_file if line.strip() and not line.startswith('#')]

# Get version from jules_scripter/__init__.py
def get_version():
    version_filepath = os.path.join(os.path.dirname(__file__), 'jules_scripter', '__init__.py')
    with open(version_filepath) as f:
        for line in f:
            if line.startswith('__version__'):
                return line.strip().split()[-1].strip("'"")
    raise RuntimeError('Version not found')

VERSION = get_version()
INSTALL_REQUIRES = read_requirements()

setup(
    name='jules-scripter',
    version=VERSION,
    author='Jules AI',
    author_email='no-reply@google.com', # Placeholder
    description='A Python library for scripting web interactions, built on Selenium.',
    long_description=read_readme(),
    long_description_content_type='text/markdown',
    url='<your_project_url_here>',  # Placeholder for actual project URL if it existed
    packages=find_packages(exclude=['examples*', '*.tests', '*.tests.*', 'tests.*', 'tests']), # find jules_scripter
    include_package_data=True, # To include non-code files specified in MANIFEST.in (if any)
    install_requires=INSTALL_REQUIRES,
    classifiers=[
        'Development Status :: 3 - Alpha', # Or "4 - Beta", "5 - Production/Stable"
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Testing',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'License :: OSI Approved :: Apache Software License', # Example, choose your license
        'Operating System :: OS Independent', # Or specify (e.g., "POSIX :: Linux")
    ],
    python_requires='>=3.8',
    keywords='selenium browser automation web scripting jules',
    project_urls={ # Optional
        'Documentation': '<your_docs_url_here>',
        'Source': '<your_source_code_url_here>',
        'Tracker': '<your_issue_tracker_url_here>',
    },
    entry_points={ # If you had a CLI tool defined in run_script.py
        # 'console_scripts': [
        # 'jules-runner=jules_scripter.run_script:main_cli_function',
        # ],
    },
)
