import numpy
import pexpect


class WifiLatencyBenchmark(object):
    def __init__(self, ip):
        object.__init__(self)

        self.ip = ip
        self.interval = 0.5

        ping_command = 'ping ' + self.ip
        self.ping = pexpect.spawn(ping_command)

        self.ping.timeout = 1200
        self.ping.readline()  # init
        self.wifi_latency = []
        self.wifi_timeout = 0

        self.res_list = []

    def run_test(self, n_test):
        for n in range(n_test):
            p = self.ping.readline()
            p_str = str(p, encoding="utf-8").strip()
            print(p_str)
            print(type(p_str))
            self.res_list.append(p_str)


    def get_results(self):
        print(self.res_list)



if __name__ == '__main__':
    ip = 'www.baidu.com'
    n_test = 3

    my_wifi = WifiLatencyBenchmark(ip)

    my_wifi.run_test(n_test)
    my_wifi.get_results()