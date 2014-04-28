from twisted.internet import reactor
from twisted.names import dns, cache, client, common, server

import docker



class DockerResolver(client.Resolver):
    def __init__(self):
        common.ResolverBase.__init__(self)

        self.__client = docker.Client()


    def lookupAddress(self,
                      name,
                      timeout = None):
        address = self.__client.inspect_container(container = name)['NetworkSettings']['IPAddress']

        return ([dns.RRHeader(name = name,
                              type = dns.A,
                              cls = dns.IN,
                              ttl = 60,
                              payload = dns.Record_A(address = address,
                                                     ttl = 60),
                              auth = True)],
                [],
                [])


def main():
    resolver = DockerResolver()
    factory = server.DNSServerFactory(caches = [cache.CacheResolver()],
                                      clients = [resolver])
    protocol = dns.DNSDatagramProtocol(factory)

    reactor.listenUDP(10053, protocol)
    reactor.run()


if __name__ == '__main__':
    main()

