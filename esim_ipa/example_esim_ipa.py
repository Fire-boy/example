# Copyright (c) Quectel Wireless Solution, Co., Ltd.All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import net
from sim import esim as ESIM
import sim
import utime
import _thread
from queue import Queue

class Enum:
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __repr__(self):
        return self.name



class EVENT(Enum):

    EVENT_ENABLE_DISABLE_UNINSTALL_PROFILE         = 1
    EVENT_QUERY_PROFILE                            = 2
    EVENT_SET_NICKNAME                             = 3
    EVENT_QUERY_EID                                = 4
    EVENT_NOTIFY_INFO                              = 6
    EVENT_GET_DEL_REP_NOTIFY                       = 7
    EVENT_INSTALL_PROFILE                          = 10
    EVENT_LPA_VERSION                              = 11
    EVENT_COM_TIME                                 = 12
    EVENT_IPA_VERSION                              = 13 
    EVENT_SET_LOOP_TIME                            = 14 
    EVENT_GET_EIM                                  = 15
    EVENT_UPDATE_ADD_EIM                           = 16
    EVENT_DEL_EIM                                  = 17
    EVENT_GET_PRO                                  = 18


class  esim_class():

    def __init__(self,lpa=None):
        self.lpa_url = lpa
        self.event_map_func = {
            EVENT.EVENT_ENABLE_DISABLE_UNINSTALL_PROFILE:   self.esim_enable_disable_uninstall_profile,
            EVENT.EVENT_QUERY_PROFILE:                      self.esim_query_profile,
            EVENT.EVENT_SET_NICKNAME:                       self.esim_set_nickname,
            EVENT.EVENT_QUERY_EID:                          self.esim_query_eid,
            EVENT.EVENT_NOTIFY_INFO:                        self.esim_notify_info,
            EVENT.EVENT_GET_DEL_REP_NOTIFY:                 self.esim_get_del_rep_notify,
            EVENT.EVENT_INSTALL_PROFILE:                    self.esim_install_profile,
            EVENT.EVENT_LPA_VERSION:                        self.esim_lpa_version,
            EVENT.EVENT_COM_TIME:                           self.esim_compile_time,
            EVENT.EVENT_IPA_VERSION:                        self.esim_ipa_version,
            EVENT.EVENT_SET_LOOP_TIME:                      self.esim_set_loop_time,
            EVENT.EVENT_GET_EIM:                            self.esim_get_eim,
            EVENT.EVENT_UPDATE_ADD_EIM:                     self.esim_update_add_eim,
            EVENT.EVENT_DEL_EIM:                            self.esim_del_eim,
            EVENT.EVENT_GET_PRO:                            self.esim_get_pro
        }
        self.event_queue        = Queue()
        self.esim_is_running    = True
        self.esim = ESIM
        self.esim.init(1)
        self.esim.setCallback(self.esim_call_back)
        self.esim_function_run  = False

    def esim_call_back(self,args):
        self.esim_log("esim_call_back get {}".format(args))
        self.event_queue.put(args)

    def esim_set_run(self,is_run):
        self.esim_is_running    = is_run

    def esim_log(self,args):
        print("ESIM: {}\n".format(args))

    def esim_enable_disable_uninstall_profile(self,args):
        self.esim_log("args {}".format(args))
        if args[2] == 0 or args[2] == 1:
            utime.sleep(1)
            net.setModemFun(0)
            utime.sleep(1)
            net.setModemFun(1)
        self.esim_function_run = False

    def esim_query_profile(self,args):
        self.esim_log("args {}".format(args))
        self.esim_function_run = False

    def esim_set_nickname(self,args):
        self.esim_log("args {}".format(args))
        self.esim_function_run = False

    def esim_query_eid(self,args):
        self.esim_log("args {}".format(args))
        self.esim_function_run = False

    def esim_notify_info(self,args):
        self.esim_log("args {}".format(args))
        self.esim_function_run = False

    def esim_get_del_rep_notify(self,args):
        self.esim_log("args {}".format(args))
        self.esim_function_run = False

    def esim_install_profile(self,args):
        self.esim_log("args {}".format(args))
        self.esim_function_run = False

    def esim_lpa_version(self,args):
        self.esim_log("args {}".format(args))
        self.esim_function_run = False

    def esim_compile_time(self,args):
        self.esim_log("args {}".format(args))
        self.esim_function_run = False

    def esim_ipa_version(self,args):
        self.esim_log("args {}".format(args))
        self.esim_function_run = False

    def esim_set_loop_time(self,args):
        self.esim_log("args {}".format(args))
        self.esim_function_run = False

    def esim_get_eim(self,args):
        self.esim_log("args {}".format(args))
        self.esim_function_run = False

    def esim_update_add_eim(self,args):
        self.esim_log("args {}".format(args))
        self.esim_function_run = False

    def esim_del_eim(self,args):
        self.esim_log("args {}".format(args))
        self.esim_function_run = False

    def esim_get_pro(self,args):
        self.esim_log("args {}".format(args))
        self.esim_function_run = False

    def esim_check_event(self,eventid):
        if eventid in self.event_map_func:
            return True
        else:
            return False

    def esim_deal_esim_calback_event(self,args):

           while self.esim_is_running:
                data = self.event_queue.get()
                #self.esim_log("esim_deal_esim_calback_event get {}".format(data))
                if self.esim_check_event(data[0]):
                    self.event_map_func[data[0]](data)
                else:
                    self.esim_log("this event id is invalied {}".format(data))

    def esim_get_id(self):
        if self.esim_function_run:
            return False
        ret = self.esim.get_eid()
        if ret == 0:
            self.esim_function_run = True
            return True
        else:
            return False

    def esim_get_profile(self):
        if self.esim_function_run:
            return False
        ret = self.esim.lpa_get_profile(0)
        if ret == 0:
            self.esim_function_run = True
            return True
        else:
            return False

    def esim_enable_profile(self,iccid):
        if self.esim_function_run:
            return False
        ret = self.esim.lpa_enable_profile(iccid)
        if ret == 0:
            self.esim_function_run = True
            return True
        else:
            return False

    def esim_disable_profile(self,iccid):
        if self.esim_function_run:
            return False
        ret = self.esim.lpa_disable_profile(iccid)
        if ret == 0:
            self.esim_function_run = True
            return True
        else:
            return False

    def esim_delete_profile(self,iccid):
        if self.esim_function_run:
            return False
        ret = self.esim.lpa_uninstall_profile(iccid)
        if ret == 0:
            self.esim_function_run = True
            return True
        else:
            return False

    def esim_download_profile(self,url=None):
        if self.esim_function_run:
            return False
        ret = self.esim.lpa_install_profile(0,url,'')
        if ret == 0:
            self.esim_function_run = True
            return True
        else:
            return False

    def esim_query_notify(self):
        if self.esim_function_run:
            return False
        ret = self.esim.lpa_query_notification(0)
        if ret == 0:
            self.esim_function_run = True
            return True
        else:
            return False

    def esim_report_notify(self,seq):
        if self.esim_function_run:
            return False
        ret = self.esim.lpa_report_notification(seq)
        if ret == 0:
            self.esim_function_run = True
            return True
        else:
            return False

esim_obj = esim_class()

if __name__ == '__main__':

    _thread.start_new_thread(esim_obj.esim_deal_esim_calback_event, ([1]))
    '''
    iloop = 0
    while True:
        utime.sleep(1)
        print("will exec iloop :{}".format(iloop))
        if iloop == 0:
            #query eid
            if esim_obj.esim_get_id() == True:
                iloop = iloop + 1
        elif iloop == 1:
            #query profile 
            if esim_obj.esim_get_profile() == True:
                iloop = iloop + 1
        elif iloop == 2:
            #query profile 
           if  esim_obj.esim_get_profile() == True:
                iloop = iloop + 1
        elif iloop == 3:
            #enable profile 
            if esim_obj.esim_enable_profile("实际的") == True:
                iloop = iloop + 1
        elif iloop == 4:
            #disable profile 
            if esim_obj.esim_disable_profile("实际的") == True:
                iloop = iloop + 1
        elif iloop == 5:
            #delete profile 
            #don't delete iccid  because this is example,
            #if esim_obj.esim_delete_profile("实际的") == True:
            #    iloop = iloop + 1
            iloop = iloop + 1
        elif iloop == 6:
            #query  notify 
            if esim_obj.esim_query_notify() == True:
                iloop = iloop + 1
        elif iloop == 7:
            #report delete profile agin
            # if need
            #esim_obj.esim_report_notify(seq)

            #if need
            #download profile
            if esim_obj.esim_download_profile("实际的AC码") == True:
                iloop = iloop + 1
        else:
            break
    '''
    print("end")

