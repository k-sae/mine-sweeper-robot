from tkinter import *
from mine_sweeper.view.Menu import Menu

if __name__ == "__main__":

    root = Tk()
    root.minsize(640, 640)
    '''root.geometry('640x640')
    #resizing background to be responsive
    def resize_image(event):
        new_width = event.width
        new_height = event.height
        image = copy_of_image.resize((new_width, new_height))
        photo = ImageTk.PhotoImage(image)
        label.config(image=photo)
        label.image = photo  # avoid garbage collection


    image = Image.open('resources/13950123000568_PhotoI.jpg')
    copy_of_image = image.copy()
    photo = ImageTk.PhotoImage(image)
    label = ttk.Label(root, image=photo)
    label.bind('<Configure>', resize_image)
    label.pack(fill=BOTH, expand=YES)'''

    Menu(root)
    root.mainloop()

