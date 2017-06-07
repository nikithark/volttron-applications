import os

idf_file=raw_input("please input the name of the idf file (without extension) ")

wea_name=raw_input("please input the name of the weather data file (without extension) ")

wea_file_path=raw_input("please input the path of the weather data file (e.g. /home/user/eplus)  ")

bcvtb_file_path=raw_input("please input the path of the bcvtb data file (e.g. /home/user/eplus)  ")

eplus_path=raw_input("please input the path for the energyplus model (e.g. /home/user/eplus) ")



f=open(idf_file+'.idf','r')

lines=f.readlines()
f.close()


for i in range(len(lines)):
       if lines[i].lower().find('building,')!=-1:

	              if len(lines[i].split(','))>2: 
                              building=lines[i].split(',')[1].replace(' ','').replace('\n','')				  
	              elif lines[i].find('!')==-1:

                              building=lines[i+1].split(',')[0].replace(' ','').replace('\n','')	
	              break
print building

# identify the zones

sch=[]
zone=[]

for i in range(len(lines)):
    if lines[i].find('ZoneControl:Thermostat,')!=-1:
	
	        index=i+1
	        num=0
	        while lines[index].find(';')==-1:
			       index=index+1
			       num=num+1
	        if num>5:
			               print "complicated control detected"+lines[i+5].split(' ')[0]
	        else:			   	
			               sch.append(lines[i+5].split(';')[0].replace('    ',''))
			               zone.append(lines[i+2].split(',')[0].replace('    ',''))

# identify the existing schedules
						   
sch_adjl=[]						   
line_sch=[]						   
sch_al=[]
zone_al=[]						   
for i in range(len(lines)):
        for j in range(len(sch)):
		        if lines[i].find(' '+sch[j]+',')!=-1:
						    if lines[i-1].find('Dual')!=-1:
                                                     line_sch.append(i+2)
                                                     sch_temp=lines[i+2].split(';')[0].replace('    ','')
                                                     sch_al.append(sch_temp)
                                                     zone_al.append(zone[j])
                                                     sch_adjl.append(sch[j])
													 
						    elif lines[i-1].find('Cooling')!=-1:
													 line_sch.append(i+1)
													 sch_temp=lines[i+1].split(';')[0].replace('    ','')
													 sch_al.append(sch_temp)
													 zone_al.append(zone[j])
													 sch_adjl.append(sch[j])



													 
sch_av=[]  
sch_adj=[]
zone_av=[]

sch_av_ems=[]  
sch_adj_ems=[]
zone_av_ems=[]

for i in range(len(sch_al)):
       for j in range(len(lines)):
                    if lines[j].lower().find(sch_al[i].lower()+',')!=-1 and (lines[j].find('Actuated')!=-1 or lines[j][0]=='!'):
					                                       print lines[j] 
					                                       temp=True
					                                       break
                    temp=False
       if  temp==False:
                    sch_av.append(sch_al[i])
                    sch_adj.append(sch_adjl[i])
                    zone_av.append(zone_al[i])
					
       if  temp==True:
                    sch_av_ems.append(sch_al[i])
                    sch_adj_ems.append(sch_adjl[i])
                    zone_av_ems.append(zone_al[i])					
                    													
print sch_adj_ems 

# disable the existing schedules
default=[]

for j in range(len(sch_av)): 
        for i in range(len(lines)):        
                    if lines[i].lower().find(' '+sch_av[j].lower()+',')!=-1:
					        print lines[i]
#					        if  lines[i].find('!    ')==-1:
#					                lines[i-1]='!'+lines[i-1]
#					                lines[i]='!'+lines[i]
					                
					        index=i+1
					        while lines[index].find(';')==-1:
#							                      if lines[index].find('!    ')==-1:
#                                                                                  lines[index]='!'+lines[index]
							                      index=index+1
#					        if lines[index].find(';')!=-1 and lines[index].find('!    ')==-1:
#                                                  lines[index]='!'+lines[index]
					        stpt=[]
							
					        for k in range(i+1,index+1):
							                if lines[k].find(',')!=-1 and lines[k].find(';')==-1: 
                                                                            if len(lines[k].split(','))>2:
																			                  text=lines[k].split(',')[1].replace(' ','')
                                                                            else:
																			                  text=lines[k].split(',')[0].replace(' ','').replace('!','')
							                elif lines[k].find(';')!=-1 and lines[k].find(',')==-1:
                                                                            text=lines[k].split(';')[0].replace(' ','').replace('!','').replace(' ','')
							                elif lines[k].find(';')!=-1 and lines[k].find(',')!=-1:
                                                                            text=lines[k].split(',')[1].split(';')[0].replace(' ','')
                                                         											
										
							                if text.replace(".", "", 1).isdigit():
									                                      stpt.append(float(text))
#					        print stpt											  
					        default.append(min(stpt))
					        break



								 							
# add new zone control       
heat_sch=[]
sch_type=[]
control_type=[]

heat_sch_ems=[]
sch_type_ems=[]
control_type_ems=[]

for i in range(len(lines)):
    for j in range(len(sch_adj)):
            if lines[i].find(' '+sch_adj[j]+';')!=-1:
					        if  lines[i].find('!    ')==-1:
					                lines[i]='!'+lines[i]
					        index=i-1
					        while lines[index].find('ZoneControl:Thermostat')==-1:
							                      if lines[index].find('!    ')==-1:
                                                                                  lines[index]='!'+lines[index]
							                      index=index-1
					        if lines[index].find('ZoneControl:Thermostat')!=-1 and lines[index].find('!')==-1:
                                                  lines[index]='!'+lines[index]	
					        control_type.append(lines[i-2])
			
			
            if lines[i].find(' '+sch_adj[j]+',')!=-1:
					        if  lines[i].find('!    ')==-1:
					                lines[i-1]='!'+lines[i-1]
					                lines[i]='!'+lines[i]
					        index=i+1
					        while lines[index].find(';')==-1:
							                      if lines[index].find('!    ')==-1:
                                                                                  lines[index]='!'+lines[index]
							                      index=index+1
					        if lines[index].find(';')!=-1 and lines[index].find('!    ')==-1:
                                                  lines[index]='!'+lines[index]	
					        if index>i+1:
                                                 heat_sch.append(lines[i+1].replace('!    ','    '))
					        else:
                                                 heat_sch.append(None)
					        sch_type.append(lines[i-1].replace('!',''))	
    for j in range(len(sch_adj_ems)):							

            if lines[i].find(' '+sch_adj_ems[j]+';')!=-1:
					        if  lines[i].find('!    ')==-1:
					                lines[i]='!'+lines[i]
					        index=i-1
					        while lines[index].find('ZoneControl:Thermostat')==-1:
							                      if lines[index].find('!    ')==-1:
                                                                                  lines[index]='!'+lines[index]
							                      index=index-1
					        if lines[index].find('ZoneControl:Thermostat')!=-1 and lines[index].find('!')==-1:
                                                  lines[index]='!'+lines[index]	
					        control_type_ems.append(lines[i-2])
			
			
            if lines[i].find(' '+sch_adj_ems[j]+',')!=-1:
					        if  lines[i].find('!    ')==-1:
					                lines[i-1]='!'+lines[i-1]
					                lines[i]='!'+lines[i]
					        index=i+1
					        while lines[index].find(';')==-1:
							                      if lines[index].find('!    ')==-1:
                                                                                  lines[index]='!'+lines[index]
							                      index=index+1
					        if lines[index].find(';')!=-1 and lines[index].find('!    ')==-1:
                                                  lines[index]='!'+lines[index]	
					        if index>i+1:
                                                 heat_sch_ems.append(lines[i+1].replace('!    ','    '))
					        else:
                                                 heat_sch_ems.append(None)
					        sch_type_ems.append(lines[i-1].replace('!',''))			
#print control_type

print control_type_ems

line_new=[] 
			

line_new.append('!-   ===========  ALL OBJECTS IN CLASS: EXTERNALINTERFACE ==========='+'\n')				             

line_new.append('ExternalInterface,'+'\n')

line_new.append('    PtolemyServer;           !- Name of External Interface'+'\n')
line_new.append('\n')										 

dup_index=[]

for i in range(len(sch_av)):
      for j in range(len(sch_av)):
	            if i!=j and zone_av[i]==zone_av[j]:
				          if len(dup_index)>1:
						        for k in range(len(dup_index)):
								          if dup_index[k]==i:
										          include=True
										          break
								          include=False
				          else:
                                        
									include=False
				          if not include:									
				                    dup_index.append(i)
				              
dup_index_ems=[]

for i in range(len(sch_av_ems)):
      for j in range(len(sch_av_ems)):
	            if i!=j and zone_av_ems[i]==zone_av_ems[j]:
				          if len(dup_index_ems)>1:
						        for k in range(len(dup_index_ems)):
								          if dup_index_ems[k]==i:
										          include=True
										          break
								          include=False
				          else:
                                        
									include=False
				          if not include:									
				                    dup_index_ems.append(i)      

print len(sch_av_ems)

        
for i in range(len(sch_av)):
    included=False
    for j in range(len(dup_index)):
	    if i == dup_index[j]:
		        included=True
		        break
	    included=False
    if not included:
                line_new.append('ExternalInterface:Schedule,'+'\n')
                line_new.append('    '+zone_av[i].replace('\n','')+'_'+sch_av[i].replace('\n','')+',  !- Name'+'\n')
                line_new.append('    Temperature,             !- Schedule Type Limits Name'+'\n')
                line_new.append('    '+str(default[i])+';                   !- Initial Value'+'\n')
                line_new.append('\n')	

                line_new.append(sch_type[i])
                line_new.append('    '+zone_av[i].replace('\n','')+'_setpoint'+',  !- Name'+'\n')
                if heat_sch[i] is not None:
                                         line_new.append(heat_sch[i])
                line_new.append('    '+zone_av[i].replace('\n','')+'_'+sch_av[i].replace('\n','')+';                !- Cooling Setpoint Temperature Schedule Name'+'\n')
                line_new.append('\n')

                line_new.append('ZoneControl:Thermostat,'+'\n')
                line_new.append('    '+zone_av[i].replace('\n','')+'_Thermostat, !- Name'+'\n')
                line_new.append('    '+zone_av[i].replace('\n','')+', !- Name'+'\n')
                line_new.append(control_type[i].replace('!    ','    '))
                line_new.append('    '+sch_type[i].replace('\n','')+' !- Control 1 Object Type'+'\n')		
                line_new.append('    '+zone_av[i].replace('\n','')+'_setpoint'+';  !- Control Name'+'\n')
                line_new.append('\n')		

for i in range(len(sch_av_ems)):
    included=False
    for j in range(len(dup_index_ems)):
	    if i == dup_index_ems[j]:
		        included=True
		        break
	    included=False
    if not included:
                line_new.append('ExternalInterface:Schedule,'+'\n')
                line_new.append('    '+zone_av_ems[i].replace('\n','')+'_'+sch_av_ems[i].replace('\n','')+',  !- Name'+'\n')
                line_new.append('    Temperature,             !- Schedule Type Limits Name'+'\n')
                line_new.append('    '+str('26.7')+';                   !- Initial Value'+'\n')
                line_new.append('\n')	

                line_new.append(sch_type_ems[i])
                line_new.append('    '+zone_av_ems[i].replace('\n','')+'_setpoint'+',  !- Name'+'\n')
                if heat_sch_ems[i] is not None:
                                         line_new.append(heat_sch_ems[i])
                line_new.append('    '+zone_av_ems[i].replace('\n','')+'_'+sch_av_ems[i].replace('\n','')+';                !- Cooling Setpoint Temperature Schedule Name'+'\n')
                line_new.append('\n')

                line_new.append('ZoneControl:Thermostat,'+'\n')
                line_new.append('    '+zone_av_ems[i].replace('\n','')+'_Thermostat, !- Name'+'\n')
                line_new.append('    '+zone_av_ems[i].replace('\n','')+', !- Name'+'\n')
                line_new.append(control_type_ems[i].replace('!    ','    '))
                line_new.append('    '+sch_type_ems[i].replace('\n','')+' !- Control 1 Object Type'+'\n')		
                line_new.append('    '+zone_av_ems[i].replace('\n','')+'_setpoint'+';  !- Control Name'+'\n')

# add the output


f=open('template/out_temp.txt','r')

lines_output=f.readlines()
f.close()
						
		
# generate the new idf file		
for i in range(len(lines)):
            if lines[i].lower().find('simulationcontrol,')!=-1:
                         if lines[i+5].lower().find('no')!=-1:
                                        lines[i+5]=lines[i+5].replace('No','Yes')
                                        lines[i+5]=lines[i+5].replace('no','Yes')	
lines=lines+line_new+lines_output

for i in range(len(lines)):
            if lines[i].lower().find('runperiod,')!=-1:
                                        lines[i+2]='    8,                       !- Begin Month'+'\n'
                                        lines[i+3]='    1,                       !- Begin Day of Month'+'\n'
                                        lines[i+4]='    8,                      !- End Month'+'\n'
                                        lines[i+5]='    1,                      !- End Day of Month'+'\n'										

	



for i in range(len(lines)):
            if lines[i].lower().find('timestep,')!=-1 and lines[i].lower().find('update frequency')==-1:
			                if lines[i].lower().find(';')!=-1:
							            lines[i]='  Timestep,60;'+'\n'
			                else:
							            lines[i+1]='  60;'+'\n'                                        							
	
										
						 
os.rename(idf_file+'.idf', idf_file+'.idf-bak')
f=open(idf_file+'.idf','w')

for i in range(len(lines)):
     f.writelines(lines[i])
f.close()



# generate the configuration file		

f=open('template/config_head.txt','r')

lines_head=f.readlines()

f.close()

for i in range(len(lines_head)):
     lines_head[i]=lines_head[i].replace('replace',eplus_path)
     lines_head[i]=lines_head[i].replace('%idf_file%',eplus_path)
     lines_head[i]=lines_head[i].replace('%idf_name%',idf_file)
     lines_head[i]=lines_head[i].replace('%wea_file_path%',wea_file_path)
     lines_head[i]=lines_head[i].replace('%wea_name%',wea_name)
     lines_head[i]=lines_head[i].replace('%bcvtb_file_path%',bcvtb_file_path)	 
	 
lines_input=[]

lines_input.append('\n    "inputs" : {'+'\n')

for i in range(len(sch_av)):
         lines_input.append('		"'+zone_av[i].replace('\n','')+'_'+sch_av[i].replace('\n','')+'" : {'+'\n')
         lines_input.append('			"name" : "'+zone_av[i].replace('\n','')+'_'+sch_av[i].replace('\n','')+'",\n')
         lines_input.append('			"type" : "schedule",'+'\n')
         lines_input.append('			"topic" : "PNNL/'+building+'/'+zone_av[i].replace(' ','')+'",'+'\n')
         lines_input.append('			"field" : "CoolingSetpointTemperature"'+'\n')
		 			
         if i==len(sch_av)-1 and len(sch_av_ems)==0:
                    t=''
         else:
                    t=','		 
         lines_input.append('		}'+t+'\n')


for i in range(len(sch_av_ems)):
         lines_input.append('		"'+zone_av_ems[i].replace('\n','')+'_'+sch_av_ems[i].replace('\n','')+'" : {'+'\n')
         lines_input.append('			"name" : "'+zone_av_ems[i].replace('\n','')+'_'+sch_av_ems[i].replace('\n','')+'",\n')
         lines_input.append('			"type" : "schedule",'+'\n')
         lines_input.append('			"topic" : "PNNL/'+building+'/'+zone_av_ems[i].replace(' ','')+'",'+'\n')
         lines_input.append('			"field" : "CoolingSetpointTemperature"'+'\n')
		 			
         if i==len(sch_av_ems)-1:
                    t=''
         else:
                    t=','		 
         lines_input.append('		}'+t+'\n')


		 
lines_input.append('    },'+'\n')		 
		 
		 
lines_output=[]
lines_output.append('    "outputs" : {'+'\n')

for i in range(len(sch_av)):
         lines_output.append('		"'+zone_av[i].replace('\n','')+' Zone Mean Air Temperature'+'" : {'+'\n')
         lines_output.append('			"name" : "'+zone_av[i].replace('\n','')+'",\n')
         lines_output.append('			"type" : "Zone Mean Air Temperature",'+'\n')
         lines_output.append('			"topic" : "PNNL/'+building+'/all",'+'\n')
         lines_output.append('			"field" : "'+zone_av[i].replace(' ','')+'_ZoneTemperature",'+'\n')
         lines_output.append('			"meta" : {"units": "degreesCentigrade", "tz": "US/Pacific", "type": "float"}'+'\n')
		 
         lines_output.append('		},'+'\n')		 
		 
         lines_output.append('		"'+zone_av[i].replace('\n','')+' Cooling Setpoint Temperature'+'" : {'+'\n')
         lines_output.append('			"name" : "'+zone_av[i].replace('\n','')+'",\n')
         lines_output.append('			"type" : "Zone Thermostat Cooling Setpoint Temperature",'+'\n')
         lines_output.append('			"topic" : "PNNL/'+building+'/all",'+'\n')
         lines_output.append('			"field" : "'+zone_av[i].replace(' ','')+'_CoolingSetpointTemperature",'+'\n')
         lines_output.append('			"meta" : {"units": "degreesCentigrade", "tz": "US/Pacific", "type": "float"}'+'\n')
		 
         lines_output.append('		},'+'\n')		 
		 
for i in range(len(sch_av_ems)):
         lines_output.append('		"'+zone_av_ems[i].replace('\n','')+' Zone Mean Air Temperature'+'" : {'+'\n')
         lines_output.append('			"name" : "'+zone_av_ems[i].replace('\n','')+'",\n')
         lines_output.append('			"type" : "Zone Mean Air Temperature",'+'\n')
         lines_output.append('			"topic" : "PNNL/'+building+'/all",'+'\n')
         lines_output.append('			"field" : "'+zone_av_ems[i].replace(' ','')+'_ZoneTemperature",'+'\n')
         lines_output.append('			"meta" : {"units": "degreesCentigrade", "tz": "US/Pacific", "type": "float"}'+'\n')
		 
         lines_output.append('		},'+'\n')		 
		 
         lines_output.append('		"'+zone_av_ems[i].replace('\n','')+' Cooling Setpoint Temperature'+'" : {'+'\n')
         lines_output.append('			"name" : "'+zone_av_ems[i].replace('\n','')+'",\n')
         lines_output.append('			"type" : "Zone Thermostat Cooling Setpoint Temperature",'+'\n')
         lines_output.append('			"topic" : "PNNL/'+building+'/all",'+'\n')
         lines_output.append('			"field" : "'+zone_av_ems[i].replace(' ','')+'_CoolingSetpointTemperature",'+'\n')
         lines_output.append('			"meta" : {"units": "degreesCentigrade", "tz": "US/Pacific", "type": "float"}'+'\n')
		 
         lines_output.append('		},'+'\n')	
		 
		 
		 
f=open('template/config_end.txt','r')

lines_end=f.readlines()

f.close()



for i in range(len(lines_end)):
      lines_end[i]=lines_end[i].replace('replace',building)

  
	  
	  
lines_config=lines_head+lines_input+lines_output+lines_end
		 
f=open('config','w')

for i in range(len(lines_config)):
     f.writelines(lines_config[i])
f.close()
		 
		 
f=open('control_config','w')


f.writelines('   "building":"'+building+'",'+'\n')
f.writelines('   "power_topic":'+'"PNNL/'+building+'/all",'+'\n')
f.writelines('   "points":{'+'\n')	 
for j in range(len(sch_av)):
	          if j==len(sch_av)-1 and len(sch_av_ems)==0:
			           extnt=''
	          else:
			           extnt=','			   
	          f.writelines('	        "point'+str(1+j)+'": "'+zone_av[j].replace(' ','')+'"'+extnt+'\n')
temp=len(sch_av)	

print temp
		  
for j in range(len(sch_av_ems)):
	          if j==len(sch_av_ems)-1:
			           extnt=''
	          else:
			           extnt=','			   
	          f.writelines('	        "point'+str(temp+j+1)+'": "'+zone_av_ems[j].replace(' ','')+'"'+extnt+'\n')			  
f.writelines('    }')          
                   	 	 	 
f.close()		 
		 

