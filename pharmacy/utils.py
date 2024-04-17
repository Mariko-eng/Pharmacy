import random
from urllib.parse import urlparse

def generate_random_number():
    otp = random.randint(100000, 999999)
    return str(otp)


def build_file_path(request, file_url = None):
    # Get the request's host
    host = request.get_host()

    print(f"host1 : {host}")

    # Check if the host is an IP address
    if host.replace('.', '').isdigit():  # Checking if host is an IP address
        # Get the port number from the request
        host = request.META.get('REMOTE_ADDR', '127.0.0.1')
        port = request.META.get('REMOTE_PORT', '')
        if port:
            # Append the port number to the host
            host += f':{port}'

        print(f"host2 : {host}")
        
        invoice_url = request.build_absolute_uri(file_url) if file_url else None
        
        if invoice_url:
        # Replace the hostname with the updated one
            parsed_url = urlparse(invoice_url)
            invoice_url = parsed_url._replace(netloc=host).geturl()

        print(f"invoice_url1 : {invoice_url}")
        return invoice_url
    else:
        invoice_url = request.build_absolute_uri(file_url) if file_url else None

        print(f"invoice_url2 : {invoice_url}")
        return invoice_url


