#for Mac
psql postgres -c "CREATE USER energy WITH PASSWORD 'x9308PslyT@#^&';"
psql postgres -c "CREATE DATABASE energyspazr OWNER energy;"
psql postgres -c "GRANT ALL PRIVILEGES ON DATABASE energyspazr to energy;"

#Ubuntu
#sudo -i -u postgres psql -c "CREATE USER energy WITH PASSWORD 'x9308PslyT@#^&';"
#sudo -i -u postgres psql -c "CREATE DATABASE energyspazr OWNER energy;"
#sudo -i -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE energyspazr to energy;"


