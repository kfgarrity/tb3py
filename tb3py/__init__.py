"""Module to run tb3py."""

# import sys
import subprocess

# import glob
import os
import tb3py

mpath = str(tb3py.__path__[0])


def precompile(julia=None):
    """Precompile Julia."""
    print("precompile")
    if julia is None:
        julia = "julia"  # julia command
    os.system(
        julia
        + ' --eval  "using ThreeBodyTB; using Plots; ThreeBodyTB.compile()"'
    )


def install(julia=None):
    """Install Julia and TB."""
    if julia is None:
        julia = "julia"  # julia command
    print("install ", julia)

    os.system(julia + " --eval " + '"import Pkg; Pkg.add(\\"ThreeBodyTB\\")"')
    os.system(julia + " --eval " + '"import Pkg; Pkg.add(\\"PyCall\\")"')
    os.system(julia + " --eval " + '"import Pkg; Pkg.add(\\"Plots\\")"')
    os.system(julia + " --eval " + '"import Pkg; Pkg.add(\\"Suppressor\\")"')
    precompile(julia)


# mpath = os.path.dirname(os.path.realpath(__file__))


# main path
try:
    out, err = subprocess.Popen(
        ["julia", "--version"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    ).communicate()
except Exception:
    out = ""
# check if JUlia has the correct version
hasjulia = (
    ("julia version 1.6" in str(out))
    or ("julia version 1.5" in str(out))
    or ("julia version 1.7" in str(out))
    or ("julia version 1.8" in str(out))
)


# print(hasjulia) ; exit()

# print("hasjulia: ", hasjulia)
julia_cmd = os.path.join(
    mpath, "tb3py", "tjulia", "julia-1.6.1", "bin", "julia"
)  # mpath+"/src/julia/julia-1.6.1/bin/julia" # path for julia
if not hasjulia:  # if the correct Julia version is not present
    # julia_cmd = mpath+"/src/julia/julia-1.6.1/bin/julia" # path for julia
    if not os.path.exists(julia_cmd):
        print("Julia not present in path:", mpath, "...downloading...")
        subfolder = os.path.join(mpath, "tb3py", "tjulia")
        if not os.path.exists(subfolder):
            os.makedirs(subfolder)
        os.chdir(subfolder)  # go to the subfolder
        juliafile = os.path.join(
            mpath, "julia-1.6.1-linux-x86_64.tar.gz"
        )  # julia file
        j_link = (
            "https://julialang-s3.julialang.org/bin/linux/x64/1.6/"
            + "julia-1.6.1-linux-x86_64.tar.gz"
        )
        # print("jlink", j_link)
        import requests
        import tarfile

        r_julia = requests.get(j_link, stream=True).content
        with open(juliafile, "wb") as jfile:
            jfile.write(r_julia)
        # print("juliafile", juliafile)
        try:
            my_tar = tarfile.open(juliafile)
            my_tar.extractall()
            my_tar.close()
        except Exception as exp:
            print(exp)
            cmd = "tar -xvzf " + juliafile
            os.system(cmd)
        os.remove(juliafile)
    else:
        print("We already downloaded to ", julia_cmd)

    # julia_cmd = mpath+"/src/julia/julia-1.6.1/bin/julia" # path for julia
    os.chdir(mpath)  # go back

else:
    julia_cmd = "julia"
    print("Correct Julia version found in path")


print("My julia command : ", julia_cmd)

# install python dependences
# os.system("python3 -m pip install --user julia")

# using julia
# import julia
# julia.install()


# os.system("pip install pmdarima")


# install
sysimage = os.path.join(
    os.environ["HOME"], ".julia", "sysimages", "sys_threebodytb.so"
)
# print("sysimage", sysimage)
# install(julia_cmd)  # install Julia dependences
if not os.path.isfile(sysimage):
    # import TB3.juliarun as juliarun
    install(julia_cmd)  # install Julia dependences
julia_bin = os.path.join(
    mpath, "tb3py", "tjulia", "julia-1.6.1", "bin"
)  # mpath+"/src/julia/julia-1.6.1/bin/julia" # path for julia
os.environ["PATH"] += os.pathsep + os.path.join(julia_bin)
# print('pathhhhhh',os.environ["PATH"])
# os.system('julia')
try:
    out, err = subprocess.Popen(
        ["julia", "--version"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    ).communicate()
except Exception as exp:
    print("check", exp)
    out = ""
# check if JUlia has the correct version
hasjulia = (
    ("julia version 1.6" in str(out))
    or ("julia version 1.5" in str(out))
    or ("julia version 1.7" in str(out))
    or ("julia version 1.8" in str(out))
)
# print("hasjulia init final", hasjulia)

# """
# cmd='python -m pip install julia'
# os.system(cmd)
# print('pathhhhhh',os.environ["PATH"])

import julia
from julia.api import Julia
julia.install()

# print("julia_cmd in main.py", julia_cmd)
jlsession = Julia(runtime=julia_cmd, compiled_modules=False, sysimage=sysimage)
jlsession.eval("using Suppressor")  # suppress output
# """
