ARG  FROM_IMAGE
FROM ${FROM_IMAGE}

LABEL version="1.0"
LABEL com.yanchirino="Yan Chirino"
LABEL description="ERP (Docker basado en Odoo Community v15)"
LABEL maintainer="Yan Chirino <support@yanchirino.com>"

USER root

COPY ./vendor                       /mnt/vendor-addons
COPY ./src                          /mnt/src-addons/src

RUN python3.9 -m pip install openpyxl
RUN python3.9 -m pip install pandas

USER odoo
