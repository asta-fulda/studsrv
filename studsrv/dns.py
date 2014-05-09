import socket
import traceback

import dnslib as dns

from studsrv.services.config import configs
from studsrv.services.project import projects



def main():
  # Open a socket listening for DNS requests
  server = socket.socket(socket.AF_INET,
                         socket.SOCK_DGRAM)
  server.bind((configs.dns_host,
               int(configs.dns_port)))

  # Build the servers root domain label
  domain = dns.DNSLabel(configs.dns_domain)

  while True:
    try:
      # Read the request packet
      pkt, adr = server.recvfrom(512)

      # Parse the request
      request = dns.DNSRecord.parse(pkt)

      # Build the response for the request
      response = dns.DNSRecord(dns.DNSHeader(id = request.header.id,
                                             qr = 1,
                                             aa = 1,
                                             ra = 1),
                               q = request.q)

      # Try to find the project named by the suffix of the requested address
      project = None
      if (dns.QTYPE[request.q.qtype] == 'A' and
          dns.CLASS[request.q.qclass] == 'IN' and
          request.q.qname.matchSuffix(domain)):
        # Get the domains prefix and strip of the trailing dot
        name = str(request.q.qname.stripSuffix(domain))[:-1]

        # Look the project up in the database
        project = projects.getProject(name = name)

      # Build the answer with the IP of the project
      if project is not None:
        response.add_answer(dns.RR(rname = request.q.qname,
                                   rtype = request.q.qtype,
                                   rclass = request.q.qclass,
                                   ttl = int(configs.dns_ttl),
                                   rdata = dns.A(project.ip)))

      # Send out the response
      server.sendto(response.pack(),
                    adr)

    except KeyboardInterrupt:
      break

    except:
      traceback.print_exc()

  # Close the socket in any case
  server.close()


if __name__ == '__main__':
  main()
