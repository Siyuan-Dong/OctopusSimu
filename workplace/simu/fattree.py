from functools import partial
from random import expovariate, sample
from numpy import random as nprdm
import random
from ns.packet.dist_generator import DistPacketGenerator
from ns.packet.sink import PacketSink
from ns.switch.switch import SimplePacketSwitch
from ns.switch.switch import FairPacketSwitch
# from ns.switch.switch import CheckSwitch
from ns.topos.fattree import build as build_fattree
from ns.topos.utils import generate_fib
from ns.topos.utils import PathGenerator
# from ns.topos.utils import generate_fib, generate_flows
import simpy
import numpy as np
import argparse
# import Sketches
import sys
sys.path.append('../')
import utils.TCP_distribution as tcpdist
import utils.create_error as cer
import utils.utils as utils

parser = argparse.ArgumentParser(description="draw results of a single flow")
parser = utils.add_arg(parser)


global args
args = parser.parse_args()
tst = ["core","time","edge"]

C_path="../C/"+args.algo+"/"
sys.path.append(C_path)
print(sys.path)
import Sketches
culprit_fg = set()
edge_num=0
edge_recall=0
edge_prec=0
print("args",args)
#####################################################

check_num=0
check_recall=0
check_prec=0

global correct_list
# reported_list = []
correct_list = []
memcost = args.mem
print("#",args.culprit_typ)
random.seed(125)
np.random.seed(125)
ff = open(C_path+"log.txt","w")

n_flows = 100000
k = 16
pir = 1000000000000000
buffer_size = 10000000000000000000000000
mean_pkt_size = 10.0
ab_fgroup = []
env = simpy.Environment()
sec_time=10
all_time=100
tp_time=0
sz = all_time//sec_time
poi_distri = nprdm.poisson(lam=sec_time,size=sz)
nor_distri = nprdm.normal(loc=sec_time*args.error_ratio,scale=sec_time*args.error_ratio/2,size=sz)
print("poi:",poi_distri,file=ff)
print("nor:",nor_distri,file=ff)
culprit_time=dict()
for s in range(sz):
    last_time = max(1,nor_distri[s])
    culprit_time[tp_time] = tp_time + last_time
    tp_time+=poi_distri[s]


sketches = Sketches.Sketches(k,args.ES_bucket_num, args.ES_memory,args.EDL_num, args.EDL_memory,args.CDL_num, args.CDL_memory)

culprit_num=int(k*k*k//4*args.err_flow_ratio)
culprit_typ= args.culprit_typ
culprit_name = ["black","loop","jitter","wait"]

f = open(C_path+"log_"+args.algo+"_"+culprit_name[culprit_typ]+".txt","w")
for key in culprit_time.keys():
    print("start:",key,"end:",culprit_time[key],file=f)
f.close()

ft = build_fattree(k)


time_rp = utils.Time_report(env)

hosts = set()
for n in ft.nodes():
    if ft.nodes[n]['type'] == 'host':
        hosts.add(n)

culprit_flows, culprit_switches, loop_pair = cer.create_error(hosts,culprit_typ,culprit_num,k)
print(culprit_switches,file=ff)
print(culprit_flows,file=ff)


PathGene = PathGenerator(ft,hosts,k)
all_flows = PathGene.generate_flows(n_flows,k)
size_dist = partial(expovariate, 1.0 / mean_pkt_size)
tmp_list = []

def constnt():
    return 0.1

for flow_id, flow in all_flows.items():
    arr_dist = constnt

    arrival_interval, is_big = tcpdist.TCP_Distribution(time = sec_time,lamda = 0.0001)
    flow.fid+= (is_big<<72)

    if ((flow.fid>>80) in culprit_flows) and ((flow.fid>>72)&1):
        print("culprit_switches",culprit_switches[(flow.fid>>80)],"path",flow.path,file=ff)
        for switch in flow.path:
            if switch in culprit_switches[(flow.fid>>80)]:
                correct_list.append([flow.fid, switch])
                culprit_fg.add((flow.fid>>80))
                break

    pg = DistPacketGenerator(env,
                             f"Flow_{flow.fid}",
                             arrival_dist = arr_dist,
                             arrival_interval=arrival_interval,
                             size_dist=size_dist,
                             flow_id=flow.fid)
    ps = PacketSink(env)

    all_flows[flow_id].pkt_gen = pg
    all_flows[flow_id].pkt_sink = ps


print("correct_list",len(correct_list),end="; ",flush=True)

ft = generate_fib(ft, all_flows)
n_classes_per_port = 4
weights = {c: 4 for c in range(n_classes_per_port)}
weights[n_classes_per_port]=0.1

cnt = {node_id: 0 for node_id in ft.nodes()}

def flow_to_classes(f_id, n_id=0):
    return (f_id + n_id ) % n_classes_per_port


cnt_edge=0
cnt_core=0
for node_id in ft.nodes():
    node = ft.nodes[node_id]

    flow_classes = partial(flow_to_classes,
                           n_id=node_id)
    if node['layer']=='edge':
        sketch1 = sketches.edgesketch[cnt_edge]
        sketch2=0
        sketch3=0
        if args.algo=="dleft":
            sketch2 = sketches.insketch[cnt_edge]
            sketch3 = sketches.outsketch[cnt_edge]
        cnt_edge+=1

        if args.algo=="dleft":
            node['device'] = FairPacketSwitch(env,k,pir,buffer_size,weights,'WFQ',flow_classes,
        # node['device'] = FairPacketSwitch(env,k,pir,buffer_size,weights,'DRR',flow_classes,
                                        element_id=node_id,
                                        layer=node['layer'],
                                        ab_fgroup=ab_fgroup,
                                        culprit_switches=culprit_switches,
                                        culprit_flows=culprit_flows,
                                        sketches=sketches,
                                        sketch1=sketch1,
                                        sketch2=sketch2,
                                        sketch3=sketch3,
                                        loop_pair=loop_pair,
                                        culprit_typ=culprit_typ,
                                        n_flows=n_flows,
                                        algo=args.algo,
                                        culprit_time=culprit_time)
        elif args.algo=="sumax" or args.algo=="marble":
            node['device'] = FairPacketSwitch(env,k,pir,buffer_size,weights,'WFQ',flow_classes,
        # node['device'] = FairPacketSwitch(env,k,pir,buffer_size,weights,'DRR',flow_classes,
                                        element_id=node_id,
                                        layer=node['layer'],
                                        ab_fgroup=ab_fgroup,
                                        culprit_switches=culprit_switches,
                                        culprit_flows=culprit_flows,
                                        sketches=sketches,
                                        sketch1=sketch1,
                                        # sketch2=sketch2,
                                        # sketch3=sketch3,
                                        loop_pair=loop_pair,
                                        culprit_typ=culprit_typ,
                                        n_flows=n_flows,
                                        algo=args.algo,
                                        culprit_time=culprit_time)
    elif node['layer']=='aggregation' or node['layer']=='core':
        sketch1 = sketches.coresketch[cnt_core]
        cnt_core+=1
        node['device'] = FairPacketSwitch(env,k,pir,buffer_size,weights,'WFQ',flow_classes,
        # node['device'] = FairPacketSwitch(env,k,pir,buffer_size,weights,'DRR',flow_classes,
                                        element_id=node_id,
                                        layer=node['layer'],
                                        ab_fgroup=ab_fgroup,
                                        culprit_switches=culprit_switches,
                                        culprit_flows=culprit_flows,
                                        sketches=sketches,
                                        sketch1=sketch1,
                                        loop_pair=loop_pair,
                                        culprit_typ=culprit_typ,
                                        n_flows=n_flows,
                                        algo=args.algo,
                                        culprit_time=culprit_time)
    elif node['layer']=='leaf':
        node['device'] = FairPacketSwitch(env,k,pir,buffer_size,weights,'WFQ',flow_classes,
        # node['device'] = FairPacketSwitch(env,k,pir,buffer_size,weights,'DRR',flow_classes,
                                        element_id=node_id,
                                        layer=node['layer'],
                                        ab_fgroup=ab_fgroup,
                                        culprit_switches=culprit_switches,
                                        culprit_flows=culprit_flows,
                                        sketches=sketches,
                                        loop_pair=loop_pair,
                                        culprit_typ=culprit_typ,
                                        n_flows=n_flows,
                                        algo=args.algo,
                                        culprit_time=culprit_time)

    node['device'].demux.fib = node['flow_to_port']
    node['device'].demux.nexthop_to_port = node['nexthop_to_port']

for n in ft.nodes():
    node = ft.nodes[n]
    for port_number, next_hop in node['port_to_nexthop'].items():
        node['device'].ports[port_number].out = ft.nodes[next_hop]['device']
        node['device'].ports[port_number+k].out = ft.nodes[next_hop]['device']


for flow_id, flow in all_flows.items():
    flow.pkt_gen.out = ft.nodes[flow.src]['device']
    ft.nodes[flow.dst]['device'].demux.ends[flow.fid] = flow.pkt_sink

    length = len(flow.path)
    for i in range(1,length-1):
        cnt[flow.path[i]]+=1

for n in ft.nodes():
    print(n,cnt[n],end="; ",file=ff)

check=utils.CheckSwitch(env,ft,ab_fgroup,sketches,all_flows,sec_time*args.window,
                    C_path=C_path,
                    args=args,
                    culprit_name=culprit_name,
                    culprit_typ=culprit_typ,
                    culprit_time=culprit_time,
                    cnt_core=cnt_core,
                    cnt_edge=cnt_edge,
                    n_flows=n_flows,
                    correct_list=correct_list,
                    culprit_fg=culprit_fg)
print("start running")
env.run(until=all_time+0.01)

#####################################################################
if args.test==0:
    s="../res/"+args.algo+"_"+culprit_name[args.culprit_typ]+".csv"
    f_res = open(s,"a")
elif args.test==1:
    s="../res_time/last"+str(args.error_ratio)+"_"+culprit_name[args.culprit_typ]+".csv"
    f_res = open(s,"a")
elif args.test==2:
    s="../res_edge/eflo"+str(args.err_flow_ratio)+"_"+culprit_name[args.culprit_typ]+".csv"
    f_res = open(s,"a")
if args.test==0:
    res_str = str(memcost)+","+str(check_prec/check_num)+","+str(check_recall/check_num)+","
elif args.test==1:
    res_str = str(args.window)+","+str(check_prec/check_num)+","+str(check_recall/check_num)+","
else:
    res_str = str(memcost)+","+str(edge_prec/edge_num)+","+str(edge_recall/edge_num)+","
print(res_str,file=f_res)
print(res_str)
f_res.close()
######################################################################
ff.close()