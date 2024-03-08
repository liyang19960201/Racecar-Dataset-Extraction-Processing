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
nodes.Create(3) 






#The mobility could be set here

mobility=ns.mobility.MobilityHelper()
mobility.SetMobilityModel("ns3::ConstantPositionMobilityModel")
mobility.Install(nodes.Get(0))

mobility.SetMobilityModel ("ns3::RandomWalk2dMobilityModel", "Bounds", ns.mobility.RectangleValue(ns.mobility.Rectangle (-50, 50, -50, 50)))
mobility.Install(nodes.Get(1))

mobility.SetMobilityModel ("ns3::RandomWalk2dMobilityModel", "Bounds", ns.mobility.RectangleValue(ns.mobility.Rectangle (-50, 50, -50, 50)))
mobility.Install(nodes.Get(2))


pointToPoint=ns.point_to_point.PointToPointHelper()
pointToPoint.SetDeviceAttribute("DataRate",ns.core.StringValue("5Mbps"))
pointToPoint.SetChannelAttribute("Delay",ns.core.StringValue("2ms"))



devices=pointToPoint.Install(nodes.Get(0),nodes.Get(1))
devices1=pointToPoint.Install(nodes.Get(2),nodes.Get(1))

stack=ns.internet.InternetStackHelper()
stack.Install(nodes)









address=ns.internet.Ipv4AddressHelper()
address.SetBase(ns.network.Ipv4Address("192.168.1.0"),
                ns.network.Ipv4Mask("255.255.255.0"))


address1=ns.internet.Ipv4AddressHelper()
address1.SetBase(ns.network.Ipv4Address("192.168.2.0"),
                 ns.network.Ipv4Mask("255.255.255.0"))


interfaces=address.Assign(devices)

interfaces1=address1.Assign(devices1)


echoServer=ns.applications.UdpEchoServerHelper(90)
echoServer1=ns.applications.UdpEchoServerHelper(91)



serverApps=echoServer.Install(nodes.Get(1))
serverApps.Start(ns.core.Seconds(1.0))
serverApps.Stop(ns.core.Seconds(10.0))


serverApps1=echoServer1.Install(nodes.Get(2))
serverApps1.Start(ns.core.Seconds(1.0))
serverApps1.Stop(ns.core.Seconds(10.0))

address=interfaces.GetAddress(1).ConvertTo()
print(address)
echoClient=ns.applications.UdpEchoClientHelper(address, 90)
echoClient.SetAttribute("MaxPackets",ns.core.UintegerValue(3))
echoClient.SetAttribute("Interval",ns.core.TimeValue(ns.core.Seconds(1.0)))
echoClient.SetAttribute("PacketSize",ns.core.UintegerValue(4096))


#This sectionc can cause segment violation


address1=interfaces1.GetAddress(0).ConvertTo()
print(address1)
echoClient1=ns.applications.UdpEchoClientHelper(address1,91)
echoClient1.SetAttribute("MaxPackets",ns.core.UintegerValue(3))
echoClient1.SetAttribute("Interval",ns.core.TimeValue(ns.core.Seconds(1.0)))
echoClient1.SetAttribute("PacketSize",ns.core.UintegerValue(4096))



clientApps=echoClient.Install(nodes.Get(0))
clientApps.Start(ns.core.Seconds(2.0))
clientApps.Stop(ns.core.Seconds(10.0))



clientApps1=echoClient1.Install(nodes.Get(2))
clientApps1.Start(ns.core.Seconds(2.0))
clientApps1.Stop(ns.core.Seconds(10.0))


#The animation section will be developed sooner or later
# anim=ns.mobility.AnimationInterface("animation.xml")

# anim.SetMobilityPollInterval(ns.core.Seconds(1))


# anim.SetConstantPosition(nodes.Get(1),10.0,20.0,0.0)
# anim.SetStartTime(ns.core.Seconds(150))
# anim.SetStopTime(ns.core.Seconds(160))

# anim.EnablePacketMetadata(True)
# anim.UpdateNodeDescription(1,"Access-point")


# anim.UpdateNodeSize(1,1.5,1.5)
# anim.UpdateNodeCounter(0,7,3.4)




    
ns.core.Simulator.Stop(ns.core.Seconds(10.0))
ns.core.Simulator.Run()

ns.core.Simulator.Destroy()





