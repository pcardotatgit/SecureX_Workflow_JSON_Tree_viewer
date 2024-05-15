#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Copyright (c) 2023 Cisco and/or its affiliates.

This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at

               https://developer.cisco.com/docs/licenses

All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.

What is this :
    read an XDR workflow JSON export and parse it
    Then Create a trees graph that shows only key information in order to understand fast the workflow  
    
version 20240504

'''
from crayons import *
import sys
import time
import datetime 
import json
import ijson
import os
import glob


debug=0
display_path=0 

text_out='''<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html>
<head>
    <title>Visual JSON Parser for XDR Workflows</title>
    <link rel="StyleSheet" href="dtree.css" type="text/css" />
    <script type="text/javascript" src="dtree.js"></script>
    <script language='javascript'>
        function popup_window( url, id, width, height )
        {
           //extract the url parameters if any, and pass them to the called html
           var tempvar=document.location.toString(); // fetch the URL string
           var passedparams = tempvar.lastIndexOf("?");
           if(passedparams > -1)
              url += tempvar.substring(passedparams);
          popup = window.open( url, id, 'toolbar=no,scrollbars=yes,location=no,statusbar=no,menubar=no,resizable=no,width=' + width + ',height=' + height + '' );
          popup.focus();
        }    
    </script>    
</head>
<body>
<h2>XDR JSON workflow to Tree Graph</h2>
<div class="dtree">
    <p><a href="javascript: d.openAll();">open all</a> | <a href="javascript: d.closeAll();">close all</a></p>
    <script type="text/javascript">
        <!--
        d = new dTree('d');
        d.add(0,-1,'JSON Tree Graph');        
'''

def delete_notes():
    file_list=glob.glob("./result/note_*.html")
    for fichier in file_list:
        fichier=fichier.replace('\\','/')       
        print(fichier)
        if os.path.exists(fichier):
            print(' ok delete ',fichier)
            os.remove(fichier)  
            
def read_json(filename):
    '''
        read json text file and convert it into json data
    '''
    with open(filename,'r') as file:
        text_data=file.read()
    json_data=json.loads(text_data)
    return(json_data)
    
def parse_json_tree(json_data):
    i=1
    for itemL0 in json_data:
        if i==1:
            print (cyan(itemL0,bold=True))
            i=0
            i1=1
            for itemL1 in itemL0:
                if i1==1:
                    print (red(itemL1,bold=True))
                    i1=0
                else:
                    print (green(itemL1,bold=True))
                    i1=1            
        else:
            print (yellow(itemL0,bold=True))
            i=1 
            i1=1            
            for itemL1 in itemL0:
                if i1==1:
                    print (red(itemL1,bold=True))
                    i1=0
                else:
                    print (green(itemL1,bold=True))
                    i1=1             
def sxo_path0(path,list,index):
    word_list=path.split('.')
    ii=index
    result=''    
    print()
    print(list, index)
    print()    
    for item in word_list:
        if item=='item':
            #result=result+'['+str(list[ii])+'].'
            result=result+'[xx].'
            ii+=1
            print(yellow(item,bold=True))  
        else:
            result=result+item+'.'
            print(white(item,bold=True))        
    print()    
    result=result[:-1]
    print(yellow(result,bold=True))
    goi=input('OK')
    return(result)
 
def sxo_path(path,list,index):
    word_list=path.split('.')
    ii=0
    result=''    
    #print()
    #print(cyan(list))
    #print()    
    for item in word_list:
        ii+=1
        if item=='item':
            result=result+'['+str(list[ii]-1)+']'
            #result=result+'[xx]'
            #print(yellow(f"ii:{ii} item={item} valeur:{list[ii]-1}",bold=True))                        
            #print(yellow(item,bold=True))  
        else:
            result=result+'["'+item+'"]'
            #print(white(item,bold=True))        
    #print()    
    #print(cyan(result,bold=True))
    #goi=input('OK')
    return(result)

def icon(line,valeur):
    print(yellow(line))
    line=line.strip()
    #gio=input('OK:')
    if 'workflow'==line:
        icone='img/run.gif'  
        #gio=input('OK:')
    elif 'target_groups' in line:
        icone='img/target_group.gif'          
    elif 'target' in line:
        icone='img/target.gif'         
    elif 'actions'==line:
        icone='img/task.gif' 
    elif 'schedules' in line:
        icone='img/schedule.gif' 
    elif 'calendar' ==line:
        icone='img/schedule.gif'  
    elif 'variable_value_new' in line:
        icone='img/set_variable.gif' 
    elif 'variable' in line:
        icone='img/var_out.gif'         
    elif 'triggers' == line:
        icone='img/alarm.gif'  
    elif 'triggerschedule' in line:
        icone='img/schedule.gif'          
    elif 'subworkflows' in line:
        icone='img/subworkflow.gif' 
    elif 'dependent_workflows' in line:
        icone='img/subworkflow.gif'
    elif 'atomic' in line:
        icone='img/a_atomic.gif'        
    elif 'description' in line:
        icone='img/info.gif' 
    elif 'script' == line:
        icone='img/topic.png' 
    elif 'name' ==line:
        print(yellow(f'valeur : {valeur}',bold=True))
        #gio=input('OK:')
        if valeur=='<u>Execute Python Script</u>':
            icone='img/python.gif' 
        elif valeur=='<u>Condition Block</u>':
            icone='img/if_block.gif' 
        elif valeur=='<u>Set Variables</u>':
            icone='img/set_variable.gif'
        elif valeur=='<u>HTTP Request</u>':
            icone='img/globe.gif'    
        elif valeur=='<u>For Each</u>':
            icone='img/loop.gif'   
        elif valeur=='<u>Completed</u>':
            icone='img/checkbox_no_full.gif'  
        elif valeur=='<u>description</u>':
            icone='img/info.gif'
        elif valeur=='<u>Break</u>':
            icone='img/red_cross.gif'             
        elif valeur=='<u>Parallel Block</u>':
            icone='img/parallel_bloc.gif'    
        elif valeur=='<u>Parallel Branch</u>':
            icone='img/parallel_branch.gif'  
        elif valeur=='<u>While Loop</u>':
            icone='img/while_loop.gif'       
        else:
            icone='' 
    elif 'scope' ==line:
        print(yellow(f'valeur : {valeur}',bold=True))
        #gio=input('OK:')
        if valeur=='input':
            icone='img/input.gif' 
        elif valeur=='output':
            icone='img/output.gif'             
        else:
            icone=''             
    else:
        icone=''
    return(icone)
    
def format_description(description):
    #print(description)
    #a=input('STOP 3: ')
    if 'generic . ' in description:
        description=description.split('generic . ')[1]
        #a=input('STOP 2: ')
    if 'base_type' in description or 'schema_id' in description or 'object_type' in description or 'is_required' in description or 'display_on_wizard' in description or 'is_invisible' in description or 'persist_output' in description or 'populate_columns' in description or 'skip_execution' in description or 'continue_on_failure' in description or 'basic . category' in description or 'category_type' in description or 'disable_certificate_validation' in description or 'delete_workflow_instance' in description or 'allow_auto_redirect' in description or 'allow_headers_redirect' in description or 'continue_on_error_status_code' in description or 'use_custom_format' in description: 
        description="hidden..."
        #a=input('STOP : ')
    if 'datatype . ' in description:
        description=description.replace('datatype . ','')
    if 'core . ' in description:
        description=description.replace('core . ','')
    if 'logic . ' in description:
        description=description.replace('logic . ','')    
    if 'web-service . http_request' in description:
        description=description.replace('web-service . ','')       
    if '___( CLICK on this link to see object content )' in description:
        description=description.replace('<span style="color:black;font-weight:bolder">','<span style="color:red;font-weight:bolder">')
    if 'workflow . sub_workflow' in description:
        description=description.replace('<span style="color:black;font-weight:bolder">','<span style="color:DarkRed;font-weight:bolder">')
    if 'unique_name' in description:
        description=description.replace('<span style="color:black;font-weight:bolder">','<span style="color:LightBlue;">')
    return(description)
    
def parse_json(json_filename,debug):
    tree=''
    parent_base=0
    parent=1
    child=0
    prefix_lenght=0
    levels=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    level_index=0
    notes_index=0
    nb_levels_items_list=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    levels_items_name_list=["","","","","","","","","","","","","","","","","","","","","","","","","","","",""]
    upper_level=''
    with open(json_filename, 'rb') as input_file:
        # load json iteratively
        parser = ijson.parse(input_file)
        fichier=open('result.txt','w')
        fichier2=open('tree.txt','w')
        last_dot_count=0
        back=0
        word_list=['end_map','map_key','end_array','start_array','start_map']
        for prefix, event, value in parser:
            print('{},-> {} = {}'.format(prefix, event, value))
            if event not in word_list:
                key_list=prefix.split('.')
                key=key_list[len(key_list)-1]
                if debug:
                    print(red(type(value),bold=True))      
                link=''
                if type(value) is str:
                    if debug:
                        print(red('value count:',bold=True))
                        print(red(value.count('\n'),bold=True))
                    if len(value)<1000 and value.count('\n')==0 and value.count('\r')==0:
                        valeur=value.replace("'","")
                    else:
                        if debug:
                            print(cyan(valeur,bold=True))
                        note_name='./result/note_'+str(notes_index)+'.html'
                        with open(note_name,'w') as note:
                            note.write('<html><head><link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/default.min.css"><script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script><script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/languages/go.min.js"></script></head><body><pre><code>')
                            note.write(value)
                            note.write('\n</code></pre><script>hljs.highlightAll();</script></body></html>')
                        link='./note_'+str(notes_index)+'.html'
                        link='javascript:popup_window(\'./note_'+str(notes_index)+'.html\', \'note\', 700, 500);'
                        notes_index+=1                        
                        valeur='___( CLICK on this link to see object content )'
                else:
                    valeur=value                      
                    if debug:
                        print('not a string')
                if debug:                        
                    print(yellow(valeur,bold=True))
                line_out='{},-> {} = {}'.format(prefix, key, valeur)                           
                fichier.write(line_out)
                fichier.write("\r")  
                if link=='':
                    #link='no_link1.html'
                    link=''
                parent=levels[level_index]
                str_parent=str(parent)
                if debug:
                    print(red(f"level index ={level_index}",bold=True))
                    print(red(f"parent level line number ={str_parent}",bold=True))
                    print(yellow(levels,bold=True))
                if key=='item':
                    item_index=str(nb_levels_items_list[level_index])
                    nb_levels_items_list[level_index]+=1
                    prefix_nb_items=prefix.count('.')
                    chemin_list=prefix.split('.')
                    if chemin_list[prefix_nb_items-1]=='variables' and chemin_list[prefix_nb_items]=='item':
                        key='variable'
                    if chemin_list[prefix_nb_items-1]=='actions' and chemin_list[prefix_nb_items]=='item':
                        key='action'  
                    if chemin_list[prefix_nb_items-1]=='blocks' and chemin_list[prefix_nb_items]=='item':
                        key='block'                           
                    key=key+item_index                
                if display_path:
                    prefix2='|--------------->'+sxo_path(prefix,nb_levels_items_list,level_index)
                else:
                    prefix2='' 
                if type(valeur)==bool:
                    if valeur:
                        color2='green'
                    else:
                        color2='red'
                else:
                    if valeur=='input':
                        color2='green'
                    elif valeur=='None':
                        color2='grey'
                    elif valeur=='output':
                        color2='red'                           
                    else:
                        color2='black'  
                if key=='name' or key=='display_name':
                    valeur='<u>'+valeur+'</u>'                  
                if type(valeur)==str:              
                    if valeur=='None':
                        valeur=''
                    else:
                        valeur=valeur.replace('.',' . ') 
                        if "secure_string" in valeur:
                            color2='orange'
                        elif "subworkflow" in valeur:
                            color2='red'                                
                if valeur is None:                     
                        valeur=''
                check_key_list=['variable_value_new','variable_to_update']
                if key in check_key_list and valeur=='':
                    color2='red'
                    valeur='Is empty... Is it Realy Missing ?  Check This...' 
                if key =="skip_execution" and valeur==True:    
                    color2='red'
                elif key =="skip_execution" and valeur==False: 
                    color2='green'
                elif key =="user" and valeur: 
                    color2='red' 
                elif key =="host" and valeur: 
                    color2='red'         
                icone=icon(key,valeur)
                icone_open=icone                    
                description='<span style="color:blue;font-weight:bolder"> {}</span> : <span style="color:{};font-weight:bolder">{}</span> {} '.format( key,color2, valeur, prefix2) 
                title='dtree'
                target=''
                if parent==-1:
                    description='JSON Tree'
                description=format_description(description)                    
                line_out2=f"        d.add({parent_base},{str_parent},'{description}',\"{link}\",'{title}','{target}','{icone}','{icone_open}');"
                print(cyan(line_out2,bold=True))
                if debug:
                    gio=input('-- NEW KEY ADDED :')                
                if parent_base!=0:
                    tree=tree+line_out2+'\n'
                    fichier2.write(line_out2)
                    fichier2.write("\r") 
                    print(green('saved *')) 
                else:
                    print(red('dont save'))                    
                parent_base+=1
            else:
                if event == 'start_array' or event == 'start_map':
                    if debug:
                        print(yellow('go to next level ->',bold=True))
                    key_list=prefix.split('.')
                    key=key_list[len(key_list)-1]
                    valeur=value
                    line_out='{},-> {} = {}'.format(prefix, key, valeur)                           
                    fichier.write(line_out)
                    fichier.write("\r")  
                    link='no_link2.html'
                    mota='Levels : '
                    for a in range (0,level_index):
                        mota+=str(levels[a])+' - '
                    print(white(mota,bold=True))
                    the_parent=levels[level_index]
                    str_parent=str(the_parent)
                    if debug:                        
                        print(red(f"level index ={level_index}",bold=True))                    
                        print(red(f"parent level line number ={str_parent}",bold=True)) 
                        print(yellow(levels,bold=True))
                        print(yellow(levels_items_name_list,bold=True))
                    upper_level=prefix   
                    prefix2=prefix
                    if level_index>=len(levels_items_name_list): 
                        print(level_index)
                        print(levels_items_name_list)
                        gio=input('STOP')                    
                    print(levels_items_name_list[level_index])
                    print(key)
                    if levels_items_name_list[level_index]!=key:
                        levels_items_name_list[level_index]=key
                        nb_levels_items_list[level_index]=0                        
                    if key=='item':
                        item_index=str(nb_levels_items_list[level_index])
                        nb_levels_items_list[level_index]+=1  
                        prefix_nb_items=prefix.count('.')                        
                        chemin_list=prefix.split('.')
                        if chemin_list[prefix_nb_items-1]=='variables' and chemin_list[prefix_nb_items]=='item':
                            key='variable'  
                        if chemin_list[prefix_nb_items-1]=='actions' and chemin_list[prefix_nb_items]=='item':
                            key='action' 
                        if chemin_list[prefix_nb_items-1]=='blocks' and chemin_list[prefix_nb_items]=='item':
                            key='block'                             
                        key=key+item_index        
                        prefix2=sxo_path(prefix,nb_levels_items_list,level_index)
                    icone=icon(key,valeur)
                    icone_open=icone                          
                    if parent==-1:
                        description='JSON Tree';  
                    else:                    
                        if display_path:
                            prefix2='|--------------->'+sxo_path(prefix,nb_levels_items_list,level_index)
                        else:
                            prefix2=''
                        if type(valeur)==bool:
                            if valeur:
                                color2='green'
                            else:
                                color2='red'
                        else:
                            if valeur=='input':
                                color2='green'
                            elif valeur=='None':
                                color2='grey'
                            elif valeur=='output':
                                color2='red'                           
                            else:
                                color2='black'
                        if key=='name' or key=='display_name':
                            valeur='<u>'+valeur+'</u>'
                        if type(valeur)==str:
                            if valeur=='None':
                                color2='red'
                                valeur='MISSING ?'
                            else:
                                valeur=valeur.replace('.','  .  ')                                  
                        if valeur is None:
                            valeur=''                             
                        description='<span style="color:blue;font-weight:bolder"> {}</span> : <span style="color:{};font-weight:bolder">{}</span> {} '.format( key,color2, valeur, prefix2)                                            
                    title='dtree'
                    target='' 
                    description=format_description(description)                    
                    line_out2=f"        d.add({parent_base},{str_parent},'{description}','{link}','{title}','{target}','{icone}','{icone_open}');"
                    print(cyan(line_out2,bold=True))
                    if debug:
                        gio=input(' -> NEW CHILD KEY ARRAY ADDED:')
                    if parent_base!=0:
                        tree=tree+line_out2+'\n'
                        fichier2.write(line_out2)
                        fichier2.write("\r")
                        #levels[level_index]+=1
                        if debug:
                            print(green('saved to file',bold=True)) 
                    else:
                        if debug:
                            print(red('dont save'))          
                        else:
                            pass 
                    level_index+=1
                    levels[level_index]=parent_base                     
                    parent_base+=1                    
                    if debug:
                        print(yellow(levels,bold=True))
                        print(yellow(f"new level_index = {level_index}  and value set to {levels[level_index]}",bold=True))                      
                        gio=input('en avant NEXT done >>:')
                if event == 'end_array' or event == 'end_map':
                    back=1
                    nb_levels_items_list[level_index]=0                         
                    if debug:
                        print(yellow(levels,bold=True))
                    if upper_level==prefix:                        
                        level_index-=1
                        if debug:
                            print('level_index equal -1')
                    else:
                        level_index=prefix.count('.')+1
                        if debug:
                            print('count number of dots')                        
                    if debug:
                        print(cyan(f"{prefix} (prefix)",bold=True))
                        print(cyan(f"{upper_level} (upper_level)",bold=True))
                        print(red(levels,bold=True))
                        print(red(f"level_index = {level_index}",bold=True))
                        print(red(f"next parent line = {levels[level_index]}",bold=True))                     
                        gio=input('en arriere BACK done<<:')
        fichier.close()
        fichier2.close()
        return(tree)
        
if __name__=="__main__":
    print(yellow("Delete old notes",bold=True))
    delete_notes()
    print(yellow("Done",bold=True))
    files =[file for file in os.listdir('./sxo_json_workflow')]
    for file in files:
        fichier='./sxo_json_workflow/'+file
    #print(fichier) 
    tree=parse_json(fichier,debug)
    footer='''
        document.write(d);
        //-->
    </script>
</div>
</body>
</html>
    '''
    
    text_out=text_out+tree+footer
    with open('./result/index.html','w') as fich:
        fich.write(text_out)

    print("==========================================================")
    print()
    print(yellow('DONE - Open the /result/index.html file with your browser ',bold=True))
    print()   
    print("==========================================================") 