#!/usr/bin/env bash
# Script to configure Nextcloud Native OIDC using occ

echo "Configuring Nextcloud Native OIDC..."
docker exec -u www-data nextcloud php occ app:install user_oidc
docker exec -u www-data nextcloud php occ user_oidc:provider add homelab-idp \
    --clientid="nextcloud-oidc-sso" \
    --clientsecret="9571db4a32271589863f883de8196289e596cf5be0a0410c" \
    --discoveryuri="https://sso.suryatmaja.dev/.well-known/openid-configuration" \
    --scope="openid profile email"

echo "Done! Please ensure Nextcloud is running."
