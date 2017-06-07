# -*- coding: utf-8 -*- {{{
# vim: set fenc=utf-8 ft=python sw=4 ts=4 sts=4 et:
"""
Copyright (c) 2015, Battelle Memorial Institute
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

The views and conclusions contained in the software and documentation are those
of the authors and should not be interpreted as representing official policies,
either expressed or implied, of the FreeBSD Project.
'''
'''
This material was prepared as an account of work sponsored by an
agency of the United States Government.  Neither the United States
Government nor the United States Department of Energy, nor Battelle,
nor any of their employees, nor any jurisdiction or organization
that has cooperated in the development of these materials, makes
any warranty, express or implied, or assumes any legal liability
or responsibility for the accuracy, completeness, or usefulness or
any information, apparatus, product, software, or process disclosed
or represents that its use would not infringe privately owned rights.

Reference herein to any specific commercial product, process, or
service by trade name, trademark, manufacturer, or otherwise does
not necessarily constitute or imply its endorsement, recommendation,
r favoring by the United States Government or any agency thereof,
or Battelle Memorial Institute. The views and opinions of authors
expressed herein do not necessarily state or reflect those of the
United States Government or any agency thereof.

PACIFIC NORTHWEST NATIONAL LABORATORY
operated by BATTELLE for the UNITED STATES DEPARTMENT OF ENERGY
under Contract DE-AC05-76RL01830
"""
import logging
import sys
from datetime import timedelta as td, datetime as dt
from dateutil import parser
import numpy as np
from volttron.platform.messaging import headers as headers_mod, topics
from volttron.platform.agent.utils import (jsonapi, setup_logging,
                                           format_timestamp, get_aware_utc_now)
from volttron.platform.vip.agent import Agent, Core
from volttron.platform.agent import utils
from datetime import datetime
import pytz
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import subprocess
import sys
import os
import time
from os.path import expanduser
home = expanduser("~")


utc=pytz.UTC

fn = home +'/stpt.txt'



fpy = home+'/volttron/DmsBms/control_agent/plot.py'



setup_logging()
_log = logging.getLogger(__name__)
logging.basicConfig(level=logging.debug,
                    format='%(asctime)s   %(levelname)-8s %(message)s',
                    datefmt='%m-%d-%y %H:%M:%S')

DATE_FORMAT = '%m-%d-%Y %H:%M:%S'

class Controlagent(Agent):
    def __init__(self, config_path, **kwargs):
        super(Controlagent, self).__init__(**kwargs)

#       read the information from the configh files


        config = utils.load_config(config_path)

        device_path = dict((key, config[key])
                           for key in ['campus', 'building', 'unit'])
        self.device = '{campus}/{building}'.format(**device_path)

        _log.debug('Work on device: {}'.format(self.device))
        self.device_topic = topics.DEVICES_VALUE(point='all', path='', **device_path)



        self.agent_id = config.get('agentid')
        self.participate = config.get('participate')
        _log.debug('Participate status: {}'.format(self.participate))
        points = config.get('points')
        points = config.get('points')


        self.points=points.values()
        _log.debug('Control point list: {}'.format(self.points))

        self.subscribing_topic=config.get('signal_topic')
        self.reservation_topic=config.get('reservation_topic')
        self.power_topic=config.get('power_topic')
        self.response_topic=config.get('response_topic')
        self.curtail_value=config.get('curtail_value')
        _log.debug('Curtail value: {}'.format(self.curtail_value))

        self.curtail=0
        self.control_variable=config.get('control_variable')
        self.count=0
        self.event_start=[]
        self.event_end=[]
        self.signal_time=[]
        self.default=[]
        if os.path.isfile(fn):
                 os.remove(fn) 
        self.s=1   
        f=open(fn,'a')

        f.close()



    @Core.receiver('onsetup')
    def setup(self, sender, **kwargs):
        self.is_running = True

    @Core.receiver('onstart')
    def starting_base(self, sender, **kwargs):
        _log.debug('Subscribing to '+self.subscribing_topic)
        self.vip.pubsub.subscribe(peer='pubsub',
                                  prefix=self.subscribing_topic,
                                  callback=self.on_new_signal)
        _log.debug('Subscribing to '+self.reservation_topic)
        self.vip.pubsub.subscribe(peer='pubsub',
                                  prefix=self.reservation_topic,
                                  callback=self.on_new_reservation)
        _log.debug('Subscribing to '+self.power_topic)
        self.vip.pubsub.subscribe(peer='pubsub',
                                  prefix=self.power_topic,
                                  callback=self.on_new_data) 
        pid = subprocess.Popen([sys.executable,fpy])







    def on_new_signal(self, peer, sender, bus, topic, headers, message):
        '''Subscribe to device data from message bus
        '''
        _log.debug('Received one request ')
        info = {}
        for key, value in message[0].items():
            info[key.lower()] = value
        
        signal_type=info['messagetype']
        startDateTime=info['eventstartdatetime']        
        duration=info['eventduration']     
        modificationNumber=info['modificationnumber']
        EventID=info['eventid']
                    
        self.start= datetime.utcnow()
        if signal_type.find('notification')!=-1:
                   _log.info('Receieve the event response for timestamp: {}.'.format(startDateTime))
                   if self.participate.lower().find('true')!=-1:
                            start=utc.localize(dt.strptime(startDateTime,DATE_FORMAT))                   
                            self.event_start.append(start)
                            end=start+td(minutes=float(duration)/60)
                            self.event_end.append(end)
                            _log.info('Event start from: {}.'.format(start))
                            _log.info('Event end at: {}.'.format(end))
                            self.send_participation_yes(EventID,modificationNumber,start.isoformat(' ') + 'Z',duration)
        

                   else:
                            _log.info('donnot participate in the event response for timestamp: {}.'.format(startDateTime))                           
                            self.send_participation_no(EventID,modificationNumber) 
        if len(self.default)<1:
                           _log.info('default values for set points are required') 
                           return
        else:
                           self.building_control()   


    def on_new_reservation(self, peer, sender, bus, topic, headers, message):
        '''Subscribe to device data from message bus
        '''
        _log.debug('Received one reservation ')
        info = {}
        for key, value in message[0].items():
            info[key.lower()] = value
        
        reservation_time=info['reservation']
        self.signal_time.append(reservation_time)
                    


    def send_participation_yes(self,eventID,modificationNumber,eventDateTime,parDuration):
        message={}
        message.update({'eventID':eventID})
        message.update({'modificationNumber':modificationNumber}) 
        message.update({'responseIndicator':True})

        now = datetime.utcnow().isoformat(' ') + 'Z'
        
        headers = {headers_mod.DATE: now, headers_mod.TIMESTAMP: now}
        
        message.update({'createdDateTime':now})
        message.update({'eventDateTime':eventDateTime})
        message.update({'responseAction':"curtail load"})
        message.update({'Participation':True})
        message.update({'parDuration':parDuration})
        message.update({'powerResponseType':'none'})
        item={}
        item['eventID']= {'units': 'none', 'type': 'str', 'tz': 'US/Pacific'}
        item['modificationNumber']= {'units': 'none', 'type': 'str', 'tz': 'US/Pacific'}
        item['responseIndicator']= {'units': 'none', 'type': 'boolean', 'tz': 'US/Pacific'}
        item['createdDateTime']= {'units': 'datetime', 'type': 'datetime', 'tz': 'US/Pacific'}
        item['eventDateTime']= {'units': 'datetime', 'type': 'datetime', 'tz': 'US/Pacific'}    
        item['responseAction']= {'units': 'none', 'type': 'str', 'tz': 'US/Pacific'}  
        item['Participation']= {'units': 'none', 'type': 'boolean', 'tz': 'US/Pacific'}
        item['parDuration']= {'units': 'seconds', 'type': 'float', 'tz': 'US/Pacific'}
        item['powerResponseType']= {'units': 'none', 'type': 'str', 'tz': 'US/Pacific'}
        message=[message , item]     
        self.vip.pubsub.publish('pubsub', self.response_topic, headers, message).get()
  
            
    def send_participation_no(self,eventID,modificationNumber):
        message={}
        message.update({'eventID':eventID})
        message.update({'modificationNumber':modificationNumber}) 
        message.update({'responseIndicatorr':True})
        now = dt.utcnow().isoformat(' ') + 'Z'
        headers = {headers_mod.DATE: now, headers_mod.TIMESTAMP: now}
        item={}
        message.update({'createdDateTime':now})
        message.update({'Participation':False})
        item['eventID']={'units': 'none', 'type': 'str', 'tz': 'US/Pacific'}
        item['modificationNumber']= {'units': 'none', 'type': 'str', 'tz': 'US/Pacific'}
        item['responseIndicator']= {'units': 'none', 'type': 'boolean', 'tz': 'US/Pacific'}
        item['createdDateTime']= {'units': 'datetime', 'type': 'datetime', 'tz': 'US/Pacific'}
        item['Participation']={'units': 'none', 'type': 'boolean', 'tz': 'US/Pacific'}
        message=[message , item]

        self.vip.pubsub.publish('pubsub', self.response_topic, headers, message).get()



    def on_new_data(self, peer, sender, bus, topic, headers, message):
        '''Subscribe to device data from message bus

        '''  
 
        data = {}
        for key, value in message[0].items():
            data[key.lower()] = value
    

        current_time = parser.parse(headers.get('Date'))



    
        f=open(fn,'a')

        f.writelines(str(current_time).replace(' ','T')+',')
        for i in range(len(self.points)):
                  
                stpt=data.get(str(self.points[i]+'_'+self.control_variable).lower())
                f.writelines(str(stpt)+',')   
        power= data.get('totalelectricdemandpower')
        f.writelines(str(power)+'\n')   
        f.close()
        
        self.s=self.s+1
        _log.info('Receieve the builiding response for timetamp: {}.'.format(current_time)) 
        if self.count<1:
              
              for i in range(len(self.points)):
   
                   old_control_value= data.get(str(self.points[i]+'_'+self.control_variable).lower())
                   self.default.append(old_control_value)  

        self.count=self.count+1

        if len(self.event_start)>0: 
               for k in range(len(self.event_start)):
                         if current_time>self.event_start[k]-td(minutes=2) and current_time<self.event_end[k]:
                                         self.curtail=self.curtail_value
                                         _log.info('curtailment: {}'.format(current_time))
                                         break
 
                         self.curtail=0 

        temp=True
        if len(self.signal_time)>0:                  
               for k in range(len(self.signal_time)):
                         if current_time==utc.localize(dt.strptime(self.signal_time[k],DATE_FORMAT))-td(minutes=1):
                                         _log.info('waiting for information: {}'.format(self.signal_time[k]))
                                         temp=False 
                                         break
                         temp=True 
        if temp:
               self.building_control() 

          



    def building_control(self):

        _now = dt.now()
        str_now = _now.strftime(DATE_FORMAT)
        _end = _now + td(minutes=4)
        str_end = _end.strftime(DATE_FORMAT)

        _log.debug('device: ' + str(self.device))
        # create schedule message for actuator.
        schedule_request = [[self.device, str_now, str_end]]
        # do schedule rpc call.  
        result = self.vip.rpc.call('platform.actuator', 'request_new_schedule', self.agent_id, 'mytask', 'HIGH', schedule_request).get(timeout=20)
        # check result status.
        if result['result'] == 'SUCCESS':
               _log.debug('Lock success.')
        if result['result'] == 'FAILURE':
               cancel_result = self.vip.rpc.call('platform.actuator', 'request_cancel_schedule', self.agent_id, 'mytask').get(timeout=10)

        for i in range(len(self.points)):    
        
               new_control_value=self.vip.rpc.call('platform.actuator', 'set_point', self.agent_id, str(self.device)+'/'+self.points[i]+'/'+self.control_variable,self.default[i]+self.curtail).get(timeout=15)

               _log.debug("new set point for" + self.points[i]+" : "+str(self.default[i]+self.curtail))       


def main():
    '''Main method called by the eggsecutable.'''
    utils.vip_main(Controlagent)
 


if __name__ == '__main__':
    # Entry point for script
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        pass

