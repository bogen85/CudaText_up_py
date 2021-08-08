# CudaText_up_py

[See CudaText_up issue # 11](https://github.com/Alexey-T/CudaText_up/issues/11)

Python flavor of [See CudaText_up](https://github.com/Alexey-T/CudaText_up)

It seems to work on FreeBSD and Linux, but I'm sure I have permissions and other issues to work out, plus I've not exercised the "install packages to Lazarus" as I've not make my own custom Lazarus directory.

As such, I would consider this work in progress as I work out any issues.

For now see ```./cudaup.sh --help``` (and the source code) until I get it more fully documented.

Python to use is automatic, ./cudaup.sh finds a compatible one and uses it (but one can be specified).

One does not need to be in the CudaText_up_py directory to run the script, one can provide the complete path to the script (the other files/folders it comes with must reside with the the script.) I don't have it working if it is in PATH yet, but I will add the ability to run it from anywhere if it is the PATH.

By default the working directory (where src is created/used) is the current directory, but a different one can be specified.
