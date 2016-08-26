# Start with fedora 23
FROM fedora:23

# Hi
MAINTAINER Hawken Rives hawkrives@fastmail.fm

# Install system tools / libraries
RUN dnf install -y python3 gcc gcc-c++ make clang

# Set up a mount point for the student information
WORKDIR /opt/student
VOLUME /opt/student

# Prepare for non-root access
RUN groupadd -r overseer && useradd -r -g overseer overseer
USER overseer
