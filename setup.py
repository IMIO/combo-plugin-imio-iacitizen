from setuptools import find_packages, setup

version = "0.1.0"

setup(
    name="combo-plugin-imio-iacitizen",
    version=version,
    author="iMio",
    author_email="support-ts@imio.be",
    description="iA.Citizen : choix des catégories du tableau de bord dans une cellule unique",
    packages=find_packages(),
    include_package_data=True,
    data_files=[("/etc/combo/settings.d", ["settings.d/50combo_plugin_imio_iacitizen.py"])],
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Django",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ],
    url="https://github.com/IMIO/combo-plugin-imio-iacitizen",
    install_requires=[
        "django>=4.2",
    ],
    zip_safe=False,
)
