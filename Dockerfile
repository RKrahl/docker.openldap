FROM rkrahl/opensuse:15.2

RUN zypper --non-interactive install \
	cyrus-sasl \
	openldap2 \
	openldap2-client

COPY start-openldap.py /usr/local/lib/start-openldap
RUN chmod 0755 /usr/local/lib/start-openldap

CMD ["/usr/local/lib/start-openldap"]

VOLUME ["/var/lib/ldap"]

EXPOSE 389 636
