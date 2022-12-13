echo "Downloading Java..."
cd ~
wget https://builds.openlogic.com/downloadJDK/openlogic-openjdk/11.0.17+8/openlogic-openjdk-11.0.17+8-linux-x64.tar.gz
tar xzfv openlogic-openjdk-11.0.17+8-linux-x64.tar.gz
echo "Exporting Java Path..."
echo '' >> ~/.bashrc
echo 'export JAVA_HOME="${HOME}/openlogic-openjdk-11.0.17+8-linux-x64"' >> ~/.bashrc
echo 'export PATH="${JAVA_HOME}/bin:${PATH}"' >> ~/.bashrc

eval "$(cat ~/.bashrc | tail -n +10)" # A hack because source .bashrc doesn't work inside the script

echo "Installed Java version is..."
java --version

rm openlogic-openjdk-11.0.17+8-linux-x64.tar.gz

echo "Running sudo apt-get update..."
sudo apt-get update

echo "Installing spark..."
cd
wget https://dlcdn.apache.org/spark/spark-3.3.1/spark-3.3.1-bin-hadoop3.tgz
tar xzfv spark-3.3.1-bin-hadoop3.tgz
rm spark-3.3.1-bin-hadoop3.tgz

echo "Initiating environment variable..."
export SPARK_HOME="${HOME}/spark-3.3.1-bin-hadoop3"
export PATH="${SPARK_HOME}/bin:${PATH}"
export PYTHONPATH="${SPARK_HOME}/python/:$PYTHONPATH"
export PYTHONPATH="${SPARK_HOME}/python/lib/py4j-0.10.9.5-src.zip:$PYTHONPATH"
