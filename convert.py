import sys
import os
import platform
import time
import ctypes
import getopt
import multiprocessing
import logging

from os.path import basename
from array import *

if sys.platform.startswith('win32'):
    import msvcrt
elif sys.platform.startswith('linux'):
    import atexit
    from select import select

from ctypes import *

try:
    if sys.platform.startswith('win32'):
        libEDK = cdll.LoadLibrary("lib/win32/edk.dll")
    # elif sys.platform.startswith('linux'):
        # srcDir = os.getcwd()
        # if platform.machine().startswith('arm'):
            # libPath = srcDir + "/../../bin/armhf/libedk.so"
        # else:
            # libPath = srcDir + "/../../bin/linux64/libedk.so"
        # libEDK = CDLL(libPath)
    else:
        raise Exception('System not supported.')
except Exception as e:
    print ("Error: cannot load EDK lib:", e)
    exit()

write = sys.stdout.write

IEE_EmoEngineEventCreate = libEDK.IEE_EmoEngineEventCreate
IEE_EmoEngineEventCreate.restype = c_void_p
eEvent = IEE_EmoEngineEventCreate()

IEE_EmoEngineEventGetEmoState = libEDK.IEE_EmoEngineEventGetEmoState
IEE_EmoEngineEventGetEmoState.argtypes = [c_void_p, c_void_p]
IEE_EmoEngineEventGetEmoState.restype = c_int

IEE_EmoStateCreate = libEDK.IEE_EmoStateCreate
IEE_EmoStateCreate.restype = c_void_p
eState = IEE_EmoStateCreate()

IS_GetTimeFromStart = libEDK.IS_GetTimeFromStart
IS_GetTimeFromStart.argtypes = [ctypes.c_void_p]
IS_GetTimeFromStart.restype = c_float

IS_GetWirelessSignalStatus = libEDK.IS_GetWirelessSignalStatus
IS_GetWirelessSignalStatus.restype = c_int
IS_GetWirelessSignalStatus.argtypes = [c_void_p]

IS_FacialExpressionIsBlink = libEDK.IS_FacialExpressionIsBlink
IS_FacialExpressionIsBlink.restype = c_int
IS_FacialExpressionIsBlink.argtypes = [c_void_p]

IS_FacialExpressionIsLeftWink = libEDK.IS_FacialExpressionIsLeftWink
IS_FacialExpressionIsLeftWink.restype = c_int
IS_FacialExpressionIsLeftWink.argtypes = [c_void_p]

IS_FacialExpressionIsRightWink = libEDK.IS_FacialExpressionIsRightWink
IS_FacialExpressionIsRightWink.restype = c_int
IS_FacialExpressionIsRightWink.argtypes = [c_void_p]

IS_FacialExpressionGetUpperFaceAction =  \
    libEDK.IS_FacialExpressionGetUpperFaceAction
IS_FacialExpressionGetUpperFaceAction.restype = c_int
IS_FacialExpressionGetUpperFaceAction.argtypes = [c_void_p]

IS_FacialExpressionGetUpperFaceActionPower = \
    libEDK.IS_FacialExpressionGetUpperFaceActionPower
IS_FacialExpressionGetUpperFaceActionPower.restype = c_float
IS_FacialExpressionGetUpperFaceActionPower.argtypes = [c_void_p]

IS_FacialExpressionGetLowerFaceAction = \
    libEDK.IS_FacialExpressionGetLowerFaceAction
IS_FacialExpressionGetLowerFaceAction.restype = c_int
IS_FacialExpressionGetLowerFaceAction.argtypes = [c_void_p]

IS_FacialExpressionGetLowerFaceActionPower = \
    libEDK.IS_FacialExpressionGetLowerFaceActionPower
IS_FacialExpressionGetLowerFaceActionPower.restype = c_float
IS_FacialExpressionGetLowerFaceActionPower.argtypes = [c_void_p]

IS_FacialExpressionGetEyeLocation = libEDK.IS_FacialExpressionGetEyeLocation
IS_FacialExpressionGetEyeLocation.restype = c_float
IS_FacialExpressionGetEyeLocation.argtype = [c_void_p]

IS_FacialExpressionGetEyelidState = libEDK.IS_FacialExpressionGetEyelidState
IS_FacialExpressionGetEyelidState.restype = c_float
IS_FacialExpressionGetEyelidState.argtype = [c_void_p]

EyeX = c_float(0)
EyeY = c_float(0)
EyeLidLeft = c_float(0)
EyeLidRight = c_float(0)

X = pointer(EyeX)
Y = pointer(EyeY)
Left = pointer(EyeLidLeft)
Right = pointer(EyeLidRight)

#Perfomance metrics Model Parameters /long term excitement not present

RawScore = c_double(0)
MinScale = c_double(0)
MaxScale = c_double(0)

Raw = pointer(RawScore)
Min = pointer(MinScale)
Max = pointer(MaxScale)

alphaValue     = c_double(0)
low_betaValue  = c_double(0)
high_betaValue = c_double(0)
gammaValue     = c_double(0)
thetaValue     = c_double(0)

alpha     = pointer(alphaValue)
low_beta  = pointer(low_betaValue)
high_beta = pointer(high_betaValue)
gamma     = pointer(gammaValue)
theta     = pointer(thetaValue)

channelList = array('I',[3, 7, 9, 12, 16])   # IED_AF3, IED_AF4, IED_T7, IED_T8, IED_Pz 

# short term excitement
IS_PerformanceMetricGetInstantaneousExcitementModelParams = libEDK.IS_PerformanceMetricGetInstantaneousExcitementModelParams
IS_PerformanceMetricGetInstantaneousExcitementModelParams.restype = c_void_p
IS_PerformanceMetricGetInstantaneousExcitementModelParams.argtypes = [c_void_p]

# relaxation
IS_PerformanceMetricGetRelaxationModelParams = libEDK.IS_PerformanceMetricGetRelaxationModelParams
IS_PerformanceMetricGetRelaxationModelParams.restype = c_void_p
IS_PerformanceMetricGetRelaxationModelParams.argtypes = [c_void_p]

# stress
IS_PerformanceMetricGetStressModelParams = libEDK.IS_PerformanceMetricGetStressModelParams
IS_PerformanceMetricGetStressModelParams.restype = c_void_p
IS_PerformanceMetricGetStressModelParams.argtypes = [c_void_p]

# boredom/engagement
IS_PerformanceMetricGetEngagementBoredomModelParams = libEDK.IS_PerformanceMetricGetEngagementBoredomModelParams
IS_PerformanceMetricGetEngagementBoredomModelParams.restype = c_void_p
IS_PerformanceMetricGetEngagementBoredomModelParams.argtypes = [c_void_p]

# interest
IS_PerformanceMetricGetInterestModelParams = libEDK.IS_PerformanceMetricGetInterestModelParams
IS_PerformanceMetricGetInterestModelParams.restype = c_void_p
IS_PerformanceMetricGetInterestModelParams.argtypes = [c_void_p]

# focus
IS_PerformanceMetricGetFocusModelParams = libEDK.IS_PerformanceMetricGetFocusModelParams
IS_PerformanceMetricGetFocusModelParams.restype = c_void_p
IS_PerformanceMetricGetFocusModelParams.argtypes = [c_void_p]

#Perfomance metrics Normalized Scores

# long term excitement
IS_PerformanceMetricGetExcitementLongTermScore = libEDK.IS_PerformanceMetricGetExcitementLongTermScore
IS_PerformanceMetricGetExcitementLongTermScore.restype = c_float
IS_PerformanceMetricGetExcitementLongTermScore.argtypes = [c_void_p]

# short term excitement
IS_PerformanceMetricGetInstantaneousExcitementScore = libEDK.IS_PerformanceMetricGetInstantaneousExcitementScore
IS_PerformanceMetricGetInstantaneousExcitementScore.restype = c_float
IS_PerformanceMetricGetInstantaneousExcitementScore.argtypes = [c_void_p]

# relaxation
IS_PerformanceMetricGetRelaxationScore = libEDK.IS_PerformanceMetricGetRelaxationScore
IS_PerformanceMetricGetRelaxationScore.restype = c_float
IS_PerformanceMetricGetRelaxationScore.argtypes = [c_void_p]

# stress
IS_PerformanceMetricGetStressScore = libEDK.IS_PerformanceMetricGetStressScore
IS_PerformanceMetricGetStressScore.restype = c_float
IS_PerformanceMetricGetStressScore.argtypes = [c_void_p]

# boredom/engagement
IS_PerformanceMetricGetEngagementBoredomScore = libEDK.IS_PerformanceMetricGetEngagementBoredomScore
IS_PerformanceMetricGetEngagementBoredomScore.restype = c_float
IS_PerformanceMetricGetEngagementBoredomScore.argtypes = [c_void_p]

# interest
IS_PerformanceMetricGetInterestScore = libEDK.IS_PerformanceMetricGetInterestScore
IS_PerformanceMetricGetInterestScore.restype = c_float
IS_PerformanceMetricGetInterestScore.argtypes = [c_void_p]

# focus
IS_PerformanceMetricGetFocusScore = libEDK.IS_PerformanceMetricGetFocusScore
IS_PerformanceMetricGetFocusScore.restype = c_float
IS_PerformanceMetricGetFocusScore.argtypes = [c_void_p]

# -------------------------------------------------------------------------

def logEmoState(userID, eState, f):
    print >>f, IS_GetTimeFromStart(eState), ",",
    print >>f, userID.value, ",",
    print >>f, IS_GetWirelessSignalStatus(eState), ",",
    print >>f, IS_FacialExpressionIsBlink(eState), ",",
    print >>f, IS_FacialExpressionIsLeftWink(eState), ",",
    print >>f, IS_FacialExpressionIsRightWink(eState), ",",

    FacialExpressionStates = {}
    FacialExpressionStates[FE_FROWN] = 0
    FacialExpressionStates[FE_SUPPRISE] = 0
    FacialExpressionStates[FE_SMILE] = 0
    FacialExpressionStates[FE_CLENCH] = 0

    upperFaceAction = IS_FacialExpressionGetUpperFaceAction(eState)
    upperFacePower = IS_FacialExpressionGetUpperFaceActionPower(eState)
    lowerFaceAction = IS_FacialExpressionGetLowerFaceAction(eState)
    lowerFacePower = IS_FacialExpressionGetLowerFaceActionPower(eState)
    FacialExpressionStates[upperFaceAction] = upperFacePower
    FacialExpressionStates[lowerFaceAction] = lowerFacePower

    print >>f, FacialExpressionStates[FE_SUPPRISE], ",",
    print >>f, FacialExpressionStates[FE_FROWN], ",",
    print >>f, FacialExpressionStates[FE_SMILE], ",",
    print >>f, FacialExpressionStates[FE_CLENCH], ",",

    IS_FacialExpressionGetEyeLocation(eState,X,Y)
    print >>f, EyeX.value, ",",
    print >>f, EyeY.value, ",",
    IS_FacialExpressionGetEyelidState(eState,Left,Right)
    print >>f, EyeLidLeft.value, ",",
    print >>f, EyeLidRight.value, ",",

    # Performance metrics Suite results
    print >>f, IS_PerformanceMetricGetExcitementLongTermScore(eState), ",",
    print >>f, IS_PerformanceMetricGetInstantaneousExcitementScore(eState), ",",    
    IS_PerformanceMetricGetInstantaneousExcitementModelParams(eState, Raw, Min, Max)
    print >>f, RawScore.value, ",",
    print >>f, MinScale.value, ",",
    print >>f, MaxScale.value, ",",
    print >>f, IS_PerformanceMetricGetRelaxationScore(eState), ",",
    IS_PerformanceMetricGetRelaxationModelParams(eState, Raw, Min, Max)
    print >>f, RawScore.value, ",",
    print >>f, MinScale.value, ",",
    print >>f, MaxScale.value, ",",
    print >>f, IS_PerformanceMetricGetStressScore(eState), ",",
    IS_PerformanceMetricGetStressModelParams(eState, Raw, Min, Max)

    print >>f, RawScore.value, ",",
    print >>f, MinScale.value, ",",
    print >>f, MaxScale.value, ",",
    print >>f, IS_PerformanceMetricGetEngagementBoredomScore(eState), ",",
    IS_PerformanceMetricGetEngagementBoredomModelParams(eState, Raw, Min, Max)
    print >>f, RawScore.value, ",",
    print >>f, MinScale.value, ",",
    print >>f, MaxScale.value, ",",
    print >>f, IS_PerformanceMetricGetInterestScore(eState), ",",
    IS_PerformanceMetricGetInterestModelParams(eState, Raw, Min, Max)
    print >>f, RawScore.value, ",",
    print >>f, MinScale.value, ",",
    print >>f, MaxScale.value, ",",
    print >>f, IS_PerformanceMetricGetFocusScore(eState), ",",
    IS_PerformanceMetricGetFocusModelParams(eState, Raw, Min, Max)
    print >>f, RawScore.value, ",",
    print >>f, MinScale.value, ",",
    print >>f, MaxScale.value, ",",
    
    count = 0
    for i in channelList:
        count += 1
        result = c_int(0)
        result = libEDK.IEE_GetAverageBandPowers(userID, i, theta, alpha, low_beta, high_beta, gamma)
        if result == 0:    #EDK_OK
            print >>f, thetaValue.value, ",",
            print >>f, alphaValue.value, ",",
            print >>f, low_betaValue.value, ",",
            print >>f, high_betaValue.value, ",",
            print >>f, gammaValue.value, "," if (count < len(channelList)) else "",
        else:
            print >>f, 0, ",",
            print >>f, 0, ",",
            print >>f, 0, ",",
            print >>f, 0, ",",
            print >>f, 0, "," if (count < len(channelList)) else "",
    
    print >>f, '\n',
    
def kbhit():
    ''' Returns True if keyboard character was hit, False otherwise.
    '''
    if sys.platform.startswith('win32'):
        return msvcrt.kbhit()   
    else:
        dr,dw,de = select([sys.stdin], [], [], 0)
        return dr != []


# -------------------------------------------------------------------------

userID = c_uint(0)
user   = pointer(userID)
option = c_int(0)
state  = c_int(0)
ready  = 0

composerPort = c_uint(1726)
timestamp    = c_float(0.0)

FE_SUPPRISE = 0x0020 
FE_FROWN    = 0x0040
FE_SMILE    = 0x0080
FE_CLENCH   = 0x0100

PM_EXCITEMENT = 0x0001,
PM_RELAXATION = 0x0002,
PM_STRESS     = 0x0004,
PM_ENGAGEMENT = 0x0008,

PM_INTEREST   = 0x0010,
PM_FOCUS      = 0x0020

# -------------------------------------------------------------------------
header = ['Time', 'UserID', 'Wireless Signal Status',
          'Blink', 'Wink Left', 'Wink Right',
          'Surprise', 'Furrow', 'Smile', 'Clench',
          'EyeLocationHoriz', 'EyeLocationVert','EyelidStateLeft', 'EyelidStateRight',
          'LongTermExcitementRawNorm',
          'ShortTermExcitementRawNorm','ShortTermExcitementRaw', 'ShortTermExcitementMin', 'ShortTermExcitementMax',
          'RelaxationRawNorm','RelaxationRaw','RelaxationMin','RelaxationMax',
          'StressRawNorm','StressRaw','StressMin','StressMax',
          'EngagementRawNorm','EngagementRaw', 'EngagementMin','EngagementMax',
          'InterestRawNorm','InterestRaw', 'InterestMin', 'InterestMax',
          'FocusRawNorm','FocusRaw','FocusMin','FocusMax',
          'AF3_theta', 'AF3_alpha', 'AF3_low_beta', 'AF3_high_beta', 'AF3_gamma',
          'T7_theta', 'T7_alpha', 'T7_low_beta', 'T7_high_beta', 'T7_gamma',
          'Pz_theta', 'Pz_alpha', 'Pz_low_beta', 'Pz_high_beta', 'Pz_gamma',
          'T8_theta', 'T8_alpha', 'T8_low_beta', 'T8_high_beta', 'T8_gamma',
          'AF4_theta', 'AF4_alpha', 'AF4_low_beta', 'AF4_high_beta', 'AF4_gamma']


print ("===================================================================")
print ("Example to convert from eeg edf data file to detections and fft at csv file.")
print ("===================================================================")


logger = multiprocessing.log_to_stderr(logging.INFO)
input_list = [];
result = []
def on_return(retval):
    result.append(retval)

def start_process():
    print 'Starting', multiprocessing.current_process().name

def edf_to_detect(input_dir, output_dir):

    print ("edf_to_detect...\n")

    #input_name_lists
    for input_name in os.listdir(input_dir):
        if input_name.endswith(".edf"):
            input_list.append(input_name)
    #create process
    pool_size = multiprocessing.cpu_count() * 1 -1
    print ("pool size %d" %(pool_size))
    pool = multiprocessing.Pool(processes=pool_size,
                                initializer=start_process,
                                )
                                
    for input in input_list:
        pool_outputs = pool.apply_async(emostate_fft,(input,input_dir,output_dir,), callback = on_return)
        
    pool.close() # no more tasks
    pool.join()  # wrap up current tasks
    logger.info(result)
    
    libEDK.IEE_EmoStateFree(eState)
    libEDK.IEE_EmoEngineEventFree(eEvent)
    
    print("Reproduce detection and fft output from edf completeted")
    return;
    
def emostate_fft(input_name, input_dir, output_dir):
    print ("emostate_fft...\n")
    print("input_name %s" %(input_name))

    out_name =  "target.csv"
    if output_dir == '':
        output_file = os.path.join(input_dir, out_name)
    else:
        # out_name =  os.path.splitext(input_name)[0] + ".csv"
        out_name =  "latest.csv"
        output_file = os.path.join(output_dir, out_name)
    print("output_file %s" %(output_file))
    
    input_file = os.path.join(input_dir, input_name).strip()
    print ("input file %s" % (input_file))

    
    if libEDK.IEE_EngineLocalConnect(input_file,"") != 0:
        print 'Emotiv Engine with EDF file start up failed.'
        return "Connect failed"
    print 'Engine connect succesfully'
    libEDK.IEE_EdfStart()

    f = file(output_file, 'w+')
    f = open(output_file, 'w+')
    print >> f, ', '.join(header)
    state_check = 0
    while (1):
        if kbhit():
            break
        state = libEDK.IEE_EngineGetNextEvent(eEvent)
        print("state %d \n" %(state))
        if state == 0:
            state_check = 0 #check state
            eventType = libEDK.IEE_EmoEngineEventGetType(eEvent)
            libEDK.IEE_EmoEngineEventGetUserId(eEvent, user)
            
            if eventType == 16:  # libEDK.IEE_Event_enum.IEE_UserAdded
                ready = 1
                libEDK.IEE_FFTSetWindowingType(userID, 1) # 1: libEDK.IEE_WindowingTypes_enum.IEE_HAMMING
                print "User added"
            if ready == 1:
                if eventType == 64:  # libEDK.IEE_Event_enum.IEE_EmoStateUpdated
                    libEDK.IEE_EmoEngineEventGetEmoState(eEvent, eState)
                    timestamp = IS_GetTimeFromStart(eState)
                    
                    logEmoState(userID, eState, f)
        elif state == 0x0600:
            state_check = state_check + 1
            # print("state_check %d \n" %(state_check))
            if(state_check == 20):
                break
        elif state != 0x0600:
            print ("Internal error in Emotiv Engine ! ")
            break
        time.sleep(0.05)
        
    f.close()
    libEDK.IEE_EngineDisconnect()
    if state_check == 20:
        return out_name  #return output if convert succesfully
    else:
        return input_name #return input if convert unsuccesfully

def main(argv):
# Show options
# -h : help otion 
# -f <input_file_dir>           = Input edf files directory Eg: C:\edf\testdata.edf\
# -d <detection_output_dir>     = Output files directory  , Default is input file directory
    input_file_dir = ''
    dectection_dir = ''
    try:
        opts, args = getopt.getopt(argv,"hf:d:",["ifile=","dfile="])
    except getopt.GetoptError:
        print 'edf_to_detection_csv.py -f <input_file_dir> -d <detection_output_dir>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'edf_to_detection_csv.py -f <input_file_dir> -d <detection_output_dir>'
            print 'Options \n'
            print ' -f <input_file_dir>         = Input edf files directory Eg: C:\\edf\\testdata.edf\ \n'
            print ' -d <detection_output_dir>   = Output files directory . Default is input file directory \n'
            sys.exit()
        elif opt in ("-f", "--ifile"):
            input_file_dir = arg
        elif opt in ("-d", "--dfile"):
            dectection_dir = arg
    print 'Input directory directory  is ', input_file_dir
    print 'Detection directory is ', dectection_dir

    #input edf file
    if input_file_dir != '':
        #call edf to detection output
        edf_to_detect(input_file_dir, dectection_dir)
    else:
        #input from headset
        print 'edf_to_detection_csv.py -f <input_file_dir> -d <detection_output_dir>'
if __name__ == "__main__":
    main(sys.argv[1:])
