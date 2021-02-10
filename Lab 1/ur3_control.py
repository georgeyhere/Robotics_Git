print("Program started.")


try:
    import sim 
except:
    print ('--------------------------------------------------------------')
    print ('"sim.py" could not be imported. This means very probably that')
    print ('either "sim.py" or the remoteApi library could not be found.')
    print ('Make sure both are in the same folder as this file,')
    print ('or appropriately adjust the file "sim.py"')
    print ('--------------------------------------------------------------')
    print ('')    

import time
import math
import msgpack

sim.simxFinish(-1)
clientID=sim.simxStart('127.0.0.1',19990,True,True,5000,5)

if clientID!=-1: # server connected
    print("Connected to remote API server")
    sim.simxAddStatusbarMessage(clientID,'Remote API server connected!',sim.simx_opmode_oneshot) # show status bar message in Coppelia
    
    res,objs=sim.simxGetObjects(clientID,sim.sim_handle_all,sim.simx_opmode_blocking) # call simxGetObjects
    if res==sim.simx_return_ok: # when data valid
        print('Number of objects in the scene: ',len(objs)) # display data
    else:
        print('Remote API function call returned with error code: ',res)
    
    executedMovId='notReady' 
    targetArm1='UR3' 
    stringSignalName=targetArm1+'_executedMovId'
    
    
    def waitForMovementExecuted(id): # checks if returned code is same as executed movement to determine if movement has been executed
        global executedMovId
        global stringSignalName
        while executedMovId!=id: # if executed move ID is not expected:
            retCode,s=sim.simxGetStringSignal(clientID,stringSignalName,sim.simx_opmode_buffer) 
            if retCode==sim.simx_return_ok:
                if type(s)==bytearray:
                    s=s.decode('ascii') # decode string to ascii if valid
                executedMovId=s
     
                
    # Start streaming stringSignalName string signal:
    sim.simxGetStringSignal(clientID,stringSignalName,sim.simx_opmode_streaming)
    
    # setup movement variables:
    mVel=100*math.pi/180 # convert from degrees to radians
    mAccel = 150*math.pi/180
    maxVel=[mVel,mVel,mVel,mVel,mVel,mVel] # set all joints to have same max velocity and acceleration
    maxAccel=[mAccel,mAccel,mAccel,mAccel,mAccel,mAccel] 
    targetVel=[0,0,0,0,0,0] # set initial target velocity = 0   
    
    # Start simulation: (necessary?)
    sim.simxStartSimulation(clientID,sim.simx_opmode_blocking)  
    
    waitForMovementExecuted('ready')
    
    
    # Send first movement sequence:
    # Go to center of cuboid
    targetConfig=[-16*math.pi/180,37*math.pi/180,100*math.pi/180,-50*math.pi/180,-90*math.pi/180,0]
    targetVel=[-0.5*math.pi/180,-0.5*math.pi/180,-0.5*math.pi/180,-0.5*math.pi/180,-0.5*math.pi/180,-0.5*math.pi/180]
    movementData={"id":"movSeq1","type":"mov","targetConfig":targetConfig,"targetVel":targetVel,"maxVel":maxVel,"maxAccel":maxAccel}
    packedMovementData=msgpack.packb(movementData)
    sim.simxCallScriptFunction(clientID,targetArm1,sim.sim_scripttype_childscript,'legacyRapiMovementDataFunction',[],[],[],packedMovementData,sim.simx_opmode_oneshot)    
    
    
    # Send second movement sequence:
    # Go to Corner 1
    targetConfig=[-9*math.pi/180,46*math.pi/180,85*math.pi/180,-47*math.pi/180,-90*math.pi/180,0]
    targetVel=[-0.5*math.pi/180,-0.5*math.pi/180,-0.5*math.pi/180,-0.5*math.pi/180,-0.5*math.pi/180,-0.5*math.pi/180]
    movementData={"id":"movSeq2","type":"mov","targetConfig":targetConfig,"targetVel":targetVel,"maxVel":maxVel,"maxAccel":maxAccel}
    packedMovementData=msgpack.packb(movementData)
    sim.simxCallScriptFunction(clientID,targetArm1,sim.sim_scripttype_childscript,'legacyRapiMovementDataFunction',[],[],[],packedMovementData,sim.simx_opmode_oneshot)
    
    # Send third movement sequence
    # Go to Corner 2
    targetConfig=[-20*math.pi/180,46*math.pi/180,85*math.pi/180,-48*math.pi/180,-90*math.pi/180,0]
    targetVel=[-0.5*math.pi/180,-0.5*math.pi/180,-0.5*math.pi/180,-0.5*math.pi/180,-0.5*math.pi/180,-0.5*math.pi/180]
    movementData={"id":"movSeq3","type":"mov","targetConfig":targetConfig,"targetVel":targetVel,"maxVel":maxVel,"maxAccel":maxAccel}
    packedMovementData=msgpack.packb(movementData)
    sim.simxCallScriptFunction(clientID,targetArm1,sim.sim_scripttype_childscript,'legacyRapiMovementDataFunction',[],[],[],packedMovementData,sim.simx_opmode_oneshot)
    
    # Send fourth movement sequence
    # Intermediary move; lift up and rotate a bit to gain clearance
    targetConfig=[-27*math.pi/180,30*math.pi/180,85*math.pi/180,-70*math.pi/180,-90*math.pi/180,0]
    targetVel=[-0.5*math.pi/180,-0.5*math.pi/180,-0.5*math.pi/180,-0.5*math.pi/180,-0.5*math.pi/180,-0.5*math.pi/180]
    movementData={"id":"movSeq4","type":"mov","targetConfig":targetConfig,"targetVel":targetVel,"maxVel":maxVel,"maxAccel":maxAccel}
    packedMovementData=msgpack.packb(movementData)
    sim.simxCallScriptFunction(clientID,targetArm1,sim.sim_scripttype_childscript,'legacyRapiMovementDataFunction',[],[],[],packedMovementData,sim.simx_opmode_oneshot)
    
    # Send fifth movement sequence
    # Go to Corner 3
    targetConfig=[-26*math.pi/180,30*math.pi/180,117*math.pi/180,-66*math.pi/180,-90*math.pi/180,0]
    targetVel=[-0.5*math.pi/180,-0.5*math.pi/180,-0.5*math.pi/180,-0.5*math.pi/180,-0.5*math.pi/180,-0.5*math.pi/180]
    movementData={"id":"movSeq5","type":"mov","targetConfig":targetConfig,"targetVel":targetVel,"maxVel":maxVel,"maxAccel":maxAccel}
    packedMovementData=msgpack.packb(movementData)
    sim.simxCallScriptFunction(clientID,targetArm1,sim.sim_scripttype_childscript,'legacyRapiMovementDataFunction',[],[],[],packedMovementData,sim.simx_opmode_oneshot)
    
    # Send sixth movement sequence
    # Go to Corner 4
    targetConfig=[-11*math.pi/180,30*math.pi/180,117*math.pi/180,-66*math.pi/180,-90*math.pi/180,0]
    targetVel=[-0.5*math.pi/180,-0.5*math.pi/180,-0.5*math.pi/180,-0.5*math.pi/180,-0.5*math.pi/180,-0.5*math.pi/180]
    movementData={"id":"movSeq6","type":"mov","targetConfig":targetConfig,"targetVel":targetVel,"maxVel":maxVel,"maxAccel":maxAccel}
    packedMovementData=msgpack.packb(movementData)
    sim.simxCallScriptFunction(clientID,targetArm1,sim.sim_scripttype_childscript,'legacyRapiMovementDataFunction',[],[],[],packedMovementData,sim.simx_opmode_oneshot)    
    
    # Send seventh movement sequence
    # Go back to origin
    targetConfig=[0,0,0,0,0,0]
    targetVel=[-0.5*math.pi/180,-0.5*math.pi/180,-0.5*math.pi/180,-0.5*math.pi/180,-0.5*math.pi/180,-0.5*math.pi/180]
    movementData={"id":"movSeq7","type":"mov","targetConfig":targetConfig,"targetVel":targetVel,"maxVel":maxVel,"maxAccel":maxAccel}
    packedMovementData=msgpack.packb(movementData)
    sim.simxCallScriptFunction(clientID,targetArm1,sim.sim_scripttype_childscript,'legacyRapiMovementDataFunction',[],[],[],packedMovementData,sim.simx_opmode_oneshot)        
    
    time.sleep(1)
    
    
    # Execute movement sequences:
    sim.simxCallScriptFunction(clientID,targetArm1,sim.sim_scripttype_childscript,'legacyRapiExecuteMovement',[],[],[],'movSeq1',sim.simx_opmode_oneshot)
    waitForMovementExecuted('movSeq1') 
    sim.simxAddStatusbarMessage(clientID,'Movement 1 executed!',sim.simx_opmode_oneshot) # show status bar message in Coppelia    
    
    time.sleep(1)
    sim.simxCallScriptFunction(clientID,targetArm1,sim.sim_scripttype_childscript,'legacyRapiExecuteMovement',[],[],[],'movSeq2',sim.simx_opmode_oneshot)
    waitForMovementExecuted('movSeq2')
    sim.simxAddStatusbarMessage(clientID,'Movement 2 executed!',sim.simx_opmode_oneshot) # show status bar message in Coppelia
    
    time.sleep(1)
    sim.simxCallScriptFunction(clientID,targetArm1,sim.sim_scripttype_childscript,'legacyRapiExecuteMovement',[],[],[],'movSeq3',sim.simx_opmode_oneshot)
    waitForMovementExecuted('movSeq3')
    sim.simxAddStatusbarMessage(clientID,'Movement 3 executed!',sim.simx_opmode_oneshot) # show status bar message in Coppelia    

    time.sleep(1)
    sim.simxCallScriptFunction(clientID,targetArm1,sim.sim_scripttype_childscript,'legacyRapiExecuteMovement',[],[],[],'movSeq4',sim.simx_opmode_oneshot)
    waitForMovementExecuted('movSeq4')
    sim.simxAddStatusbarMessage(clientID,'Movement 4 executed!',sim.simx_opmode_oneshot) # show status bar message in Coppelia        
    
    time.sleep(0.5)
    sim.simxCallScriptFunction(clientID,targetArm1,sim.sim_scripttype_childscript,'legacyRapiExecuteMovement',[],[],[],'movSeq5',sim.simx_opmode_oneshot)
    waitForMovementExecuted('movSeq5')
    sim.simxAddStatusbarMessage(clientID,'Movement 5 executed!',sim.simx_opmode_oneshot) # show status bar message in Coppelia
    
    time.sleep(1)
    sim.simxCallScriptFunction(clientID,targetArm1,sim.sim_scripttype_childscript,'legacyRapiExecuteMovement',[],[],[],'movSeq6',sim.simx_opmode_oneshot)
    waitForMovementExecuted('movSeq6')
    sim.simxAddStatusbarMessage(clientID,'Movement 6 executed!',sim.simx_opmode_oneshot) # show status bar message in Coppelia  
    
    time.sleep(1)
    sim.simxCallScriptFunction(clientID,targetArm1,sim.sim_scripttype_childscript,'legacyRapiExecuteMovement',[],[],[],'movSeq7',sim.simx_opmode_oneshot)
    waitForMovementExecuted('movSeq7')
    sim.simxAddStatusbarMessage(clientID,'Movement 7 executed!',sim.simx_opmode_oneshot) # show status bar message in Coppelia        
    
    sim.simxGetPingTime(clientID)
    sim.simxFinish(clientID)
    
    
else:
    print("Not connected to remote API server")
    sys.exit("Could not connect")
    