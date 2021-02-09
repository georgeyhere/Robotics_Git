print("Program started.")


try:
    import sim as vrep
except:
    print ('--------------------------------------------------------------')
    print ('"sim.py" could not be imported. This means very probably that')
    print ('either "sim.py" or the remoteApi library could not be found.')
    print ('Make sure both are in the same folder as this file,')
    print ('or appropriately adjust the file "sim.py"')
    print ('--------------------------------------------------------------')
    print ('')    

import time
vrep.simxFinish(-1)
clientID=vrep.simxStart('127.0.0.1',19999,True,True,5000,5)

if clientID!=-1:
    print("Connected to remote API server")
    
    res,objs=vrep.simxGetObjects(clientID,vrep.sim_handle_all,vrep.simx_opmode_blocking)
    if res==vrep.simx_return_ok:
        print('Number of objects in the scene: ',len(objs))
    else:
        print('Remote API function call returned with error code: ',res)
    
    time.sleep(2)
    vrep.simxAddStatusbarMessage(clientID,'API getting joint handles...',vrep.simx_opmode_oneshot)
    
    # get joint handles
    err_code,joint1_handle = vrep.simxGetObjectHandle(clientID, "UR3_joint1", vrep.simx_opmode_blocking)
    err_code,joint2_handle = vrep.simxGetObjectHandle(clientID, "UR3_joint2", vrep.simx_opmode_blocking)
    err_code,joint3_handle = vrep.simxGetObjectHandle(clientID, "UR3_joint3", vrep.simx_opmode_blocking)
    err_code,joint4_handle = vrep.simxGetObjectHandle(clientID, "UR3_joint4", vrep.simx_opmode_blocking)
    err_code,joint5_handle = vrep.simxGetObjectHandle(clientID, "UR3_joint5", vrep.simx_opmode_blocking)
    err_code,joint6_handle = vrep.simxGetObjectHandle(clientID, "UR3_joint6", vrep.simx_opmode_blocking)
    
    vrep.simxAddStatusbarMessage(clientID,'Going to Position 1.',vrep.simx_opmode_oneshot)
   
    vrep.simxSetJointTargetPosition(clientID,joint1_handle,2,vrep.simx_opmode_oneshot)
    # startTime=time.time() # set start time
    
    # while time.time()-startTime < 30:
        # returnCode,data=vrep.simxGetJointPosition(clientID,joint1_handle,vrep.simx_opmode_streaming)
        # if returnCode==vrep.simx_return_ok:
           # print('UR3_joint1 position: ',data)
        # time.sleep(0.05)
 
    time.sleep(5)
    
    vrep.simxGetPingTime(clientID)
    vrep.simxFinish(clientID)
    
    
else:
    print("Not connected to remote API server")
    sys.exit("Could not connect")
    