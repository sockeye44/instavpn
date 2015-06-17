[ -d instavpn ] && rm -rf instavpn/
echo "Installing git"
if [[ ! -z $(which apt-get) ]]; then
    apt-get install -y git > /dev/null
    echo "Ok"
else
    echo "You must use Ubuntu"
    exit 1
fi
echo "Cloning git repo"
git clone https://github.com/sockeye44/instavpn.git --quiet || exit 1
echo "Ok"
cd instavpn
sudo python install.py
