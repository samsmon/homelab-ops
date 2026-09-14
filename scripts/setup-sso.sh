#!/usr/bin/env bash
# Script to configure Nextcloud Native OIDC using occ

echo "Configuring Nextcloud Native OIDC..."
docker exec -u www-data nextcloud php occ app:install user_oidc
docker exec -u www-data nextcloud php occ user_oidc:provider add homelab-idp \
    --clientid="nextcloud-oidc-sso" \
    --clientsecret="ba7e49089a333e534ae3690b166974208eb6922ead28ae7a" \
    --discoveryuri="http://192.168.18.225:8300/.well-known/openid-configuration" \
    --scope="openid profile email"

echo "Done! Please ensure Nextcloud is running."
