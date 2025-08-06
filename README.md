<!-- # [Interface] section
# Address = 10.0.0.2/24           # Default: none (must be set)
# PrivateKey = <client private key> # Default: none (must be set)
# DNS = 1.1.1.1                   # Default: none (optional, common default)
# MTU = 1420                      # Default: auto (optional)
# ListenPort = 51820              # Default: random (optional)
#
# [Peer] section
# PublicKey = <server public key>  # Default: none (must be set)
# PresharedKey = <psk>             # Default: none (optional)
# AllowedIPs = 0.0.0.0/0           # Default: none (must be set)
# Endpoint = <server:51820>        # Default: none (must be set)
# PersistentKeepalive = 25         # Default: off (optional, 25 is common for clients) -->

<!-- /etc/wireguard/wg0.conf, sudo wg syncconf wg0 <(wg-quick strip wg0) -->

Was essentially recreating https://github.com/h44z/wg-portal; use this project instead. Leaving this repo archived in case anyone wants to see the key and QR code generation logic.
