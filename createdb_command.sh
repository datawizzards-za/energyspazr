sudo -i -u postgres psql -c "CREATE USER energy WITH PASSWORD 'x9308PslyT@#^&';"
sudo -i -u postgres psql -c "CREATE DATABASE energyspazr OWNER energy;"
sudo -i -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE energyspazr to energy;"
# for mac 


