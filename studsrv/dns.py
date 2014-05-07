import socket
import traceback
import dnslib as dns

from studsrv.services.project import projects



port = 10053
domain = dns.DNSLabel('stud.x.hs-fulda.org')
ttl = 60



def main():
  server = socket.socket(socket.AF_INET,
                         socket.SOCK_DGRAM)
  server.bind(('localhost', port))

  try:
    while True:
      pkt, adr = server.recvfrom(512)

      request = dns.DNSRecord.parse(pkt)
      print(request)

      response = dns.DNSRecord(dns.DNSHeader(id = request.header.id,
                                             qr = 1,
                                             aa = 1,
                                             ra = 1),
                               q = request.q)

#      response.add_ns(dns.RR(rname = domain,
#                             rtype = dns.QTYPE.NS,
#                             rclass = 1,
#                             ttl = ttl,
#                             rdata = dns.NS(dns.DNSLabel('localhost'))))
#
#      response.add_ns(dns.RR(rname = domain,
#                             rtype = dns.QTYPE.SOA,
#                             rclass = 1,
#                             ttl = ttl,
#                             rdata = dns.SOA(mname = dns.DNSLabel('localhost'),
#                                             rname = domain.add('edv'))))

      project = None
      if (dns.QTYPE[request.q.qtype] == 'A' and
          dns.CLASS[request.q.qclass] == 'IN' and
          request.q.qname.matchSuffix(domain)):
        # Get the domains prefix and strip of the trailing dot
        name = str(request.q.qname.stripSuffix(domain))[:-1]

        project = projects.getProject(name = name)

      if project is not None:
        response.add_answer(dns.RR(rname = request.q.qname,
                                   rtype = request.q.qtype,
                                   rclass = request.q.qclass,
                                   ttl = ttl,
                                   rdata = dns.A(project.ip)))

      print(response)

      server.sendto(response.pack(),
                    adr)

  except:
    traceback.print_exc()

    server.close()


if __name__ == '__main__':
  main()
