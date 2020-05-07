# Use the official Python image to create a build artifact.
# This is based on Debian and sets the GOPATH to /go.
# https://hub.docker.com/_/python
FROM python:3 as builder

# Make skills-tickets directory
RUN mkdir /skills-tickets

# Copy local code to the container image.
COPY *.py /skills-tickets/
COPY README.md /skills-tickets/
COPY LICENSE /skills-tickets/
COPY Dockerfile /skills-tickets/
COPY hack/ /skills-tickets/hack/
COPY test/ /skills-tickets/test/

# Insall dependencies via pip.
RUN pip install PyYAML==5.3.1
RUN pip install uservoice==0.0.25
RUN pip install docopt==0.6.2

# Build and run UTs
RUN /skills-tickets/hack/build.sh --tests

# Run sanity check.
CMD /skills-tickets/st.py --version