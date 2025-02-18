# deploy-video-service

Deploy a service to collect photos and information from a video camera.

## Slik går du fram for å kjøre dette lokalt eller på en skytjeneste

1. Sette opp virtuell server. Dette bør være en server med GPU for å kjøre real-time video analyse
  
2. Networking: Open up port 8080 for incoming traffic from any * incoming source.

3. kommandoer for å innstallere containere (kan trolig optimaliseres - trenger ikke alt dette)

```Shell
sudo apt update

## conda installasjon
curl -O https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
sh Miniconda3-latest-Linux-x86_64.sh
## restart shell
conda install pytorch torchvision torchaudio cpuonly -c pytorch

sudo apt install docker-compose
sudo git clone https://github.com/langrenn-sprint/deploy-video-service.git
# copy .env file og secrets (inkl GOOGLE_APPLICATION_CREDENTIALS)
sudo usermod -aG docker $USER #deretter logge ut og inn igjen
# secrets og konfigurasjon
# opprette en .env fil med miljøvariable, se under
source .env
docker-compose pull
docker-compose up &
```

## Tilgang til Google Pub-sub (lokasjon til secrets file må ligge i .env GOOGLE_APPLICATION_CREDENTIALS)

Set upp application default credentials: https://cloud.google.com/docs/authentication/provide-credentials-adc#how-to

```Shell kommandoer hvis du skal laste filen opp på en Azure virtuell server
ssh -i /home/heming/github/sprint-ubuntu_key.pem azureuser@sprint.northeurope.cloudapp.azure.com
scp -i key.pem -r application_default_credentials.json azureuser@20.251.168.187:/home/azureuser/github/deploy-video-service/.
Tips: chmod 700 på nøkkelen
```

## Starte opp containere

Når du har logga inn på serveren, gå til folderen der docker-compose filen ligger og kjør følgende kommandoer:

```Filhåndtering - lage bind-mounts som stemmer med referansene i docker-compose filen
mkdir files

```Shell
docker-compose pull && docker-compose up -d # Henter siste versjon av containere og starter dem
# evt starte opp uten video-service
docker-compose up photo-service-gui event-service photo-service competition-format-service user-service mongodb
```

## Monitorere logger

Gå til folderen der docker-compose filen ligger og kjør følgende kommando:

```Shell
docker-compose logs -f
```

## Stoppe containere

Følgende kommando stopper alle services:

```Shell
docker-compose stop
```

Følgende kommando stopper og fjerner containere:

```Shell
docker-compose down
```

## slette images og containere

```Shell
docker image prune -a
docker rm -f $(sudo docker ps -a -q)
docker network prune
```

## Miljøvariable

Du må sette opp ei .env fil med miljøvariable. Eksempel:

```Shell
JWT_SECRET=secret
ADMIN_USERNAME=admin
ADMIN_PASSWORD=password
DB_USER=admin
DB_PASSWORD=password
EVENTS_HOST_SERVER=localhost
EVENTS_HOST_PORT=8082
PHOTOS_HOST_SERVER=localhost
PHOTOS_HOST_PORT=8092
FERNET_KEY=23EHUWpP_MyKey_MyKeyhxndWqyc0vO-MyKeySMyKey=
GOOGLE_APPLICATION_CREDENTIALS="application_default_credentials.json"
GOOGLE_CLOUD_PROJECT=sigma-celerity-257719
GOOGLE_PUBSUB_NUM_MESSAGES=1
GOOGLE_PUBSUB_TOPIC_ID=langrenn-sprint
GOOGLE_PUBSUB_SUBSCRIPTION_ID=langrenn-sprint-sub
GOOGLE_STORAGE_BUCKET=langrenn-sprint
GOOGLE_STORAGE_SERVER=https://storage.googleapis.com
GOOGLE_OAUTH_CLIENT_ID=12345My-ClientId12345.apps.googleusercontent.com
SERVICEBUS_NAMESPACE_CONNECTION_STR=connection_string
JWT_EXP_DELTA_SECONDS=3600
LOGGING_LEVEL=INFO
USERS_HOST_SERVER=localhost
USERS_HOST_PORT=8086
VIDEO_URL=https://harnaes.no/maalfoto/2023SkiMaal.mp4
LOCAL_PHOTO_DIRECTORY=/home/github/deploy-video-service/files
```
