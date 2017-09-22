try:
    import configparser
except ImportError:
    import ConfigParser as configparser

from certmonger_comodo_helper import *


def main():
    # Set a default as it may not exist.
    config = configparser.ConfigParser({'ca_poll_wait': '60'})
    config.read('/etc/certmonger/comodo.ini')

    crt = ComodoTLSService(customer_login_uri=config.get('default', 'customer_login_uri'),
                           org_id=config.get('default', 'org_id'),
                           password=config.get('default', 'password'),
                           secret_key=config.get('default', 'secret_key'),
                           login=config.get('default', 'login'),
                           ca_poll_wait=config.getint('default', 'ca_poll_wait'))

    env = get_environment()

    if env['CERTMONGER_OPERATION'] == 'SUBMIT':
        crt.submit(cert_type_name=config.get('default', 'cert_type_name'),
                   revoke_password=config.get('default', 'revoke_password'),
                   term=config.get('default', 'term'))
    elif env['CERTMONGER_OPERATION'] == 'POLL':
        crt.poll()
    else:
        sys.exit(6)