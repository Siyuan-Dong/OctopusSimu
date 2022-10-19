def add_arg(parser):
    parser.add_argument('--culprit_typ', default=3, type=int, help='type of problems')
    parser.add_argument('--mem', default=800, type=float, help='memory')
    parser.add_argument('--algo', default="dleft", type=str, help='algorithm')
    parser.add_argument('--error_ratio', default=0.25, type=float, help='ratio of error in a section')
    parser.add_argument('--test', default=0, type=int, help='type of test')
    parser.add_argument('--mem_num', default=0, type=int, help='rank of memory')
    parser.add_argument('--window', default=1, type=float, help='size of window compared to a section')
    parser.add_argument('--err_flow_ratio', default=0.1, type=float, help='ratio of culprit hosts')

    parser.add_argument('--ES_bucket_num', default=3, type=int, help='type of problems')
    parser.add_argument('--ES_memory', default=3, type=int, help='type of problems')
    parser.add_argument('--EDL_num', default=3, type=int, help='type of problems')
    parser.add_argument('--EDL_memory', default=3, type=int, help='type of problems')
    parser.add_argument('--CDL_num', default=3, type=int, help='type of problems')
    parser.add_argument('--CDL_memory', default=3, type=int, help='type of problems')


class Time_report:
    def __init__(self,
                 env):
        self.env = env
        self.action = env.process(self.run())

    def run(self):
        while True:
            yield self.env.timeout(1)
            print("time",self.env.now,end="; ",flush=True)


class CheckSwitch:
    def __init__(self,
                 env,
                 ft,
                 ab_fgroup,
                 sketches,
                 all_flows,
                 duration,
                 C_path,
                 args,
                 culprit_name,
                 culprit_typ,
                 culprit_time,
                 cnt_core,
                 cnt_edge,
                 n_flows,
                 correct_list,
                 culprit_fg) -> None:
        self.env = env
        self.ft = ft
        self.duration = duration
        self.ab_fgroup = ab_fgroup
        self.sketches = sketches
        self.all_flows = all_flows
        self.action = env.process(self.run())
        self.C_path = C_path
        self.args = args
        self.culprit_name = culprit_name
        self.culprit_typ = culprit_typ
        self.culprit_time = culprit_time
        self.cnt_core = cnt_core
        self.cnt_edge = cnt_edge
        self.n_flows = n_flows
        self.correct_list = correct_list
        self.culprit_fg = culprit_fg

    def convert(self,x):
        res = x.srcIP_dstIP()
        res = (res<<16)+x.srcPort()
        res = (res<<16)+x.dstPort()
        res = (res<<8)+x.proto()
        return res

    def converts(self,xs):
        ress = []
        for x in xs:
            res = self.convert(x)
            ress.append(res)
        return ress

    def intrsec(self,a1,b1,a2,b2):
        if a1>=a2 and a1<b2 and b1>b2:
            return 1
        elif b1>a2 and b1<=b2 and a1<a2:
            return 1
        elif a1>=a2 and b1<=b2:
            return 1
        elif a1<a2 and b1>b2:
            return 1
        return 0

    def run(self):
        while True:
            yield self.env.timeout(self.duration)
            f = open(self.C_path+"log_"+self.args.algo+"_"+self.culprit_name[self.culprit_typ]+".txt","a")
            
            ab_flow_list = []
            ab_flow_list.extend(self.sketches.get_ab_fs())
            conv_list = []
            for flo in ab_flow_list:
                tmp=(flo[0]<<72)+(flo[1]<<40)+(flo[2]<<24)+(flo[3]<<8)+flo[4]
                conv_list.append(tmp)
            print("ab_flow_list",conv_list,file=f)
            
            # if self.env.now > self.duration+1:
            for key in self.culprit_time.keys():
                if not self.intrsec(self.env.now-self.duration,self.env.now,key,self.culprit_time[key]):
                    continue
                reported_list = []
                for dle in range(0,self.cnt_core):
                    print(dle,self.sketches.coresketch[dle].PPrint(),file=f)
                for dle in range(0,self.cnt_edge):
                    print(dle,self.sketches.edgesketch[dle].PPrint(),file=f)
                for j in range(101,102,2):
                # for j in range(1,10,2):
                    t=0
                    if self.culprit_typ==0:
                        t=80/j
                    else:
                        t=j/100
                    ##############################################
                    if self.args.test==0:
                        print('test 0: ',self.args.culprit_typ,file=f)
                        s="../res/"+self.args.algo+"_"+self.culprit_name[self.args.culprit_typ]+".csv"
                        f_res = open(s,"a")
                    elif self.args.test==1:
                        print('test 1: ',self.args.culprit_typ,file=f)
                        s="../res_time/last"+str(self.args.error_ratio)+"_"+self.culprit_name[self.args.culprit_typ]+".csv"
                        f_res = open(s,"a")
                    elif self.args.test==2:
                        print('test 2: ',self.args.culprit_typ,file=f)
                        s="../res_edge/eflo"+str(self.args.err_flow_ratio)+"_"+self.culprit_name[self.args.culprit_typ]+".csv"
                        f_res = open(s,"a")
                    ##############################################
                    if self.args.test!=2:
                        print("traversing",end=": ",flush=True)
                        for flow_id in range(0,self.n_flows):
                            flow = self.all_flows[flow_id]

                            src_ip = flow.fid>>72
                            dst_ip = flow.fid>>40 & 0xffffffff
                            src_port = (flow.fid>>24) & 0xffff
                            dst_port = (flow.fid>>8) & 0xffff
                            _proto = flow.fid & 0xff
                            if not [src_ip,dst_ip,src_port,dst_port,_proto] in ab_flow_list:
                                continue
                        
                            length = len(flow.path)
                            # print("flow",flow.fid,"path",flow.path,file=f)
                            print("flow",flow.fid,"interval",flow.pkt_gen.arrival_interval,"path",flow.path,file=f)
                            if self.culprit_typ==3:
                                for i in range(2,length-1):
                                    last_wait = self.ft.nodes[flow.path[i-1]]['device'].sketch1.query_wait_pre(src_ip,dst_ip,src_port,dst_port,_proto)
                                    prst_wait = self.ft.nodes[flow.path[i]]['device'].sketch1.query_wait_pre(src_ip,dst_ip,src_port,dst_port,_proto)
                                    last_freq = self.ft.nodes[flow.path[i-1]]['device'].sketch1.query_pre(src_ip,dst_ip,src_port,dst_port,_proto)
                                    prst_freq = self.ft.nodes[flow.path[i]]['device'].sketch1.query_pre(src_ip,dst_ip,src_port,dst_port,_proto)
                                    print(flow.path[i-1],last_wait,last_freq,end=' * ',file=f)
                                    print(flow.path[i],prst_wait,prst_freq,file=f)
                                    if last_wait == 0:
                                        break
                                    if prst_wait/last_wait > t:
                                        print("flow",flow_id,"ab-switch",flow.path[i],file=f)
                                        reported_list.append([flow.fid,flow.path[i]])
                                        break
                            elif self.culprit_typ==2:
                                for i in range(2,length-1):
                                    last_interval = self.ft.nodes[flow.path[i-1]]['device'].sketch1.query_interval_pre(src_ip,dst_ip,src_port,dst_port,_proto)
                                    prst_interval = self.ft.nodes[flow.path[i]]['device'].sketch1.query_interval_pre(src_ip,dst_ip,src_port,dst_port,_proto)
                                    last_freq = self.ft.nodes[flow.path[i-1]]['device'].sketch1.query_pre(src_ip,dst_ip,src_port,dst_port,_proto)
                                    prst_freq = self.ft.nodes[flow.path[i]]['device'].sketch1.query_pre(src_ip,dst_ip,src_port,dst_port,_proto)
                                    print(flow.path[i-1],last_interval,last_freq,end=' * ',file=f)
                                    print(flow.path[i],prst_interval,prst_freq,file=f)
                                    if last_interval == 0:
                                        break
                                    if prst_interval/last_interval > t:
                                        print("flow",flow_id,"ab-switch",flow.path[i-1],file=f)
                                        reported_list.append([flow.fid,flow.path[i-1]])
                                        break
                            elif self.culprit_typ==1:
                                for i in range(2,length-1):
                                    last_freq = self.ft.nodes[flow.path[i-1]]['device'].sketch1.query_pre(src_ip,dst_ip,src_port,dst_port,_proto)
                                    prst_freq = self.ft.nodes[flow.path[i]]['device'].sketch1.query_pre(src_ip,dst_ip,src_port,dst_port,_proto)
                                    print(flow.path[i-1],last_freq,end=' ',file=f)
                                    print(flow.path[i],prst_freq,file=f)
                                    if last_freq == 0:
                                        break
                                    if prst_freq/last_freq > t:
                                        print("flow",flow_id,"ab-switch",flow.path[i],file=f)
                                        reported_list.append([flow.fid,flow.path[i]])
                                        break
                            elif self.culprit_typ==0:
                                for i in range(2,length-1):
                                    last_freq = self.ft.nodes[flow.path[i-1]]['device'].sketch1.query_pre(src_ip,dst_ip,src_port,dst_port,_proto)
                                    prst_freq = self.ft.nodes[flow.path[i]]['device'].sketch1.query_pre(src_ip,dst_ip,src_port,dst_port,_proto)
                                    print(flow.path[i-1],last_freq,end=' ',file=f)
                                    print(flow.path[i],prst_freq,file=f)
                                    if last_freq == 0:
                                        break
                                    if prst_freq/last_freq < t:
                                        print("flow",flow_id,"ab-switch",flow.path[i],file=f)
                                        reported_list.append([flow.fid,flow.path[i]])
                                        break

                        if len(reported_list):
                            inter_num=0
                            for ite in self.correct_list:
                                if ite in reported_list:
                                    inter_num+=1
                            prec = inter_num/len(reported_list)
                            recall = inter_num/len(self.correct_list)
                            # res_str = str(memcost)+","+str(prec)+","+str(recall)+","
                            # print(res_str,file=f_res)
                        else:
                            prec = 0
                            recall = 0
                            # res_str = str(memcost)+","+str(prec)+","+str(recall)+","
                            # print(res_str,file=f_res)
                        global check_num,check_prec,check_recall
                        check_num+=1
                        check_prec+=prec
                        check_recall+=recall
                        print("reported",len(reported_list),reported_list,file=f)
                        print("correct",len(self.correct_list),self.correct_list,file=f)
                        print("recall",recall,"precision",prec)
                        f_res.close()
                
                break    

            if self.args.algo == "dleft":
                self.ab_fgroup = self.sketches.ab_fg(self.culprit_num,self.culprit_typ)
                print("lala",len(self.ab_fgroup),self.ab_fgroup)
###################################################
                if self.args.test==2:
                    for key in self.culprit_time.keys():
                        if not self.intrsec(self.env.now-self.duration,self.env.now,key,self.culprit_time[key]):
                            continue
                        inter_num=0
                        rep_num=0
                        for ite in self.ab_fgroup:
                            if ite==0:
                                continue
                            rep_num+=1
                            if ite in self.culprit_fg:
                                inter_num+=1
                        prec=0
                        if rep_num:
                            prec = inter_num/rep_num
                        recall=inter_num/len(self.culprit_fg)
                        global edge_num,edge_prec,edge_recall
                        edge_num+=1
                        edge_prec+=prec
                        edge_recall+=recall
                        print("reported",len(self.ab_fgroup),self.ab_fgroup,file=f)
                        print("correct",len(self.culprit_fg),self.culprit_fg,file=f)
                        print("recall",recall,"precision",prec)
                        break
                ###################################################
            for n in self.ft.nodes():
                node = self.ft.nodes[n]
                node['device'].demux.loop_num=dict()
            
                if args.algo == "dleft":
                    for port in node['device'].egress_ports:
                        port.ab_fgroup = self.ab_fgroup
                        port.out.ab_fgroup = self.ab_fgroup
                    node['device'].demux.ab_fgroup = self.ab_fgroup
            
            self.sketches.Clear()
            f.close()