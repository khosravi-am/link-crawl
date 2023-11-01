FROM exoplatform/ubuntu:20.04
LABEL maintainer="eXo Platform <docker@exoplatform.com>"

RUN mkdir /app 

WORKDIR /app

RUN apt-get update && apt-get -y install openjdk-11-jdk-headless && rm -rf /var/lib/apt
RUN wget https://github.com/SeleniumHQ/selenium/releases/download/selenium-4.14.0/selenium-server-4.14.0.jar

ENTRYPOINT ["/usr/local/bin/tini", "--", "/usr/bin/java"]

