#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" This is the tools module. 
It helps to draw the windwos."""
import sys
import os
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import font



__author__ = "1966bc aka giuseppe costanzi"
__copyright__ = "Copyleft"
__credits__ = ["hal9000",]
__license__ = "GNU GPL Version 3, 29 June 2007"
__version__ = "4.2"
__maintainer__ = "1966bc"
__email__ = "giuseppecostanzi@gmail.com"
__date__ = "2018-12-25"
__status__ = "Production"

class Tools(object):

    def __init__(self,*args, **kwargs):

        super(Tools, self).__init__( *args, **kwargs)
        
    def __str__(self):
        return "class: %s\nMRO: %s" % (self.__class__.__name__,  [x.__name__ for x in Tools.__mro__])


    def get_rgb(self, r,g,b):
        """translates an rgb tuple of int to a tkinter friendly color code"""
        return "#%02x%02x%02x" % (r,g,b)

    def center_me(self, container):
        
        """center window on the screen"""
        x = (container.winfo_screenwidth() - container.winfo_reqwidth()) / 2
        y = (container.winfo_screenheight() - container.winfo_reqheight()) / 2
        container.geometry("+%d+%d" % (x, y))


    def cols_configure(self,w):
        
        w.columnconfigure(0, weight=1)
        w.columnconfigure(1, weight=1)
        w.columnconfigure(2, weight=1)   

    def get_init_ui(self, container):
        """All insert,update modules have this same configuration on init_ui.
           A Frame, a columnconfigure and a grid method.
           So, why rewrite every time?"""
        w = self.get_frame(container)
        self.cols_configure(w)
        w.grid(row=0, column=0, sticky=tk.N+tk.W+tk.S+tk.E)

        return w
        
    def get_frame(self, container, padding=None):
        return ttk.Frame(container, padding=padding)
        
    
    def get_label_frame(self, container, text=None, ):
        return ttk.LabelFrame(container, text=text,)    

    def get_button(self, container, text, row=None, col=None):

        w = ttk.Button(container, text=text, underline=0)

        if row is not None:
            w.grid(row=row, column=col, sticky=tk.W+tk.E, padx=5, pady=5)
        else:
            w.pack(fill =tk.X, padx=5, pady=5)
        
        return w

    def get_label(self, container, text ,textvariable=None, anchor=None, args=()):

        w = ttk.Label(container,
                     text=text,
                     textvariable=textvariable,
                     anchor=anchor)

        if args:
            w.grid(row=args[0], column=args[1], sticky=args[2])
        else:
            w.pack(fill=tk.X, padx=5, pady=5)
        
        return w

 
        

    def get_save_cancel(self, caller, container):

        caller.btnSave = self.get_button(container, "Save",0,2)
        caller.btnSave.bind("<Button-1>", caller.on_save)
        caller.btnSave.bind("<Return>", caller.on_save)
    
        caller.btCancel = self.get_button(container, "Cancel", 1,2)
        caller.btCancel.bind("<Button-1>", caller.on_cancel)



    def on_fields_control(self, container):

        msg = "Please fill all fields."

        for w in container.winfo_children():
            for field in w.winfo_children():
                if type(field) in(ttk.Entry,ttk.Combobox):
                    #print(type(field),)
                    #for i in field.keys():
                    #    print (i)
                    if not field.get():
                        messagebox.showwarning(self.title,msg)
                        field.focus()
                        return 0
                    elif type(field)==ttk.Combobox:
                          if field.get() not in field.cget('values'):
                              msg = "You can choice only values in the list."
                              messagebox.showwarning(self.title,msg)
                              field.focus()
                              return 0

    def get_tree(self, container, cols, size=None, show=None):

        ttk.Style().configure("Treeview.Heading",background = self.get_rgb(240,240,237))
        ttk.Style().configure("Treeview.Heading", font=('Helvetica', 10 ))

        headers = []

        for col in cols:
            headers.append(col[1])
        del headers[0]

        if show is not None:
            w = ttk.Treeview(container,show=show)

        else:
            w = ttk.Treeview(container,)
            
        
        w['columns']=headers
        w.tag_configure('is_enable', background='light gray')

        for col in cols:
            w.heading(col[0], text=col[1], anchor=col[2],)
            w.column(col[0], anchor=col[2], stretch=col[3],minwidth=col[4], width=col[5])
           
        sb = ttk.Scrollbar(container)
        sb.configure(command=w.yview)
        w.configure(yscrollcommand=sb.set)

        w.pack(side=tk.LEFT, fill=tk.BOTH, expand =1)
        sb.pack(fill=tk.Y, expand=1)

        return w

    def get_validate_text(self, caller, what=None ):

        if what is not None:
            callback = self.validate_integer
        else:
            callback = self.validate_float
            
        return (caller.register(callback),
             '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')

    def get_validate_integer(self, caller ):
        return (caller.register(self.validate_integer),
             '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')

    def get_validate_float(self, caller ):
        return (caller.register(self.validate_float),
             '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')


    def limit_chars(self, c, v, *args):
        
        if len(v.get())>c:
               v.set(v.get()[:-1])
         

    def validate_integer(self, action, index, value_if_allowed,
                 prior_value, text, validation_type,
                 trigger_type, widget_name):
        # action=1 -> insert
        if(action=='1'):
            if text in '0123456789':
                try:
                    int(value_if_allowed)
                    return True
                except ValueError:
                    return False
            else:
                return False
        else:
            return True

    def validate_float(self, action, index, value_if_allowed,
                       prior_value, text, validation_type, trigger_type, widget_name):
        # action=1 -> insert
        if(action=='1'):
            if text in '0123456789.-+':
                try:
                    float(value_if_allowed)
                    return True
                except ValueError:
                    return False
            else:
                return False
        else:
            return True              

    def get_widget_attributes(self,container):
        all_widgets = container.winfo_children()
        for widg in all_widgets:
            print('\nWidget Name: {}'.format(widg.winfo_class()))
            keys = widg.keys()
            for key in keys:
                print("Attribute: {:<20}".format(key), end=' ')
                value = widg[key]
                vtype = type(value)
                print('Value: {:<30} Type: {}'.format(value, str(vtype)))

    def get_widgets(self,container):
        all_widgets = container.winfo_children()
        for widg in all_widgets:
            print(widg)
            print('\nWidget Name: {}'.format(widg.winfo_class()))
            #keys = widg.keys()
            
                                
def main():
    
    foo = Tools()
    print(foo)                
    input('end')
       
if __name__ == "__main__":
    main()
