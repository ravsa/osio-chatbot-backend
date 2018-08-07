FROM centos:7

MAINTAINER Ravindra Ratnawat <ravindra@redhat.com>

ENV LANG="en_US.utf8"
ENV BAYESIAN_FETCH_PUBLIC_KEY="http://sso.openshift.io/"
ENV BAYESIAN_JWT_AUDIENCE="fabric8-online-platform,openshiftio-public"
EXPOSE 8008
RUN groupadd pyuser && adduser -g pyuser pyuser


RUN yum install -y epel-release
RUN yum install -y python34-pip python34-devel
RUN yum groupinstall -y "Development Tools"
RUN yum clean all

RUN pip3 install -U pip
RUN pip3 install --upgrade setuptools
RUN pip3 install spacy

RUN python3 -m spacy download en
RUN python3 -m spacy download en_core_web_md
RUN python3 -m spacy link en_core_web_md en --force

COPY requirements.txt /bot-server/requirements.txt
WORKDIR /bot-server

RUN pip3 install -r requirements.txt
COPY . /bot-server

RUN chown -R pyuser:pyuser /bot-server

USER pyuser

RUN chmod a+x run.sh
CMD ["/bot-server/run.sh"]
