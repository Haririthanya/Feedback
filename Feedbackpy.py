
# coding: utf-8

# In[1]:


#----TKINTER - GUI LIBRARY----
import tkinter as tk
from tkinter import ttk
from tkinter import *
import tkinter.messagebox
from tkinter import filedialog
from tkinter.filedialog import askopenfilename
import time
from datetime import datetime


# In[2]:


#----SEARCH FILE----
import os
from os.path import join
import re


# In[3]:


#----DATA PROCESSING and VISUALIZATION----
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pandas import Series,DataFrame
from matplotlib.pyplot import figure
from matplotlib.backends.backend_pdf import PdfPages


# In[4]:


class App_variables:
        def __init__(self):
            self.save = 0
            self.generate = 0
            self.measures = 0
            self.filename = ""
            self.search=0
            self.browse=0


# In[5]:


App = App_variables()


# In[6]:


def choose_filebrowse(file):
    
    df = pd.read_csv(os.path.expanduser(file),encoding = 'ISO-8859-1')#open the file
    choose_filebrowse.row_count = min(df.shape)#get the row count to know the total strength of the class
    print("choose df",min(df.shape)-2)
    print(df.columns)
    if(App.generate==0):
        if df.empty:
            tk.messagebox.showinfo("File","File Not Found") #File not found
        else:
            tk.messagebox.showinfo("File","File Found") #File found
    return df


# In[7]:


def draw_plots(name,j,l,new_df,pdf):
    def label_values(rects): #Mark the values of the plot on top of it.
        for rect in rects:
            height = rect.get_height()
            ax.text(rect.get_x() + rect.get_width()/2., 1.0*height,
                '%d' % int(height),
                ha='center', va='bottom')
    sum_cols = []
    x = []
    min_ind = new_df[new_df['Name of the teacher']==name].index[0] #Isolate rows belonging to one faculty
    if 'Select All' in l:
        sum_cols = new_df.loc[new_df['Name of the teacher']==name,:].sum(numeric_only=True) #calculate the sum of all columns
        x = [i for i in range(1,21)] #x values
        txt = "" #text to be added below the plot
        i = 1
        for keys in performance_dict.keys(): #get the key values of the selected performance
            txt = txt + str(i)+'-'+keys+'\n'
            i = i+1
    else:
        list_of_cols = []
        for colname in l:
            for col_names in new_df.columns:  #get the actual column name from the dataframe.
                if colname in col_names:
                    list_of_cols.append(col_names) #append it to the list of columns
        sum_cols = new_df.loc[new_df['Name of the teacher']== name,list_of_cols].sum(numeric_only=True) #calculate the sum of the columns in the list of columns
        print('sumcols' , sum_cols)
        x = [i for i in range(1,len(l)+1)]
        txt = ""
        i = 1
        wrap = 1
        for key in l:
            #txt = txt+ str(i)+' - ' + new_df.columns.values[new_df.columns.get_loc(key)]+'\n'
            if(wrap%4==0):
                txt = txt + str(i)+ ' - '+key+'\n'
            else:   
                txt = txt + str(i) +'-' + key+'   '
            i = i+1
            wrap = wrap + 1
        #x = [i for i in range(1,len(l)+1)]
    percent = [round(((i[1]/choose_filebrowse.row_count*5)*100),2) for i in enumerate(sum_cols)]  #calculate the percent 
    y = percent
    print('x:')
    print(x)
    print('y')
    print(y)
    fig,ax = plt.subplots(figsize=(15,8)) #figure size
    figure = plt.gcf()
    plot = ax.bar(x,y,align='center',alpha=0.5,width = 0.5,tick_label=x) #plot the graph for one faculty
    ax.set_title(name+' - '+new_df.iloc[min_ind][0]) #set the title for the plot
    ax.set_ylabel('Performance')          #ylabel
    ax.set_xlabel('Performance Measures')   #xlabel
    fig.subplots_adjust(bottom=0.4)        #space at the bottom    
    #fig.text(.1,.3,txt)
    plt.text(0.01,0.05,txt, transform=fig.transFigure, size=10)  #text coordinates
    fn=label_values(plot) #figure
    pdf.savefig(fn) #save the figure in the opened pdf


# In[8]:


def data_preprocessing():
    filename = browsefunc.filename  #get the filename
    df = choose_filebrowse(filename)  #get the dataframe
    row_count = min(df.shape) 
    del df['Timestamp']  #delete timestamp , email address columns
    del df['Email Address']
    #del df['Section']
    print("Shape" , max(df.shape))
    df.columns = ['Subject taught & Course No', 'Name of the teacher', 'Punctuality and Regularity in the Class', 'Completes syllabus of the course in time', 'Focus on Syllabi', 'Self-Confidence', 'Communication Skills', 'Skill of linking subject to life experience & creating interest in the subject', 'Refers to latest developments in the field', 'Uses of teaching aids (Blackboard/PPT\x92s/Video lectures etc)', 'Shares and discusses the answers of test questions after the conduct of test.', 'Makes sure that he / she is being understood', 'Helps student in providing study material which is not readily available in the text books say through e-sources, e-journals, reference books, open course wares etc.', 'Helps students irrespective of ethnicity and culture / background and gender', 'Approach towards developing professional skills among students', 'Helps students in realizing career goals', 'Regular checking of laboratory observation books / Records', 'Helping the students in conducting experiments through set of instructions or demonstrations', 'Control mechanism in effectively conducting the class', 'Skills of addressing inappropriate behavior of students', 'Tendency of inviting opinion and question on subject matter from students', 'Inspires students for ethical conduct and acts as a role model','Additional Remarks']*(max(df.shape)//23)
    list = []
    i=0
    for col in df:
        list.append(df.iloc[:,i:i+23]) # beginning and end indices for each faculty
        i=i+23
    
    new_df = pd.concat([list[i] for i in range(0,max(df.shape)//23)],sort = False,ignore_index=True) #adding subsequent faculties under the first faculty columns and creating a new data frame with just 23 columns.
    #del new_df['Additional Remarks'] #remove col
    cat_det = {'Excellent (5)':5,'Very Good (4)':4,'Good (3)':3,'Average (2)':2,'Below Average (1)':1} #substitution values 
    for col in df:
        try:
            new_df[col] = new_df[col].apply(lambda x:cat_det[x])   #substitute the values column wise
        except:
            pass
    return new_df


# In[9]:


def check_measure_select():
    for k,v in performance_dict.items():  #to check if atleast one performance measure is chosen by the user while generating the plot
        if v .get() == 1:     
            return 1
    return 0


# In[10]:


def generate_results():
    App.measures = check_measure_select()
    if (App.measures == 0):
        tk.messagebox.showinfo("Measures","Select few measures to generate graph")
        #App.measures = check_measure_select()
    if(App.measures == 1):    
        App.generate = 1
        l = []
        for key, value in performance_dict.items():
            if value.get() > 0:
                l.append(key)
        new_df = data_preprocessing() 
        names = new_df['Name of the teacher'].unique()
        print(names)
        #try:
            #if(len(browsefunc.filename)!=0):
        print(App.save)
        if (App.save==0):
            match=re.search(r'([\w.-]+)+.csv',browsefunc.filename)  #get the filename from the path using regular expression , when save as is not used.
            pdf = PdfPages(match.group(1)+'results'+time.strftime("%d-%m-%Y-%H-%M-%S")+'.pdf')
            App.filename = App.filename + match.group(1)+'results'+time.strftime("%d-%m-%Y-%H-%M-%S")+'.pdf'
        else:
            pdf = PdfPages(Path.name)
            match=re.search(r'([\w.-]+)+.pdf',Path.name)
            App.filename = match.group(1)+'.pdf'
        
        #Summary page of the pdf
        Subject_taught = new_df['Subject taught & Course No'].unique()
        print(Subject_taught)
        list_of_cols = []
        avg_fac = []
        for colname in l:
            for col_names in new_df.columns:
                if colname in col_names:
                    list_of_cols.append(col_names)
        print("total value",choose_filebrowse.row_count*5)
        for name in names: 
            print(name)
            sum_cols = new_df.loc[new_df['Name of the teacher']== name,list_of_cols].sum(numeric_only=True)
            sum_cols = [((i/choose_filebrowse.row_count)*100) for i in sum_cols]
            avg_fac.append(sum(sum_cols)//len(list_of_cols))
        print(avg_fac)
        print(len(names))
        print(len(Subject_taught))
        print(len(avg_fac))
        data = {'Name of Faculty':[name for name in names],'Subject Taught':[sub for sub in Subject_taught],'Faculty Performance':[avg for avg in avg_fac]}
        avg_df = pd.DataFrame(data)
        print(avg_df)
        fig = plt.figure(figsize=(15,7))
        ax = plt.subplot(111)
        ax.set_title('Summary of Faculty Performance')
        ax.axis('off')
        ax.table(cellText=avg_df.values,cellLoc = 'left', colLabels=avg_df.columns,colWidths = [0.5,0.4,0.2],FONTSIZE=12,bbox=[0,0,1,1])
        pdf.savefig(fig)    
         
        #drawplots
        for i in names:
            j=0
            draw_plots(i,j,l,new_df,pdf)
            j=j+1
        tk.messagebox.showinfo("Plot","Plot Generated and File Saved as "+str(App.filename))
        pdf.close() #close pdf streams
    


# In[11]:


def browsefunc():
    files = [("CSV","*.csv")]  #constraint for selection
    browsefunc.filename = filedialog.askopenfilename(filetypes=files,defaultextension = files)
    pathlabel.config(text=browsefunc.filename)
    if browsefunc.filename:
        try:
            tk.messagebox.showinfo('Source File','File Opened')
            App.browse = 1
        except:
            tk.messagebox.showerror('Source File','Failed to read file')


# In[12]:


def Save_as():
    files = [("PDF","*.pdf")]  #constraint to save file
    global Path
    Path = filedialog.asksaveasfile(filetype = files,defaultextension = files)
    match_name=re.search(r'([\w.-]+)+.pdf',Path.name)
    App.save = 1


# In[13]:


def select_all_command(): #when select all is checked ,make all check boxes checked
    if(select_all.get()==0):
        for keys in performance_dict:
            performance_dict[keys].set(0);
    if(select_all.get()==1):
        App.measures = 1
        for keys in performance_dict:
            performance_dict[keys].set(1);
        checkbutton_list.append(select_all_c)


# In[14]:


def on_closing():           #prompt the user to quit without saving
    if App.generate == 0 and (App.search == 1 or App.browse == 1):
        if tk.messagebox.askokcancel("Quit", "Are you sure if want to quit without saving?"):
            window.destroy()
    elif(App.search==0 and App.browse == 0):
        if tk.messagebox.askokcancel("Quit","Are you sure if want to quit?"):
            window.destroy()
    else:    
        window.destroy()


# In[15]:


window = tk.Tk()
window.title("Performance Analysis")
window.geometry("800x800")


# In[16]:


TopFrame = Frame(window)
BottomFrame = Frame(window)
TopFrame.pack()
BottomFrame.pack()


# In[17]:


#----LABELS----
prompt = ttk.Label(TopFrame,text="Welcome to Performance Analysis App",font=('Times New Roman',15))
prompt.grid(row = 0,columnspan = 3,sticky = W)


# In[18]:


selection_prompt = ttk.Label(BottomFrame,text="Choose the required performance measures",justify=tk.LEFT,font=('Times New Roman',10))
selection_prompt.grid(row = 22,sticky = W ,padx = 5)


# In[19]:


checkbutton_list = []
performance_dict = {'Punctuality and Regularity':0,'Completes syllabus':0,'Focus on Syllabi':0,'Self-Confidence':0,'Communication Skills':0,'Skill of linking subject to life':0,'Refers to latest developments':0,'Uses of teaching aids':0,'Shares and discusses the answers':0,'Makes sure that he / she is being understood':0,'Helps student in providing study material':0, 'Helps students irrespective of ethnicity':0,'Approach towards developing professional skills':0,'Helps students in realizing career goals':0,'Regular checking of laboratory observation':0,'Helping the students in conducting experiments':0,'Control mechanism':0,'Skills of addressing inappropriate behavior':0,'Tendency of inviting opinion and question':0,'Inspires students for ethical conduct':0}
labels = list(performance_dict.keys())
i=0

row_no = 24
for keys in performance_dict:
    if i == 2:
        i = 0
        row_no = row_no + 3
    performance_dict[keys] = IntVar()
    c = ttk.Checkbutton(BottomFrame, text=keys, variable=performance_dict[keys])
    c.grid(column = i , row = row_no,sticky = W) 
    checkbutton_list.append(c)
    i = i + 1


# In[20]:


#----LABELS - SELECT ALL----
select_all = IntVar()
select_all_c = ttk.Checkbutton(BottomFrame,text='Select All',variable = select_all,command=select_all_command)
select_all_c.grid(column=1,row = 95,sticky=W)


# In[21]:


#----BUTTON - BROWSE FILE----
browsebutton = ttk.Button(TopFrame,text='Browse',command=browsefunc)
browsebutton.grid(row = 28,sticky = W)
pathlabel = ttk.Label(window)
pathlabel.pack()


# In[22]:


#----BUTTON - GENERATE RESULTS----
generate_results = ttk.Button(BottomFrame , text = "Generate Results",command = generate_results)
generate_results.grid(row = 105,sticky = W)


# In[23]:


#----BUTTON - SAVE AS----
save_as = ttk.Button(BottomFrame , text = "Save As",command = Save_as)
save_as.grid(row = 100 , sticky = W)


# In[24]:


window.protocol("WM_DELETE_WINDOW",on_closing)


# In[25]:


window.mainloop()


# In[219]:


for i in range(0,2):
    print(i)


# In[220]:


66//23

