import distutils.core
setup = distutils.core.run_setup("setup.py")
print(setup.install_requires)