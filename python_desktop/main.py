import serial
import tkinter as Tk
import threading
import queue



class Main():
    def __init__(self):

        # Initialize servo positions
        self.posX = 0
        self.posY = 0


        # Create que for inter-thread communication
        self.messageQue = queue.Queue()


        self.root = Tk.Tk()
        self.root.title("Symmetric Dashboards")
        # Set the size of the window
        self.root.geometry("600x300")
        


        self.setupGUI()


        # Setup the serial communication which will run in a seperate thread,
        # So serial commands can be processed in parallel in real time.
        self.serialCommunicationThread = threading.Thread(target=self.serialCommunication)
        self.serialCommunicationThread.daemon = True
        self.serialCommunicationThread.start()



        # Start the main loop
        self.root.mainloop()


    def serialCommunication(self):
        
        ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)
        
        while True:

            if not self.messageQue.empty():
                commandToSend = self.messageQue.get()
                print(f"Serial Thread: Sending message `{commandToSend}`")
                ser.write(commandToSend.encode())

            # Read line from serial port (you can use .read() or .readline() depending on your data format)
            data = ser.readline().decode('utf-8', errors="ignore").strip()
            # print(data)
        
    def setupGUI(self):
        # Configure the grid to make columns and rows expandable
        self.root.grid_columnconfigure(0, weight=1, uniform="equal")
        self.root.grid_columnconfigure(1, weight=1, uniform="equal")
        self.root.grid_rowconfigure(0, weight=1)

        # Create the left dashboard frame
        self.left_frame = Tk.Frame(self.root, width=300, height=300)
        self.left_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Add a label to the left dashboard
        self.label_left = Tk.Label(self.left_frame, text="Left Dashboard", font=("Arial", 14))
        self.label_left.pack(pady=20)

        # Create a frame for the buttons in the left dashboard (to arrange them horizontally)
        self.buttons_left = Tk.Frame(self.left_frame)
        self.buttons_left.pack(fill="x", pady=20)

        # Add the buttons horizontally, ensuring even spacing
        self.button_left_1 = Tk.Button(self.buttons_left, text="<", command=lambda: self.makeMovement("x", "l"))
        self.button_left_1.pack(side="left", expand=True, padx=10)

        self.button_left_2 = Tk.Button(self.buttons_left, text=">", command=lambda: self.makeMovement("x", "r"))
        self.button_left_2.pack(side="left", expand=True, padx=10)

        # Add a label to the left dashboard
        self.position_label_left = Tk.Label(self.left_frame, text="Position", font=("Arial", 14))
        self.position_label_left.pack(pady=20)

        # Create the right dashboard frame
        self.right_frame = Tk.Frame(self.root, width=300, height=300)
        self.right_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        # Add a label to the right dashboard
        self.label_right = Tk.Label(self.right_frame, text="Right Dashboard", font=("Arial", 14))
        self.label_right.pack(pady=20)

        # Create a frame for the buttons in the right dashboard (to arrange them horizontally)
        self.buttons_right = Tk.Frame(self.right_frame)
        self.buttons_right.pack(fill="x", pady=20)

        # Add the buttons horizontally, ensuring even spacing
        self.button_right_1 = Tk.Button(self.buttons_right, text="<", command=lambda: self.makeMovement("y", "l"))
        self.button_right_1.pack(side="left", expand=True, padx=10)

        self.button_right_2 = Tk.Button(self.buttons_right, text=">", command=lambda: self.makeMovement("y", "r"))
        self.button_right_2.pack(side="left", expand=True, padx=10)

        # Add a label to the left dashboard
        self.position_label_right = Tk.Label(self.right_frame, text="Position", font=("Arial", 14))
        self.position_label_right.pack(pady=20)

    # target: x, y
    # direction: r, l
    def makeMovement(self, target, direction):
        self.messageQue.put(f"{target} {direction}")



if __name__ == "__main__":
    Main()
