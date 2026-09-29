import argparse 
import socket
from concurrent.futures import ThreadPoolExecutor,as_completed
import time
import json


class port_actions:
    def __init__(self):
        pass


    def port_check(self,ports):
        p_len = 1
        try:
            portset = set()
            if "," in ports:
                ports1 = ports.split(",")
                p_len = len(ports1)
                for p in ports1:
                    p_toint = int(p)
                    if not (0 <= p_toint <= 65535) :
                        raise ValueError("端口范围不合理，请重新输入")
                    else:
                        portset.add(p_toint)
                print(portset)
                return portset,p_len
            elif "-" in ports:
                p_start,p_end = ports.split("-",1)
                p_len = int(p_end) - int(p_start) + 1
                if not (0 <= int(p_start) <= 65535) or not (0 <= int(p_end) <= 65535):
                    raise ValueError("端口范围不合理，请重新输入")
                elif int(p_start) > int(p_end):
                    raise ValueError("起始端口不能大于终点端口，请重新输入")
                else:
                    portset.update(range(int(p_start),int(p_end)+1))
                    return portset,p_len
            elif 0 <= int(ports) <= 65535:
                portset.add(int(ports))
                return portset,p_len
            else:
                raise ValueError("端口范围不合理，请重新输入")
        except ValueError as v:
            print(v)
            return None,p_len
        except Exception as e:
            print("未知错误")
            return None,p_len

    
    def target_check(self,ipf):
        try:
            ip = ipf.lower()
            if ip == "0.0.0.0" or ip == "255.255.255.255":
                print("禁止未指定地址或广播地址，请重新输入")
                return False
            if "." not in ip:
                raise ValueError 
            vt1 = ip.split(".")
            for i in vt1 :
                if not (i.isdigit()):
                    return ip
                vt2 = int(i)
                if len(vt1) != 4:
                    raise ValueError
                if not (0 <= vt2 <= 255):
                    raise ValueError
            return ip
        except ValueError as v:
            print("输入的ip或域名内容非法，请重新输入")
            return None
        except Exception as e:
            print(type(e).__name__,e)
            return None

        
    def ports_scan(self,ip,ports,timeout,banner = False):
        target = None
        s = None
        dedate = ""
        try:
            s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            target = socket.gethostbyname(ip)
            s.settimeout(timeout)
            s.connect((target,ports))
            if banner:
                try:
                    s.settimeout(timeout)
                    date = s.recv(1024)
                    dedate = date.decode("utf-8")
                    print(f"收到回复: {dedate}")
                except socket.timeout :
                    dedate = ""
            return "目标端口开启",f"{str(ports)}",f"{target}",f"端口回复：{dedate}"
        except socket.gaierror as g :
            print(f"域名解析失败,{g}")
            return None
        except ConnectionRefusedError as cr:
            return "目标端口关闭",f"{str(ports)}",f"{target}",f"端口回复：{dedate}"
        except socket.timeout as st:
            return "超时或目标不可达",f"{str(ports)}",f"{target}",f"端口回复：{dedate}"
        except Exception as e:
            print(type(e).__name__,e)
            return e,str(ports),target,dedate
        finally:
            s.close()

    def TPE(self,concurrency,ip,ports,timeout,banner = False,output = False):
        global open_p,p_count,ac,target
        with ThreadPoolExecutor(max_workers=concurrency) as ext:
            futures = [ext.submit(self.ports_scan,ip,p,timeout,banner) for p in ports]
            try:
                for f in as_completed(futures):
                    r = f.result()
                    if '目标端口关闭' not in r and '超时或目标不可达' not in r and f.result() is not None:
                        open_p.append(r[1])
                    elif r is None:
                        print("发现结果返回None,可能是域名解析失败，中止任务")
                        for o in futures:
                            o.cancel()
                        break
                    print(r)
                    if output:
                        js = {
                                "scan_info": {
                                    "target": target,
                                    "ip": r[2],
                                    "port_count_scanned": p_count,
                                    "concurrency": concurrency,
                                    "timeout_sec": timeout,
                                }
                                }
                        if banner:
                            js["results"] = [
                                {
                                    "port":r[1],
                                    "state":r[0],
                                    "banner":r[3]
                                }
                            ]
                        else:
                            js["results"] = [
                                {
                                    "port":r[1],
                                    "state":r[0],
                                    "banner":""
                                }
                            ]    
                        with open("scan_result.json","w",encoding="utf-8") as f3:
                            json.dump(js,f3,indent=4,ensure_ascii=False)
            except KeyboardInterrupt:
                print("收到Ctrl + c,程序正在退出...")
                for fut in futures:
                    fut.cancel()
            else:
                return r[2]

                
                
 
if __name__ == "__main__":
        print("=" * 60)
        print("⚠️  本工具仅供授权测试与学习使用,请勿用于非法用途!")
        print("=" * 60)
        pg = "21,22,23,25,53,80,110,143,443,445,1433,1521,3306,3389,5432,5900,6379,8080,8443,27017"
        open_p = []
        vt = argparse.ArgumentParser()
        vt.add_argument("-t","--target",required=True,help="输入一个ip或者域名")
        vt.add_argument("-p","--ports",default=pg,help="输入一个或以上数量的端口,若只输入一个端口则只扫描一个端口；若扫描若干数量端口则输入例如:80,3306,8080,....的格式；若需要扫描特定范围的端口，则输入: 起始端口-终点端口 的格式，起始端口必须小于终点端口，例如:720-888，不输入则进行默认端口的扫描")
        vt.add_argument("-c","--concurrency",default=50,help="输入一个数字，设定并发数量单元上限")
        vt.add_argument("--timeout",type=float,default=1.5,help="设置超时时间")
        vt.add_argument("-b","--banner",action="store_true",help="若携带此参数，则在探测到开放端口后尝试抓取服务指纹信息；若未携带，仅做快速端口开放性探测。")
        vt.add_argument("-o","--output",action="store_true",help="若指定此参数，以 JSON 格式结构化保存到当前目录的scan_result.json文件")
        args = vt.parse_args()
        ac = port_actions()
        target = args.target
        ip_T = ac.target_check(args.target)
        port_T = ac.port_check(args.ports)[0]
        p_count = ac.port_check(args.ports)[1]
        if port_T and ip_T:
            start = time.time()
            aTPE = ac.TPE(args.concurrency,ip_T,port_T,args.timeout,args.banner,args.output)
            end = time.time()
            elapsed_time_sec = f"{end - start:.2f}"
            print(f"扫描结束，开放端口为 {open_p}")
            print(f"耗时{elapsed_time_sec}秒")
