

from ns import ns


import sys


#This file should represent the fundamental typology:
#
#There should have two nodes, one is staying in fixed position
#Another one should make some random movement
#
#The channel should be limited at data rate__



# Method1--Logout the proper output
# ns.core.LogComponentEnable("lteUeDevice",ns.core.LOG_LEVEL_INFO)#enable log environment
# ns.core.LogComponentEnable("lteEnbDevice",ns.core.LOG_LEVEL_INFO)


#

#####Setting BS node x1
bsnodes=ns.network.NodeContainer()

bsnodes.Create(1)


print(bsnodes.Get(0).GetTypeId())

#####Setting UE nodes x2
uenodes=ns.network.NodeContainer()
uenodes.Create(2)

print(uenodes.Get(0).GetTypeId())



# # #this section should be about position

mobility = ns.mobility.MobilityHelper()#This is where my project has to use
mobility.SetPositionAllocator("ns3::GridPositionAllocator", "MinX", ns.core.DoubleValue(0.0),
                              "MinY", ns.core.DoubleValue (0.0), "DeltaX", ns.core.DoubleValue(5.0), "DeltaY", ns.core.DoubleValue(10.0),
                              "GridWidth", ns.core.UintegerValue(3), "LayoutType", ns.core.StringValue("RowFirst"))



mobility.SetMobilityModel("ns3::ConstantPositionMobilityModel")
mobility.Install(bsnodes)


mobility.SetMobilityModel ("ns3::RandomWalk2dMobilityModel", "Bounds", ns.mobility.RectangleValue(ns.mobility.Rectangle (-50, 50, -50, 50)))
mobility.Install(uenodes)





#The protocol here based on the example is LTE&&#This is the step to connect UEs to BS



lteHelper =ns.CreateObject("LteHelper")
bsDevs = lteHelper.InstallEnbDevice(bsnodes)

ueDevs = lteHelper.InstallUeDevice(uenodes)
lteHelper.Attach(ueDevs, bsDevs.Get(0))

# lteHelper.EnableLogComponents()


#troutbleshooting



#Data Radio bearer 

qci=ns.lte.EpsBearer.GBR_CONV_VOICE

bearer=ns.lte.EpsBearer(qci)

lteHelper.ActivateDataRadioBearer(ueDevs,bearer)



    
ns.core.Simulator.Stop(ns.core.Seconds(0.005))
ns.core.Simulator.Run()

ns.core.Simulator.Destroy()


