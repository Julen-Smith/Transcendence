FROM owasp/modsecurity-crs:nginx

COPY conf/before-crs.conf /etc/modsecurity.d/owasp-crs/rules/REQUEST-900-EXCLUSION-RULES-BEFORE-CRS.conf
COPY conf/after-crs.conf /etc/modsecurity.d/owasp-crs/rules/RESPONSE-999-EXCLUSION-RULES-AFTER-CRS.conf
COPY conf/default.conf /etc/nginx/templates/conf.d/default.conf.template