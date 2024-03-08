from ns import ns
import sys


#This file should represent the fundamental typology:
#
#There should have two nodes, one is staying in fixed position
#Another one should make some random movement
#
#The channel should be limited at data rate__
#
#


ns.core.LogComponentEnable("UdpEchoClientApplication",ns.core.LOG_LEVEL_INFO)#enable log environment
ns.core.LogComponentEnable("UdpEchoServerApplication",ns.core.LOG_LEVEL_INFO)

nodes=ns.network.NodeContainer()
nodes.Create(2)

pointToPoint=ns.point_to_point.PointToPointHelper()
pointToPoint.SetDeviceAttribute("DataRate",ns.core.StringValue("5Mbps"))
pointToPoint.SetChannelAttribute("Delay",ns.core.StringValue("2ms"))

devices=pointToPoint.Install(nodes)

stack=ns.internet.InternetStackHelper()
stack.Install(nodes)



#this section should be about position

mobility = ns.mobility.MobilityHelper()#This is where my project has to use
mobility.SetPositionAllocator("ns3::GridPositionAllocator", "MinX", ns.core.DoubleValue(0.0),
                              "MinY", ns.core.DoubleValue (0.0), "DeltaX", ns.core.DoubleValue(5.0), "DeltaY", ns.core.DoubleValue(10.0),
                              "GridWidth", ns.core.UintegerValue(3), "LayoutType", ns.core.StringValue("RowFirst"))

mobility.SetMobilityModel ("ns3::RandomWalk2dMobilityModel", "Bounds", ns.mobility.RectangleValue(ns.mobility.Rectangle (-50, 50, -50, 50)))
mobility.Install(nodes.Get(0))

mobility.SetMobilityModel("ns3::ConstantPositionMobilityModel")
mobility.Install(nodes.Get(1))
####


address=ns.internet.Ipv4AddressHelper()
address.SetBase(ns.network.Ipv4Address("192.168.1.0"),
                ns.network.Ipv4Mask("255.255.255.0"))

interfaces=address.Assign(devices)

echoServer=ns.applications.UdpEchoServerHelper(9)


serverApps=echoServer.Install(nodes.Get(1))
serverApps.Start(ns.core.Seconds(1.0))
serverApps.Stop(ns.core.Seconds(10.0))

address=interfaces.GetAddress(1).ConvertTo()
echoClient=ns.applications.UdpEchoClientHelper(address, 9)
echoClient.SetAttribute("MaxPackets",ns.core.UintegerValue(3))
echoClient.SetAttribute("Interval",ns.core.TimeValue(ns.core.Seconds(1.0)))
echoClient.SetAttribute("PacketSize",ns.core.UintegerValue(4096))


clientApps=echoClient.Install(nodes.Get(0))
clientApps.Start(ns.core.Seconds(2.0))
clientApps.Stop(ns.core.Seconds(10.0))


anim=ns.mobility.AnimationInterface("animation.xml")

anim.SetMobilityPollInterval(ns.core.Seconds(1))


anim.SetConstantPosition(nodes.Get(1),10.0,20.0,0.0)
anim.SetStartTime(ns.core.Seconds(150))
anim.SetStopTime(ns.core.Seconds(160))

anim.EnablePacketMetadata(True)
anim.UpdateNodeDescription(1,"Access-point")


anim.UpdateNodeSize(1,1.5,1.5)
anim.UpdateNodeCounter(0,7,3.4)
    
ns.core.Simulator.Stop(ns.core.Seconds(5.0))
ns.core.Simulator.Run()

ns.core.Simulator.Destroy()





