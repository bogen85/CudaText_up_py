#  ls ${HOME}/.config/cudatext/
#  rm -rf ${HOME}/.config/cudatext/*

set -xeuo pipefail

mkdir -pv ~/opt/CudaText

dest=~/opt/CudaText/03

rm -rf ${dest}
mkdir -pv ${dest}
  
rsync -a ./build/src/CudaText/app/data/   ${dest}/data/
rsync -a ./build/src/CudaText/app/py/   ${dest}/py/
rsync -a ./build/src/CudaText/app/settings_default/   ${dest}/settings_default/
cp -av ./build/src/CudaText/app/cudatext ${dest}/

rm -vf ~/bin/cudatext

ln -vs ${dest}/cudatext ~/bin/cudatext
ln -vs ${HOME}/.config/cudatext/settings ${dest}/settings

  # cp ./build/src/bin/linux-x86_64-gtk3/cudatext ~/bin/

