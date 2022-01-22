import matplotlib.pyplot as plt
class gCode:
    def __init__(self, FILE_PATH):
        self.FILE_PATH = FILE_PATH

    def getGcode(self):

        f = open(self.FILE_PATH, "r")
        f_text = f.read()
        f.close()

        text = f_text.splitlines()

        return text

    def cleanGcode(self):

        text = gCode.getGcode(self)
        pure_code = []

        for i in range(len(text)):
            if ((";" not in text[i]) and (text[i] != "")):
                pure_code.append(text[i])
            elif (not text[i].startswith(";")) and (text[i] != ""):
                pure_code.append(text[i][:text[i].find(";")].strip())
                
        return pure_code

    def lines(self):
        lines = len(gCode.cleanGcode(self))
        return lines
        
    def parseGcode(self):

        parsed_code = gCode.cleanGcode(self)

        for i in range(len(parsed_code)):
        
            parsed_code[i] = parsed_code[i].split(" ")

        for i in range(len(parsed_code)):
            for j in range(len(parsed_code[i])):
                parsed_code[i][j] = [parsed_code[i][j][0],parsed_code[i][j][1:]]

        return parsed_code

    def plot(self, xlim, ylim, zlim, frameOn = False):
        parsed = gCode.parseGcode(self)

        relative_pos = False
        absolute_pos = True

        x = []
        y = []
        z = []

        for i in range(len(parsed)):
            command_type = parsed[i][0][0] + parsed[i][0][1]

            if command_type == "G91":
                relative_pos = True
                absolute_pos = False

            if command_type == "G90":
                relative_pos = False
                absolute_pos = True
            
            if command_type == "G28":
                x.append(0)
                y.append(0)
                z.append(0)

            if (command_type == "G0" or command_type == "G1"):
                if (relative_pos == False and absolute_pos == True):
                    command_types = []
                    for j in range(len(parsed[i])):
                        command_types.append(parsed[i][j][0])
                    if "X" in command_types:
                        x.append(float(parsed[i][command_types.index("X")][1]))
                    else:
                        x.append(x[-1])
                    if "Y" in command_types:
                        y.append(float(parsed[i][command_types.index("Y")][1]))
                    else:
                        y.append(y[-1])
                    if "Z" in command_types:
                        z.append(float(parsed[i][command_types.index("Z")][1]))
                    else:
                        z.append(z[-1])
                
                elif (relative_pos == True and absolute_pos == False):
                    command_types = []
                    for j in range(len(parsed[i])):
                        command_types.append(parsed[i][j][0])
                    if "X" in command_types:
                        x.append((float(x[-1]) + float(parsed[i][command_types.index("X")][1])))
                    else:
                        x.append(x[-1])
                    if "Y" in command_types:
                        y.append((float(y[-1]) + float(parsed[i][command_types.index("Y")][1])))
                    else:
                        y.append(y[-1])
                    if "Z" in command_types:
                        z.append((float(z[-1]) + float(parsed[i][command_types.index("Z")][1])))
                    else:
                        z.append(z[-1])

        fig = plt.figure()
        ax = plt.axes(projection ='3d')

        if (frameOn == True):
            x_printer = [0,xlim,xlim,0,0,0,xlim,xlim,xlim,xlim,xlim,xlim,0,0,0,0]
            y_printer = [0,0,ylim,ylim,0,0,0,0,0,ylim,ylim,ylim,ylim,ylim,ylim,0]
            z_printer = [0,0,0,0,0,zlim,zlim,0,zlim,zlim,0,zlim,zlim,0,zlim,zlim]
            ax.plot3D(x_printer, y_printer, z_printer, 'blue')

        ax.plot3D(x, y, z, 'green')
        ax.set_title('Printing Path')
        ax.set_xlim([0,int(xlim+ylim+zlim)/3])
        ax.set_ylim([0,int(xlim+ylim+zlim)/3])
        ax.set_zlim([0,int(xlim+ylim+zlim)/3])
        plt.show()

    def saveGcode(self, code): 
        f = open("output.gcode", "w")
        for i in range(len(code)):
            f.write(code[i])
            if i == len(code)-1:
                break
            f.write("\n")
        f.close()