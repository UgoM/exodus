# Exodus
**Exodus** is meant to:
  * download a bunch of APK files from *Google Play*
  * find trackers signature in unzipped APK
  * retrieve application information like version, handle, ...
  * analyze the network traffic generated by the application
  * retrieve DNS queries and responses
  * retrieve HTTP posted data
  * generate JSON report

# Development environment
## Step 1 - System dependencies
```
sudo apt install git virtualenv postgresql-9.6 rabbitmq-server tshark aapt build-essential libssl-dev aapt libffi-dev python3-dev openjdk-8-jre
```

## Step 2 - Clone the project
```
git clone https://github.com/Exodus-Privacy/exodus.git
```

## Step 3 - Create database and user
```
sudo su - postgres
psql
CREATE USER exodus WITH PASSWORD 'exodus';
CREATE DATABASE exodus WITH OWNER exodus;
```

## Step 4 - Set Python virtual environment and install dependencies   
```
cd exodus
virtualenv ./venv -p python3
source venv/bin/activate
pip3 install -r requirements.txt
```

## Step 5 - Create the DB schema
```
cd exodus
python manage.py migrate --fake-initial --settings=exodus.settings.dev
python manage.py makemigrations --settings=exodus.settings.dev
python manage.py migrate --settings=exodus.settings.dev
```

## Step 6 - Create admin user
You have to activate the virtual venv and `cd` into the same directory as `manage.py` file.
```
source venv/bin/activate
cd exodus
python manage.py createsuperuser --settings=exodus.settings.dev
```

## Step 7 - Install Minio server
Minio is in charge to store files like APK, icons, flow and pcap files.
```
wget https://dl.minio.io/server/minio/release/linux-amd64/minio -O $HOME/minio
chmod +x $HOME/minio
```
### Configure Minio
```
mkdir -p $HOME/.minio
cat > $HOME/.minio/config.json << EOL
{
        "version": "20",
        "credential": {
                "accessKey": "exodusexodus",
                "secretKey": "exodusexodus"
        },
        "region": "",
        "browser": "on",
        "logger": {
                "console": {
                        "enable": true
                },
                "file": {
                        "enable": false,
                        "filename": ""
                }
        },
        "notify": {}
}
EOL
```

### Create Minio storage location
```
mkdir -p /tmp/exodus-storage
```

## Step 8 - Start Minio
```
$HOME/minio server /tmp/exodus-storage
```
Minio is now listening on `9000` port and the browser interface is available 
at [http://127.0.0.1:9000](http://127.0.0.1:9000). Use `exodusexodus` as both login 
and password.

## Step 9 - Start the εxodus worker
The εxodus handle asynchronous tasks submitted by the front-end.
You have to activate the virtual venv and `cd` into the same directory as `manage.py` file.
```
source venv/bin/activate
cd exodus
export DJANGO_SETTINGS_MODULE=exodus.settings.dev; python manage.py celery worker -A exodus.core -l info
```
Now, the εxodus worker is waiting for tasks.

## Step 10 - Start the εxodus front-end
You have to activate the virtual venv and `cd` into the same directory as `manage.py` file.
```
source venv/bin/activate
cd exodus
python manage.py runserver --settings=exodus.settings.dev
```
Now browse [http://127.0.0.1:8000](http://127.0.0.1:8000)

## Step * - Analyse an application
Browse [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/) and enter your login and password. Then, 
browse [http://127.0.0.1:8000/analysis/submit/](http://127.0.0.1:8000/analysis/submit/), specify an application handle 
and click on submit.

# FAQ
## GPlaycli refuses to download APK
It is probably a configuration issue. First of all, check the file `$HOME/.config/gplaycli/gplaycli.conf`, it 
should contains:
  * `android_ID=3d716411bf8bc802`
  
 If the issue remains, fill:
   * `gmail_address`
   * `gmail_password`
   
with a real Google Account :-(

## How to import another database?
You first need to delete the previous database, then import the new one :
```
sudo su - postgres
psql
DROP DATABASE exodus;
CREATE DATABASE exodus WITH OWNER exodus;
psql exodus < exodus.sql
```

