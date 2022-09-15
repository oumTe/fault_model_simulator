# Software fault model simulator and result analysis automator

This tool entails simulating software fault models automatically using existing software fault models and additional models inferred from physical
fault injections and developing an automated method to compare software fault simulation and physical injection, as well as software simulation and RTL. 
This gives support to engineers as they conduct a series of more rigorous tests on the system under investigation in real time.

## Supported faut models

### Instruction Skip
Skipping one or more instructions from the target program.

### Instruction Skip and instruction repeat
This model involves skipping one or more instructions and then repeating one or more previously executed instructions.

### Double instruction corruption
#### Repeating bits that belong to 32-bit instruction 

This model is the consequence of replacing 32 bits of a misaligned code fetched to the memory with previous word, where the first bits repeated represent the least significant 16 bits of a 32-bit instruction.

![image](https://user-images.githubusercontent.com/72249224/190470176-391e6107-c73b-43e4-b9c0-648fac2a2c01.png)

#### Repeating bits that belong to 16-bit instruction

This model is the consequence of replacing 32 bits of a misaligned code fetched to the memory with previous word, where the first bits repeated represent a 16-bit instruction.

![image](https://user-images.githubusercontent.com/72249224/190471237-e2797356-fb85-4fb3-91a3-2e4c4efa1b8b.png)

### Instruction Skip and instruction corruption

This model is the consequence of skipping one or more lines of a misaligned code fetched to the memory.

![image](https://user-images.githubusercontent.com/72249224/190471524-596d8598-638f-4cb4-bed0-1f400da80fb3.png)

### Instruction skip, instruction repeat and double instruction corruption
#### The first 16 bits repeated belong to a 32-bit instruction
This model is the consequence of replacing one or more lines of a misaligned code fetched to the memory with previous ones, where the first bits repeated represent the least significant 16 bits of a 32-bit instruction.

![image](https://user-images.githubusercontent.com/72249224/190473409-b1789ab7-2d95-4bf0-b84c-8e2b1ef58dd1.png)


#### The first 16 bits repeated represent a 16-bit instruction
This model is the consequence of replacing one or more lines of a misaligned code fetched to the memory with previous ones, where the first bits repeated represent a 16-bit instruction.

![image](https://user-images.githubusercontent.com/72249224/190473472-a49d88a3-94b9-404a-9bb1-545a2eb7552a.png)

### Instruction skip and new instruction execution

This model is the consequence of skiping one or more lines of a misaligned code fetched to the memory with previous ones, where the first bits skipped represent a 16-bit instruction.

![image](https://user-images.githubusercontent.com/72249224/190473651-be57e328-0a37-45ea-b61e-744b1718b119.png)

### Instruction corruption with zeros

This model is the consequence of skiping one or more lines of a misaligned code fetched to the memory and inserting a sequence of zeros in its place.

![image](https://user-images.githubusercontent.com/72249224/190473783-d1ed92bb-2ba6-4051-ab15-813958679fdb.png)

![image](https://user-images.githubusercontent.com/72249224/190473817-53526114-2aca-4150-b759-89300c89be84.png)

### One operand corruption

In this model one or more operands are corrupted using the previous instruction.

![image](https://user-images.githubusercontent.com/72249224/190474077-f2afa219-7dbf-428e-9b5b-1eb06080db34.png)


### One instruction corruption, changing it to MOV instruction

In this model an instruction is corrupted by a mov instruction were its source operand is R0. 
![image](https://user-images.githubusercontent.com/72249224/190474247-61bc0749-8293-4eeb-90d9-1d8955af5585.png)

## Running the tool
This tool is a Linux-based Python script. In order to use it, begin by cloning the github repository or downloading the ZIP code file. 

### Create a virtual environment
Once downloaded, navigate to the folder containing the source code and start a virtual envirenment with the code below.

**virtualenv [Name of virtual environment]**

**source ./[Name of virtual environment]/bin/activate**

### Installing the requirenments 

In order to install the requirements the command that follows should be executed.

**pip install numpy & pip install pandas & pip install fpdf & pip install keystone-engine & pip install capstone.**

### Executing the script

To use this tool, the main script must be executed. Navigate to the project folder and run the following command: 

**python main.py**. 

Fellow the instruction to perform the analysis and by the end navigate to the code folder to find the report(s) and the csv file containing the software fault model simulation.


For more information about the models please refer to : 

https://ieeexplore.ieee.org/abstract/document/9505074

https://bcolombier.fr/assets/publis_PDF/2022/Alshaer_DSD_2022.pdf

