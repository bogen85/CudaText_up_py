#  ls ${HOME}/.config/cudatext/
#  rm -rf ${HOME}/.config/cudatext/*
  rsync -a ./build/src/CudaText/app/data/   ${HOME}/.config/cudatext/data/
  rsync -a ./build/src/CudaText/app/py/   ${HOME}/.config/cudatext/py/
  rsync -a ./build/src/CudaText/app/settings_default/   ${HOME}/.config/cudatext/settings_default/
  mkdir -pv ${HOME}/.config/cudatext/settings
  # cp ./build/src/bin/linux-x86_64-gtk3/cudatext ~/bin/

