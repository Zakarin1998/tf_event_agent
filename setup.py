from setuptools import setup, find_packages

descr = "Agente AI per analizzare una pagina web Eventbrite, oppure elaborare un file event.html con scraping, parsing."
author_name = "Alessandro Brillante"

setup(
    name="eventbrite-agent",
    version="0.1.0",
    packages=find_packages(where="."),
    install_requires=[
        # HTTP & Parsing
        "requests>=2.32.4",
        "beautifulsoup4>=4.13.4",
        "lxml>=5.4.0",
        # Graph Analytics and Data manipulation
        "pandas>=1.2.0",
        "networkx>=3.2.1",
        # (Opzionali) YAML config, storage e .env
        "python-dotenv>=1.1.0",
        "PyYAML>=6.0.2",
    ],
    entry_points={
        "console_scripts": [
            "pom-agent-cli=cli:main",
            "pom-agent=run_agent:run_pom_agent"
        ]
    },
    author=author_name,
    description=descr,
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License"
    ],
    python_requires='>=3.9,<3.10',
)
