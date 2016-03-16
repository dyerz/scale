FROM geoint/scale
MAINTAINER Trevor R.H. Clarke <tclarke@ball.com>

# Doesn't seem to be a way to mount volumes as a non-root user
# with 0755 perms so we'll do this.
USER root

# Change the entrypoint to run gunicoem and export the port,
# everything is already in the base image
EXPOSE 8000
ENTRYPOINT ["/usr/bin/gunicorn", "-b", "0.0.0.0:8000", "scale.wsgi:application"]
