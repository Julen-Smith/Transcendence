POSTGRES_USER="Astro98"
POSTGRES_PASSWORD="Tr4nsc3nd3nc3!"
POSTGRES_DB="transcendence"
POSTGRES_HOST="postgres"
LOGIN_PORT=25671
SECRET_KEY="c52c0b4e6aa0ab54d16b144f9820933dba18fcca13e075cf00752725e76f9947"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30
POSTGRES_INITDB_WALDIR="./Volumes/Database/login/Logs"
LOGGER_PARAMS="/app/tools/logger.json"
PARAMS="/app/tools/params.json"
INTRA_UID= "u-s4t2ud-6b7efca18b23485e50a6d9bc6df43ecc1024f25f5cf92dc6fd473fcc8647e21c"
INTRA_SECRET= "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"
INTRA_REDIRECT_URI='http://localhost:4242/api/login/intra_callback'
INTRA_AUTH_URL= 'https://api.intra.42.fr/oauth/authorize'
INTRA_VERIFY_URL='https://api.intra.42.fr/oauth/token'
GATEWAY_PORT=4242
GOOGLE_LOGIN_URL="http://login:25671/api/login/google"
GOOGLE_CALLBACK_URL="http://login:25671/api/login/google/callback"