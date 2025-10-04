from setuptools import setup, find_packages

# Read requirements from the requirements.txt file
with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name="ai-terminal",
    version="1.0.0",
    author="Your Name",
    description="An AI-powered hybrid terminal that communicates with an MCP server.",
    packages=find_packages(),
    install_requires=required,
    entry_points={
        'console_scripts': [
            'ai-terminal = ai_terminal.client:main',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
