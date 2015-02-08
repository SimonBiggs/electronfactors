FROM simonbiggs/jupyter

ADD . /home/admin

RUN chown admin:admin /home/admin/*.ipynb
