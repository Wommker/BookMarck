from tkinter import *
from tkinter import messagebox
from io import open
import sqlite3

#Functions

    #savebookmark: Create the database and save the bookmark

def savebookmark():
    #In the case that the database does not exist it creates it and also the HTML file
    try:
        myconnection=sqlite3.connect("BBDD")
        mycursor=myconnection.cursor()
        mycursor.execute("CREATE TABLE BOOKMARKS (LABEL VARCHAR(50), BOOKMARK VARCHAR(50) UNIQUE, URL VARCHAR(5000))")
        html_file=open("file.html","w")
        html_file.close()
    except:
        pass
    #Once if the database is created Save the bookmark
    finally:
        myconnection=sqlite3.connect("BBDD")
        mycursor=myconnection.cursor()
        if entrybookmark.get() != '' and entryurl.get() != '':
            try:
                if entrylabel.get() == '':
                    strlabel.set("Temporary markers")
                mycursor.execute("INSERT INTO BOOKMARKS VALUES('"+entrylabel.get()+"','" + entrybookmark.get()+ "','" + entryurl.get()+"')")
                messagebox.showinfo("Bookmark Created", "The bookmark has been created: "+entrybookmark.get())

            except:
                #If the bookmark already exists:
                messagebox.showerror("Error","The bookmark already exists")
        else:
            #If there is no bookmark and / or url written
            messagebox.showerror("Error", "Insufficient information, make sure you get the name and URL fields")
        myconnection.commit()
        myconnection.close()
        writehtml()

#writehtml: Write the bookmarks

def writehtml():
    try:
        varcss = radiovarcss.get()
        if varcss == 0:
            try:
                html_file=open("file.html","r")
                tex=html_file.read()
                if len(tex)>=80:
                    if tex[80] == '1':
                        varcss = 1
                    elif tex [80] == '2':
                        varcss = 2
                    elif tex [80] == '3':
                        varcss = 3
                    else:
                        varcss = 1
                else:
                    varcss = 1
                html_file.close()
            except:
                varcss = 1
                  
        myconnection=sqlite3.connect("BBDD")
        mycursor=myconnection.cursor()
        html_file=open("file.html","w")
        mycursor.execute("SELECT * FROM BOOKMARKS ")
        bookmarkslist=mycursor.fetchall()
        #Create the label list
        labellist = []
        for i in bookmarkslist:
            if i[0] in labellist:
                pass
            else:
                labellist.append(i[0])
        #Write HTML
        html_file.write('<!DOCTYPE html>\n<html>\n<head>\n<title>Enlaces</title>\n<meta charset="utf-8">')
            #Write CSS as the case may be
        if varcss == 1:
            html_file.write('\n<!--1-->\n<style type="text/css">\nbody{font-family:Century Gothic;background:rgb(25,25,25);text-decoration:none;}\n.Clases{display:grid;grid-template-columns:1fr 1fr 1fr;}\n.Clase{	background-color:rgba(44,44,44,1);text-align:center;border-style:solid;border-width:10px;border-color:rgba(34,34,34,1);	border-collapse:collapse;margin:10px;}\n.Clase h3{font-size:25px;color:rgba(163,48,48,1);margin:20px;padding:0px;}\n.Clase a{text-decoration:none;color:rgba(250,250,250,1);}\n</style>')
        elif varcss == 2:
            html_file.write('\n<!--2-->\n<style type="text/css">\nbody{font-family:Century Gothic;background:rgb(50,137,124);text-decoration:none;}\n.Clases{display:grid;grid-template-columns:1fr 1fr 1fr;}\n.Clase{	background-color:rgba(74,184,173,1);text-align:center;border-style:solid;border-width:10px;border-color:rgba(248,181,50,1);border-collapse:collapse;margin:10px;}\n.Clase h3{font-size:25px;color:rgba(255,73,25,1);margin:20px;padding:0px;}\n.Clase a{text-decoration:none;color:rgba(250,250,250,1);}\n</style>')
        elif varcss == 3:
            html_file.write('\n<!--3-->\n<style type="text/css">\nbody{font-family:Century Gothic;background:rgb(7,30,37);text-decoration:none;}\n.Clases{display:grid;grid-template-columns:1fr 1fr 1fr;}\n.Clase{	background-color:rgba(6,57,75,1);text-align:center;border-style:solid;border-width:10px;border-color:rgba(34,160,182,1);border-collapse:collapse;margin:10px;}\n.Clase h3{font-size:25px;color:rgba(203,12,69,1);margin:20px;padding:0px;}\n.Clase a{text-decoration:none;color:rgba(250,250,250,1);}\n</style>')
        html_file.write('\n</head>\n<body><section class="Clases">')
            #Write all bookmarks
        for e in labellist:
            if e != labellist[0]:
                html_file.write('</section>')
            html_file.write('<section class="Clase">')
            html_file.write('<h3>' + str(e) + '</h3> <br / > \n')
            for i in bookmarkslist:
                if e == i[0]:
                    html_file.write('<a href="' + str(i[2]) + '">' + str(i[1]) + '</a> <br / > \n')
        html_file.write('</section></body>\n</html>')
        html_file.close()
        myconnection.close()
    except:
        pass
    
#deletebookmark: Delete the marker and if it is the case delete the Label with all its markers
        
def deletebookmark():
    try:
        myconnection=sqlite3.connect("BBDD")
        mycursor=myconnection.cursor()
        mycursor.execute("SELECT * FROM BOOKMARKS ")
        bookmarkslist=mycursor.fetchall()
        #Check if the name of the bookmark to delete exists
        if entrybookmark.get() != '':
            for i in bookmarkslist:
                #When I find the bookmark
                if i[1] == entrybookmark.get():
                    #Ask if you want to delete it
                    if(messagebox.askyesno("Are you sure you want to delete? "," Are you sure you want to delete the bookmark " + entrybookmark.get() + "?")):
                        mycursor.execute("DELETE FROM BOOKMARKS WHERE BOOKMARK=" + "'" + entrybookmark.get() + "'" )
                        break
                    else:
                        break
            #If not found the bookmark Show error
                elif i[1]==(bookmarkslist[len(bookmarkslist)-1][1]):
                    messagebox.showerror("Error "," Cannot find a bookmark named: " + entrybookmark.get())
        #check if what you want to delete are all the bookmarks of the label
        elif entrylabel.get() != '' and entrybookmark.get() == '':
            for i in bookmarkslist:
                if i[0] == entrylabel.get():
                    if(messagebox.askyesno("Are you sure you want to delete? "," Are you sure you want to delete the label " + entrylabel.get() + "?")):
                        for i in bookmarkslist:
                            mycursor.execute("DELETE FROM BOOKMARKS WHERE LABEL=" + "'" + entrylabel.get() + "'" )
                        break
                    else:
                        break
                    #If it does not exist Show error
                elif i==(bookmarkslist[len(bookmarkslist)-1]):
                    messagebox.showerror("Error "," Cannot find a tag named: " + entrylabel.get())
        else:
            #If there is nothing Show error
            messagebox.showerror("Error "," The marker or tag name cannot be found or is incorrect")
        myconnection.commit()
        myconnection.close()
        writehtml()
    except:
        pass

#Graphic interface

    #Root, frame and configuration

root= Tk()
root.resizable(False,False)
root.title("BookMarks")
frame=Frame(root)
frame.pack()

    #StringVars

strlabel = StringVar()
strbookmark = StringVar()
strurl = StringVar()

    #Entrys

entrylabel=Entry(frame, textvariable=strlabel)
entrylabel.grid(row=0, column = 1,padx=10,pady=10)

entrybookmark=Entry(frame, textvariable=strbookmark)
entrybookmark.grid(row=1, column = 1,padx=10,pady=10)

entryurl=Entry(frame, textvariable=strurl)
entryurl.grid(row=2, column = 1,padx=10,pady=10)

    #Labels

entryla=Label(frame, text="Label")
entryla.grid(row=0, column=0, sticky="w", padx=10,pady=10)

entrybook=Label(frame, text="Bookmark")
entrybook.grid(row=1, column=0, sticky="w", padx=10,pady=10)

entryur=Label(frame, text="URL")
entryur.grid(row=2, column=0, sticky="w", padx=10,pady=10)

entrystyle=Label(frame, text="Page style:")
entrystyle.grid(row=4, column=0, sticky="w", padx=10,pady=10)

    #Buttons

savebutton=Button(frame, text="Save",command=savebookmark)
savebutton.grid(row=3,column=0,sticky="w", padx=10,pady=10)

botonborrar=Button(frame, text="Delete",command=deletebookmark)
botonborrar.grid(row=3,column=1,sticky="w", padx=10,pady=10)

botonborrar=Button(frame, text="Eewrite HTML",command=writehtml)
botonborrar.grid(row=3,column=2,sticky="w", padx=10,pady=10)

    #Radio buttons

radiovarcss=IntVar()
Radiobutton(root, text="Night", variable = radiovarcss, value = 1, command=writehtml).pack()
Radiobutton(root, text="Day", variable = radiovarcss, value = 2, command=writehtml).pack()
Radiobutton(root, text="Cyberpunk", variable = radiovarcss, value = 3, command=writehtml).pack()

root= mainloop()

