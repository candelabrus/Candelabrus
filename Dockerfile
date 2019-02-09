# Use a clean Arch Linux base install as the parent of this image 
# This is good for development, but might not fit production
FROM archlinux/base

LABEL maintainer="Cláudio Pereira <development@claudiop.com>"

# Install required system packages.
# gcc:         GCC (required to compile uwsgi)
# python:      Django intrepreter
# python-pip:  Python package manager
# gdal:        Geographical extensions
# After finished, 
RUN pacman -Sy gcc python python-pip gdal --noconfirm --noprogressbar --cachedir /tmp

# Install pip packages
COPY pip-packages /usr/src/
RUN pip install --no-cache-dir --trusted-host pypi.python.org -r /usr/src/pip-packages && mkdir -p /candelabrus/http
COPY source /candelabrus/source
COPY locale /candelabrus/locale

# Tag exports
VOLUME  ["/candelabrus/config", "/candelabrus/http"]
# Change directory into project folder
WORKDIR /candelabrus
# Expose the uwsgi port
EXPOSE 1993

ENV CANDELABRUS_CONFIG /candelabrus/config/settings.json
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Execute uwsgi daemon once this container runs
ENTRYPOINT ["uwsgi", "config/uwsgi.ini"]
