import os
import subprocess
dirpath = os.getcwd()
os.environ["PATH"] += os.pathsep + dirpath + os.pathsep + 'graphviz-2.38\\release\\bin'
print(os.environ["PATH"])
from tkinter import *
from tkinter import Entry
from tkinter.filedialog import askopenfilename
import tkinter as tk
import PARSER as gr
import scanner as src
win = tk.Tk()
var = IntVar()
def readfromfile(INPUTFILE):
    inFile = open(INPUTFILE, 'r') 
    lines = inFile.readlines()
    inFile.close()
    return lines
err=0
y=1    
def main(lines):
    global err
    global y 
    y=1
    err=0
    for i in range(len(src.scanner(lines))):
       print(src.scanner(lines)[i].tokentype)    
       if(src.scanner(lines)[i].tokenvalue==";"):
        y=y+1
       elif(src.scanner(lines)[i].tokenvalue=="then"):
        if((src.scanner(lines)[i-1].tokentype!="NUM") & (src.scanner(lines)[i-1].tokenvalue!=")") &(src.scanner(lines)[i-1].tokentype!="ID")):
          label2.config(text="Error,syntax error at line"+str(y),bg="yellow",fg="black")
          err=1 
        y=y+1
       elif(src.scanner(lines)[i].tokenvalue=="if"):
          if((src.scanner(lines)[i+1].tokentype!="NUM") & (src.scanner(lines)[i+1].tokenvalue!="(") &(src.scanner(lines)[i+1].tokentype!="ID")):
              label2.config(text="Error,syntax error at line"+str(y),bg="yellow",fg="black")
              err=1             
       elif(src.scanner(lines)[i].tokenvalue=="repeat"):
        y=y+1
       elif(src.scanner(lines)[i].tokenvalue=="else"):
        y=y+1
       elif(src.scanner(lines)[i].tokenvalue=="end"):
        y=y+1
       elif(src.scanner(lines)[i].tokenvalue=="until"):
            y=y+1
       elif(src.scanner(lines)[i].tokentype=="NUM"):
        if(i<=(len(src.scanner(lines))-2)):    
          if(src.scanner(lines)[i+1].tokentype=="ID"):
            y=y+1                     
       try:          
        if(src.scanner(lines)[i].tokenvalue=="read"):
          if(src.scanner(lines)[i+2].tokenvalue!=";"):    
                   label2.config(text="Error,syntax error at line"+str(y),bg="yellow",fg="black")
                   err=1
       except:
        label2.config(text="Error,syntax error at line"+str(y),bg="yellow",fg="black")
        err=1                                    
    if(err==0):
     gr.outputs = src.scanner(lines)
     gr.program()                        
     gr.generate_tree()

####Functions####
def sel():  
   x = var.get()
   if x == 1: 
       label1.config(text = "you select FilePath",bg="blue",fg="white")
       label2.config(text="Status: FilePath entry is choosen",bg="yellow",fg="black")        
       E2.config(state='disabled')
       E1.config(state='normal')
       E2.delete(0, END)
       Code.configure(text="File Content:")    
   elif x ==2:
       label1.config(text = "you select code",bg="blue",fg="white")
       label2.config(text="Status: Code entry is choosen",bg="yellow",fg="black")        
       E1.config(state='disabled')
       E2.config(state='normal')
       E2.delete('1.0', END)
       E1.delete(0, END)
       Code.configure(text="Enter Code:")               
def main_RUN():
    global err
    err=0
    x = var.get()
    if(x==1):
      if(Entry.get(E1).endswith(".txt")):
        if(err==0):    
          if(len(Entry.get(E1))):
            label2.config(text="Status: Code is running from file successfully",bg="green",fg="white")
            #lines = readfromfile(Entry.get(E1))
            lines = E2.get(1.0, END)
            lines = lines.split("\n")
            main(lines)
          else:
            label2.config(text="Status: Error, please enter a directory at first!",bg="red",fg="white")
      else:
        label2.config(text="Status: Can't Open This File As It is Not Text File",bg="red",fg="white")              
    elif(x==2):
        if(len(E2.get(1.0, END)) > 1):  
             label2.config(text="Status: Code is Running successsfully",bg="green",fg="white")
             lines = E2.get(1.0, END)
             lines = lines.split()
             main(lines)
        else:
            label2.config(text="Status: Error, empty code",bg="red",fg="white")
    else:
        label2.config(text="Status: Error, select an entry",bg="red",fg="white")
def OpenFileGui():
    filename = askopenfilename()
    if(len(Entry.get(E1))):
        E1.delete(0,END)
    E1.insert(END,filename)
    if(Entry.get(E1).endswith(".txt")):
     lines = readfromfile(Entry.get(E1))
     E2.config(state='normal')
     E2.delete('1.0', END)
     lines = "".join(lines)
     E2.insert(END,lines)
     label2.config(text="code is reading",bg="yellow",fg="black")
def Scanr():
        global err
        err=0
        lines = E2.get(1.0, END)
        lines = "".join(lines)
        tokens_types = {";": "SEMICOLON", "if": "IF", "then": "THEN", "end": "END", "repeat": "REPEAT",
        "until": "UNTIL", ":=": "ASSIGN", "read": "READ", "write": "WRITE", "<": "LESSTHAN", "=": "EQUAL",
        "+": "PLUS", "-": "MINUS", "*": "MULT", "/": "DIV", "(": "OPENBRACKET", ")": "CLOSEDBRACKET","{":"startComment","}":"endComment"}
        reserved_words = ["if", "then", "end", "repeat", "until", "read", "write"]
        single_special_chars = [";", "<", "+", "-", "*", "/", "(", ")","{","}"]
        tokens_collected = []
        skipper = 0
        code = ""
        #taking input
        print("=> type 'run' to generate a file of tokens")
        print("=> type 'exit' to finish")
        print("Enter your code: ")
        # end when exit typed
        code = lines
        print(code[0])
        #scanning
        for i in range(len(code)):
            #skipping if needed
            if skipper > 1:
                skipper -= 1
                continue

            # reset skipping counter to zero
            skipper = 0
            if code[i]=="{":
                tokens_collected.append([code[i], "startComment"])
                num_counter = 1
                try:
                 while (code[i+num_counter]!="}")&(i+num_counter<len(code)):
                  if(code[i+num_counter]=="}"):
                     err=0
                  else:
                    tokens_collected.append([code[i+num_counter], "InComment"])      
                    num_counter += 1
                    skipper += 1
                    err=1
                 tokens_collected.append([code[i+num_counter], "endComment"])
                 err=0
                except:
                 err=1
                 label2.config(text="Error,syntax error at line"+str(y),bg="yellow",fg="black")
            # assign operator
            if code[i] == ":":
                if code[i+1] == "=":
                    tokens_collected.append([code[i]+code[i+1], "ASSIGN"])
                else:
                    tokens_collected.append([code[i], "INVALID_TOKEN"])

            # equal
            elif code[i] == "=":
                if code[i-1] == ":":
                    continue
                else:
                    tokens_collected.append([code[i], "EQUAL"])
            # the rest of the special chars
            elif code[i] in single_special_chars:
                tokens_collected.append([code[i], tokens_types[code[i]]])
            # numbers
            elif code[i].isnumeric():
                num = ""
                num_counter = 0
                while code[i+num_counter].isnumeric():
                    num += code[i+num_counter]
                    num_counter += 1
                    skipper += 1
                tokens_collected.append([num, "NUMBER"])

            # letters => identifiers and reserved words
            elif code[i].isalpha():
                word = ""
                word_counter = 0
                while code[i+word_counter].isalpha():
                    word += code[i+word_counter]
                    word_counter += 1
                    skipper += 1

                # check wether identifier or reserved word
                if word not in reserved_words:
                    tokens_collected.append([word, "IDENTIFIER"])
                else:
                    tokens_collected.append([word, tokens_types[word]])

            #invalid tokens
            elif not code[i].isalpha() and not code[i].isdigit() and code[i] not in single_special_chars and code[i] != " " and code[i] != "\n":
                tokens_collected.append([code[i], "INVALID_TOKEN"])

        #generating file of tokens
        tokens = ""

        #stringify tokens
        for i in tokens_collected:
            print(i)
            token = ",".join(i)
            tokens += token + "\n"
            
        # Specify the file path
        file_path = "tokens.txt"

        # Open the file in write mode ("w"), which will create the file if it doesn't exist
        if(err==0):
          with open(file_path, "w") as file:
           file.write(tokens)
          label2.config(text="code is scanning successfully",bg="green",fg="black")

        # Open the file with the default text editor or associated program on Windows
          subprocess.run(["start", file_path], shell=True, check=True)

####program name####
win.title("Parser Application")
win.configure(background='purple')
win.geometry("700x600")
win.resizable(False,False)

####labels###    
label1 = tk.Label(win, text="",bg="purple")
label1.pack()
label2 = tk.Label(win, text="Status: choose entry", bg="yellow",fg="black")
label2.pack()
L2 = tk.Label(win , text= "Choose your entry:", bg="black",fg="white")
L2.pack()
L2.place(bordermode=INSIDE, x=10, y=25)


####FilePath####
E1 = Entry(win, width = 70)
E1.pack()
E1.place(bordermode=OUTSIDE, x=100, y=110)
Dir = tk.Label(win , text= "Enter FilePath:", fg="white",bg="black")
Dir.pack()
Dir.place(bordermode=INSIDE, x=10, y=110)

####Entry of Code####
E2 = Text(win, width = 80, height = 24)
E2.pack()
E2.place(x= 10, y= 170)
Code = tk.Label(win , text= "Enter Code:",bg="black",fg="white")
Code.pack()
Code.place(bordermode=INSIDE, x=10, y=145)

###Buttons###
R1 = Radiobutton(win, text = "FilePath", selectcolor= "black", highlightcolor = "white", activebackground="purple", bg="purple", fg="white", variable = var, value = 1, command = sel,font= ("Arial", 12, "bold"))
R1.pack()
R1.place(bordermode=OUTSIDE, x=20, y=50)
R2 = Radiobutton(win, text = "Code", selectcolor= "black", highlightcolor = "white",activebackground="purple", bg="purple", fg="white", variable = var, value = 2, command = sel,font= ("Arial", 12, "bold"))
R2.pack()
R2.place(bordermode=OUTSIDE, x=20, y=70)
parse = tk.Button(win, text = "Parse", command = main_RUN,  width = 10,activebackground= "white", activeforeground = "green",font= ("Arial", 10, "bold"),bg="yellow")
parse.pack()
parse.place(x=10, y=560)
scan = tk.Button(win, text = "Scan", command = Scanr,  width = 10,activebackground= "white", activeforeground = "green",font= ("Arial", 10, "bold"),bg="yellow")
scan.pack()
scan.place(x=570, y=560)
OpenFile = tk.Button(win, text = "Open File", command = OpenFileGui,  width = 10,activebackground= "white", activeforeground = "green",font= ("Arial", 10, "bold"))
OpenFile.pack()
OpenFile.place(x=530, y=105)
win.mainloop()