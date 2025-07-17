
from pathlib import Path
import os,shutil
import numpy as np
import pandas as pd
import tempfile

class SFControl:
    def __init__(self, sf_dir):
        self.superfish_dir = Path(sf_dir)
    def start_SF7(self,inputfile="",controlfile=""):
        app_name = "SF7.EXE"
        try:
            filepath=Path(inputfile)
            control=Path(controlfile)
            cmd_line=str(self.superfish_dir / app_name)+" "+str(control)+" "+str(filepath)
            print(f"Superfish command: {cmd_line}")
            os.system(cmd_line)
            print(f"Input File Path: {filepath}")
            SF7RESULT= "OUTSF7.TXT"
            with open(SF7RESULT, 'r') as SF7RESULT:
                lines = SF7RESULT.readlines()
                for line in lines:
                    if "Interpolated" in line:
                        outname = Path(line.split()[-1].strip()[:-1])
                        print(f"Output file found: {outname}")
                        break
            return outname if outname.exists() else None
        except Exception as e:
            print(f"Error starting Superfish: {e}")
            return None
class SFDataProcessor:
    def __init__(self, sf_dir):
        self.superfish_dir = Path(sf_dir)
    def create_sf7_input(self):
        pass
    def process_tbl_data(self, tbl_file):
        with open(tbl_file, 'r') as file:
            lines = file.readlines()
            found_data_start=False
            for i, line in enumerate(lines):
                if not found_data_start and "Data" in line:
                    start_index = i + 3
                    print(f"Start index: {start_index}")
                    found_data_start = True
                if "EndData" in line:
                    end_index = i
                    print(f"End index: {end_index}")
                    break
            data_lines = lines[start_index:end_index]
            data_lines = [line.strip().split() for line in data_lines if line.strip()]
            title = lines[start_index-2][1:].strip().split()
            unit= lines[start_index-1][1:].strip().split()
            df=pd.DataFrame(data_lines, columns=title)
        return df, title, unit
            
if __name__ == "__main__":
    sfdp=SFDataProcessor(r"C:\LANL")
    sfc=SFControl(r"C:\LANL")
    Path("temp").mkdir(exist_ok=True)
    testfieldpath=Path("./test/fieldresult/1CELL.T35").absolute()
    testfieldpath2=Path("./test/cavinputtest/CAVITY_INPUT.T35").absolute()
    controlfilepath=Path("./test/fieldresult/cmd.in7").absolute()
    with tempfile.TemporaryDirectory(dir="./temp") as tempdir:
        original_cwd = os.getcwd()
        os.chdir(Path(tempdir))
        
        print(f"Current working directory: {os.getcwd()}")
        tempin=shutil.copy(testfieldpath, os.getcwd())
        tempctrl=shutil.copy(controlfilepath, os.getcwd())
        print(f"Copied test field file to: {tempin}")
        resultfile=sfc.start_SF7(controlfile=tempctrl,inputfile=tempin)
        df,title,unit=sfdp.process_tbl_data(resultfile)
        print(f"Result of starting SF7: {df}")
        
        # result=sfc.start_SF7(controlfile=controlfilepath,inputfile=testfieldpath2)
        os.chdir(original_cwd)
