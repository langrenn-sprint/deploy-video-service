# deploy

Deploy a service to collect photos and information from a video camera.

## Slik går du fram for å kjøre dette lokalt eller på en skytjeneste

1. Sette opp virtuell server - ubuntu. Dette bør være en server med GPU for å kjøre real-time video analyse
2. Networking: Open up port 8080 for incoming traffic from any * incoming source.
3. Tildele dns navn - eks: ragdesprinten.norwayeast.cloudapp.azure.com

4. kommandoer for å innstallere containere (kan trolig optimaliseres - trenger ikke alt dette)

```Shell
sudo apt-get update
sudo apt-get install python-is-python3
curl -sSL https://install.python-poetry.org | python3 -
# log out and back in
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
scp -i sprint-langrenn_key.pem -r application_default_credentials.json azureuser@20.251.168.187:/home/azureuser/github/deploy/.
```

## Starte opp containere

Når du har logga inn på serveren, gå til folderen der docker-compose filen ligger og kjør følgende kommandoer:

```Shell
docker-compose pull && docker-compose up -d # Henter siste versjon av containere og starter dem
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
docker-compose rm result-service-gui
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
GOOGLE_APPLICATION_CREDENTIALS=/home/heming/github/secrets/application_default_credentials.json
GOOGLE_CLOUD_PROJECT=sigma-celerity-257719
GOOGLE_PUBSUB_NUM_MESSAGES=1
GOOGLE_PUBSUB_TOPIC_ID=langrenn-sprint
GOOGLE_PUBSUB_SUBSCRIPTION_ID=langrenn-sprint-sub
GOOGLE_STORAGE_BUCKET=langrenn-sprint
GOOGLE_STORAGE_SERVER=https://storage.googleapis.com
GOOGLE_OAUTH_CLIENT_ID=12345My-ClientId12345.apps.googleusercontent.com
SERVICEBUS_NAMESPACE_CONNECTION_STR=<connection string>
JWT_EXP_DELTA_SECONDS=3600
LOGGING_LEVEL=INFO
USERS_HOST_SERVER=localhost
USERS_HOST_PORT=8086
PHOTOS_FILE_PATH=files
VIDEO_URL=https://harnaes.no/maalfoto/2023SkiMaal.mp4
GLOBAL_SETTINGS_FILE=global_settings.json
VIDEO_STATUS_FILE=video_status.json
```